from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import StringPromptTemplate
from langchain.chains import LLMChain
from langchain.schema import AgentAction, AgentFinish
from app.core.llm_client import get_llm
import re

class BaseAgent(ABC):
    def __init__(self, memory: Optional[ConversationBufferMemory] = None):
        self.llm = get_llm()
        self.memory = memory or ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.tools = self._setup_tools()
        self.agent = self._create_agent()
    
    @abstractmethod
    def _setup_tools(self) -> List[Tool]:
        pass
    
    @abstractmethod
    def _get_prompt_template(self) -> StringPromptTemplate:
        pass
    
    def _create_agent(self):
        prompt = self._get_prompt_template()
        llm_chain = LLMChain(llm=self.llm, prompt=prompt)
        
        # Custom output parser
        def output_parser(text: str):
            if "Final Answer:" in text:
                return AgentFinish(
                    return_values={"output": text.split("Final Answer:")[-1].strip()},
                    log=text
                )
            regex = r"Action: (.*?)[\n]*Action Input: (.*?)(?:\n|$)"
            match = re.search(regex, text, re.DOTALL)
            if not match:
                # If no action, treat as final
                return AgentFinish(return_values={"output": text}, log=text)
            action = match.group(1).strip()
            action_input = match.group(2).strip()
            return AgentAction(tool=action, tool_input=action_input, log=text)
        
        agent = LLMSingleActionAgent(
            llm_chain=llm_chain,
            output_parser=output_parser,
            stop=["\nObservation:"],
            allowed_tools=[tool.name for tool in self.tools]
        )
        return AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True
        )
    
    def run(self, input_text: str) -> str:
        return self.agent.run(input=input_text)