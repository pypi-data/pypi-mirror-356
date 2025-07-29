import logging
import re
import time
import traceback
from typing import Union, Optional, List, TypeVar, Iterable

from lxml import etree
from pydantic import BaseModel

from duowen_agent.llm import OpenAIChat, MessagesSet
from duowen_agent.tools.base import BaseTool
from duowen_agent.tools.manager import ToolManager
from duowen_agent.tools.mcp_client import McpClient
from duowen_agent.utils.core_utils import stream_to_string
from duowen_agent.utils.string_template import StringTemplate
from duowen_agent.utils.xml_tool_parser import parse_xml_tool_calls
from .base import BaseAgent
from ..error import ObserverException
from ..prompt.prompt_build import prompt_now_day
from ..utils.core_utils import generate_unique_id, remove_think

REACT_SYSTEM_PROMPT_TEMPLATE = StringTemplate(
    template_format="jinja2",
    template="""
# 修改后的提示词

作为勤勉的任务代理，你的目标是尽可能高效地完成提供的任务或问题。

## Tools
你可以使用以下工具，工具信息通过以下结构描述提供：
{{tool_descriptions}}

## Output Format
请使用以下XML格式回答问题。仅返回XML，不要有解释。否则将会受到惩罚。
输出必须符合以下XML格式规范。仅返回XML，不要解释。

```xml
<response>
  <analysis>当前操作思路及原因分析</analysis>
  <function_calls>
    <invoke name="工具名称">
      <parameter name="参数名1">参数值1</parameter>
      <parameter name="参数名2">["参数值1","参数值2"]</parameter> 
    </invoke>
  </function_calls>
</response>
```

如果使用此格式，用户将按以下格式回应：

```
Observation: tool response
```

你应持续重复上述格式，直到获得足够信息无需继续使用工具即可回答问题。此时必须改用以下两种格式之一：

- 若能回答问题：

```xml
<response>
  <analysis>最终判断依据及结论</analysis>
  <function_calls>
    <invoke name="finish">
      <parameter name="content">你的答案</parameter>
    </invoke>
  </function_calls>
</response>
```

- 若当前上下文无法回答问题：

```xml
<response>
  <analysis>无法解决的原因分析</analysis>
  <function_calls>
    <invoke name="finish">
      <parameter name="content">抱歉，我无法回答您的查询，因为（总结所有步骤并说明原因）</parameter>
    </invoke>
  </function_calls>
</response>
```

## Attention
- 仅返回XML格式，不要有解释
- 每一步只能选择一个工具
- 最终答案语言需与用户提问语言一致
- 动作参数的格式（XML或字符串）取决于工具定义

## User question
{{question}}

## Current Conversation
以下是当前对话历史记录，包含交替的用户提问和助手回复：

""",  # noqa: E501
)
PREFIX_TEMPLATE = """你是一个{agent_identity}，名为{agent_name}，你的目标是{agent_goal}，限制条件是{agent_constraints}。"""  # noqa


class ActionResponseArgs(BaseModel):
    name: str
    args: Union[dict, str]


class ActionResponse(BaseModel):
    analysis: str
    action: ActionResponseArgs


class ReactActionParameters(BaseModel):
    analysis: Optional[str] = None
    action_name: str
    action_parameters: Optional[dict] = None


class ReactAction(BaseModel):
    action: ReactActionParameters
    cell_id: str


T = TypeVar("T")


class ReactObservationResult(BaseModel):
    result: str
    view: Optional[T] = None


class ReactObservation(BaseModel):
    observation: ReactObservationResult
    action: ReactActionParameters
    exec_status: bool
    cell_id: str


class ReactResult(BaseModel):
    result: str
    cell_id: str


class ReactAgent(BaseAgent):

    def __init__(
        self,
        *,
        llm: OpenAIChat,
        tools: List[BaseTool] = None,
        mcp_client: Optional[McpClient] = None,
        prefix_prompt: str = None,
        filter_function_list: List[str] = None,
        max_iterations: Optional[int] = 15,
        _from: Optional[str] = None,
    ):
        super().__init__()
        self.tool_manager = ToolManager(tools, filter_function_list) if tools else None
        self.mcp_client = mcp_client
        self.llm = llm
        self.system_prompt_template: StringTemplate = REACT_SYSTEM_PROMPT_TEMPLATE
        self.conversation_prompt: str = ""
        self.filter_function_list = filter_function_list
        self.max_iterations = max_iterations
        self.max_execution_time: Optional[float] = None
        self.prefix_prompt = prefix_prompt

    def get_llm(self) -> OpenAIChat:
        return self.llm

    def _build_system_prompt(self, instruction: str | MessagesSet) -> str:

        prefix_prompt = self.prefix_prompt or ""

        _func_tool_descriptions = (
            self.tool_manager.tool_descriptions if self.tool_manager else "\n"
        )

        _mpc_tool_descriptions = (
            self.mcp_client.tool_descriptions if self.mcp_client else "\n"
        )

        if isinstance(instruction, MessagesSet):
            _instruction = instruction.get_format_messages()
        else:
            _instruction = instruction

        return (
            prefix_prompt
            + "\n\n"
            + self.system_prompt_template.format(
                question=_instruction,
                tool_descriptions=_func_tool_descriptions + _mpc_tool_descriptions,
            )
        )

    @property
    def current_date(self) -> str:
        return prompt_now_day()
        # f"Current date: {time.strftime('%Y-%m-%d %H:%M:%S')}"

    def _run(
        self,
        instruction: str | MessagesSet,
        return_raw_data: bool = False,
        verbose=True,
        **kwargs,
    ) -> Iterable[Union[ReactAction, ReactObservation, ReactResult]]:
        self.conversation_prompt = self._build_system_prompt(instruction)
        logging.debug(f"[agent] ToolAgent system prompt: {self.conversation_prompt}")

        iterations = 0
        used_time = 0.0
        start_time = time.time()

        while self._should_continue(iterations, used_time):
            cell_id = generate_unique_id("react")
            llm_resp = stream_to_string(
                self.llm.chat_for_stream(
                    messages=self.conversation_prompt + self.current_date
                )
            )

            while llm_resp == "":
                llm_resp = stream_to_string(
                    self.llm.chat_for_stream(
                        messages=self.conversation_prompt + self.current_date
                    )
                )

            try:
                action_resp: ActionResponse = self._parse_llm_response(llm_resp)
            except ObserverException as e:
                logging.warning(f"ReactAction parse llm response error: {str(e)} ")
                self.conversation_prompt += f"\nAction:{remove_think(llm_resp)}\n"
                self.conversation_prompt += f"\nObservation: ReactAction parse llm response error: {str(e)} ;response data : {remove_think(llm_resp)}\n"
                continue

            if verbose:
                yield ReactAction(
                    **{
                        "action": {
                            "analysis": action_resp.analysis,
                            "action_name": action_resp.action.name,
                            "action_parameters": action_resp.action.args,
                        },
                        "cell_id": cell_id,
                    }
                )

            self.conversation_prompt += f"\nAction:{remove_think(llm_resp)}\n"
            logging.debug(
                f"[dw] tool agent <{iterations}> current prompt: {self.conversation_prompt}"  # noqa
            )

            if "finish" in action_resp.action.name:
                if return_raw_data:
                    _res = ReactResult(result=action_resp, cell_id=cell_id)
                else:
                    _res = ReactResult(
                        result=action_resp.action.args["content"], cell_id=cell_id
                    )
                    yield _res
                return

            try:
                tool_result, tool_result_meta = self.run_tool(
                    action_resp.action.name, action_resp.action.args
                )
                tool_exec_status = True
            except ObserverException as e:
                tool_result, tool_result_meta = str(e), None
                tool_exec_status = False
            except Exception as e:
                tool_result, tool_result_meta = str(e), None
                tool_exec_status = False
                logging.error(f"Tool execution error: {traceback.format_exc()}")

            self.conversation_prompt += f"Observation: {tool_result}\n"
            if verbose:
                yield ReactObservation(
                    **{
                        "observation": {
                            "result": tool_result,
                            "view": tool_result_meta,
                        },
                        "action": {
                            "analysis": action_resp.analysis,
                            "action_name": action_resp.action.name,
                            "action_parameters": action_resp.action.args,
                        },
                        "exec_status": tool_exec_status,
                        "cell_id": cell_id,
                    }
                )
            iterations += 1
            used_time += time.time() - start_time

    def run_tool(self, tool_name: str, parameters: Union[str, dict]):

        if self.tool_manager and self.tool_manager.get_tool(tool_name):
            return self.tool_manager.run_tool(tool_name, parameters)
        elif self.mcp_client.get_tool_info(tool_name):
            return self.mcp_client.run_tool(tool_name, parameters), None
        else:
            return f"未知的工具调用{tool_name}", None

    def _should_continue(self, current_iteration: int, current_time_elapsed) -> bool:
        if self.max_iterations and current_iteration >= self.max_iterations:
            return False
        if self.max_execution_time and current_time_elapsed >= self.max_execution_time:
            return False
        return True

    @staticmethod
    def _extract_response_block(xml_content: str) -> Optional[str]:
        """
        从XML内容中提取第一个完整的<response>...</response>块

        参数:
            xml_content: 包含可能多个XML块的字符串内容

        返回:
            包含完整<response>块的字符串，如果未找到则返回None
        """
        pattern = r"<response>.*?</response>"
        matches = re.findall(pattern, xml_content, re.DOTALL)

        if matches:
            return matches[0]
        return None

    @staticmethod
    def _extract_analysis(response_block: str) -> Optional[str]:
        """
        从<response>块中提取<analysis>标签的内容

        参数:
            response_block: 完整的<response> XML块字符串

        返回:
            <analysis>标签内的文本内容（如存在），如果未找到则返回None
        """
        try:
            # 方法1：使用lxml解析（推荐，更健壮）
            root = etree.fromstring(response_block)
            analysis = root.find(".//analysis")
            if analysis is not None:
                return analysis.text
            return None
        except:
            # 方法2：正则解析（备选方案）
            pattern = r"<analysis>(.*?)</analysis>"
            match = re.search(pattern, response_block, re.DOTALL)
            if match:
                return match.group(1).strip()
            return None

    @staticmethod
    def _parse_llm_response(llm_resp: str) -> ActionResponse:

        res = ReactAgent._extract_response_block(llm_resp)
        if not res:
            raise ObserverException("未找到完整的<response>...</response>块")

        analysis = ReactAgent._extract_analysis(res)
        if not analysis:
            raise ObserverException("未找到<analysis>...</analysis>标签")

        try:
            actions = parse_xml_tool_calls(res)
            for i in actions:
                return ActionResponse(
                    analysis=analysis,
                    action=ActionResponseArgs(
                        name=i.function_name,
                        args=i.parameters,
                    ),
                )
        except Exception as e:
            raise ObserverException(f"解析<response>...</response>块失败: {str(e)}")
