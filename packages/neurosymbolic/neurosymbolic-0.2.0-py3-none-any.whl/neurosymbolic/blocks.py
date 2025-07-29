## Sample building blocks for building neurosymbolic tools.

import os
from typing import Any, List, Optional

from langchain_community.callbacks.openai_info import OpenAICallbackHandler
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import PydanticToolsParser
from langchain_core.prompts import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI
from langgraph.errors import GraphRecursionError
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel

from .tools.bash import Bash
from .tools.python import Python
from .types import String


class NotFoundError(Exception):
    pass


NEUROSYM_DEFAULT_MODEL = os.environ.get("NEUROSYM_DEFAULT_MODEL", "gpt-3.5-turbo")
TOKEN_LOGGER = OpenAICallbackHandler()


def build_agent():
    """Single function to build agents"""
    agent = ChatOpenAI(
        temperature=0, model=NEUROSYM_DEFAULT_MODEL, callbacks=[TOKEN_LOGGER]
    )
    return agent


SYSTEM_PROMPT = os.environ.get(
    "NEUROSYM_SYSTEM_PROMPT",
    "Solve the task you were provided. You can run as many actions as necessary to solve the problem. You can use all tools at your disposal. Do not use a tool if you do not need it. Note that all commands you invoke have to be **'one-shot'**, in other words you **can't launch interactive sessions** because you are running within an llm chain.",
)


def cast_chain(target_type: BaseModel, agent=None, prompt=None) -> Runnable:
    """Cast an object to a given type."""

    if agent is None:
        agent = build_agent()

    tools_parser = PydanticToolsParser(tools=[target_type], strict=True)

    prompt = prompt or ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                "You are a tool that converts data to the given type. The type is: {type}"
            ),
            HumanMessagePromptTemplate.from_template(
                "You are given the data: ```{data}```. Convert the data to the given type: {type}."
            ),
        ]
    )
    chain: Runnable = (
        prompt | agent.bind_tools([target_type], strict=True) | tools_parser
    )
    return chain


def cast_n(
    data: Any, target_type: Optional[BaseModel], agent=None, config=None, prompt=None
) -> BaseModel:
    """Cast an object to a given type using agents based on neural models."""
    if target_type is None:
        target_type = String
    if agent is None:
        agent = build_agent()
    if config is None:
        config = {
            "configurable": {"thread_id": 42},
        }
    chain = cast_chain(target_type, agent=agent, prompt=prompt)
    return chain.invoke(
        {
            "data": data,
            "type": target_type,
        },
        config=config,
    )[0]


def eval_n(
    prompt: str,
    toolbox: List[Any],
    target_type: BaseModel = String,
    max_iterations: int = 100,
) -> Optional[BaseModel]:
    """Evaluate the given prompt using the provided toolbox and return an object of the target type."""
    model = build_agent()
    agent = create_react_agent(
        tools=toolbox,
        model=model,
        response_format=target_type,
    )
    try:
        return agent.invoke(
            {"messages": [HumanMessage(content=prompt)]},
            config={
                "configurable": {"thread_id": 42},
                "recursion_limit": max_iterations,
            },
        )["structured_response"]
    except GraphRecursionError:
        return None


def eval_python(*args, **kwargs):
    """
    Evaluate the given data using the Python interpreter.
    """
    # Create a new instance of the Python interpreter
    python_interpreter = Python(verbose=True)

    # Call the eval_s function with the Python interpreter as the agent
    return eval_n(*args, toolbox=[python_interpreter], **kwargs)


def eval_bash(*args, **kwargs):
    """
    Evaluate the given data using the Bash interpreter.
    """

    # Create a new instance of the Bash interpreter
    bash_interpreter = Bash(verbose=True)

    # Call the eval_s function with the Bash interpreter as the agent
    return eval_n(*args, toolbox=[bash_interpreter], **kwargs)
