from langchain_openai import ChatOpenAI
import os
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from logger import setup_logger
from dotenv import load_dotenv
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
setup_logger(logger)
load_dotenv()


class Agent:
    def __init__(self, tools: list[tool], master_prompt: SystemMessage):
        """The class can be used to intelligently control processes.

        Args:
            tools (list[tool]): list of tools/programs that model can use
            master_prompt (SystemMessage): detailed description of the instructions that the model should follow
        """
        self.tools = tools
        self.tools_dict = self._get_tools_dict()
        self.master_prompt = master_prompt
        self.messages = []

        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.0
        )
        self.llm = self.llm.bind_tools(self.tools)

    def _log_tools_calls(self, ai_msgs: list) -> None:
        for t in ai_msgs.tool_calls:
            logger.debug(f"FUNCTION CALL: {t}")

    def _get_tools_dict(self):
        tools_dict = {}
        for t in self.tools:
            tools_dict[t.name] = t
        return tools_dict

    def _call_tools(self, tools_to_call: list[AIMessage]) -> list[ToolMessage]:
        """Call list of tools with appropriate agruments. The list should be previously generated by the model.

        Args:
            tools_to_call (list[AIMessage]): list of tools with appropriate agruments

        Returns:
            list[ToolMessage]: list of tool execution values
        """
        tool_responses = []
        for tool_call in tools_to_call.tool_calls:
            try:
                logger.info(f"Writing to {tool_call['args']['file_path']} ...")
            except:
                pass
            selected_tool = self.tools_dict[
                tool_call["name"].lower()]
            tool_msg = selected_tool.invoke(tool_call)
            tool_responses.append(tool_msg)
        logger.info("All tools executed.")
        return tool_responses

    def execute_query(self, query: HumanMessage) -> None:
        """Executes user querry, generates logs, print final model answer. 

        Args:
            query (HumanMessage): Task description
        """
        self.messages = [self.master_prompt, query]
        # The model decides which tools to use and selects the appropriate arguments for them
        tools_to_call = self.llm.invoke(self.messages)
        self._log_tools_calls(tools_to_call)
        self.messages.append(tools_to_call)

        # Tools with the appropriate agruments are executed
        tools_responses = self._call_tools(tools_to_call=tools_to_call)
        for tr in tools_responses:
            self.messages.append(tr)

        # Final answer generation
        final_ans = self.llm.invoke(self.messages)
        logger.info(final_ans.content)
