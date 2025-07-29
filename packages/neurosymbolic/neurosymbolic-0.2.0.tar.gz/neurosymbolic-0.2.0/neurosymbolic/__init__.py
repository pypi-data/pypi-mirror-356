import argparse
import enum

from langchain_community.tools import ReadFileTool, WriteFileTool
from pydantic import BaseModel, Field

from neurosymbolic.tools.bash import Bash
from neurosymbolic.tools.python import Python
from neurosymbolic.z3tool import Z3Tool

from .blocks import TOKEN_LOGGER, cast_n, eval_n, eval_python


def main():
    """Simple neurosymbolic solver with bash/z3/read/write file capabilities."""
    parser = argparse.ArgumentParser(description="Neurosymbolic solver")
    parser.add_argument("goal", help="Goal for the neurosymbolic solver")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Increase output verbosity"
    )
    parser.add_argument("-d", "--debug", action="store_true", help="Debug mode")
    parser.add_argument(
        "-g",
        "--graph",
        action="store_true",
        help="Generate graph of the langgraph workflow",
    )
    args = parser.parse_args()

    user_input = args.goal
    verbose = args.verbose
    debug = args.debug

    toolbox = [
        Bash(verbose=verbose),
        # Z3Tool(verbose=verbose),
        # ReadFileTool(verbose=verbose),
        # WriteFileTool(verbose=verbose),
        # Python(verbose=verbose),
    ]
    try:
        result = eval_n(prompt=user_input, toolbox=toolbox)
        print(repr(result))
        if debug and result:
            _, messages = result
            for message in messages:
                print(message)
    finally:
        tokens = TOKEN_LOGGER.total_tokens
        cost = TOKEN_LOGGER.total_cost
        print(f"Total tokens: {tokens}")
        print(f"Total cost: ${cost:.6f}")


__all__ = ["main"]
