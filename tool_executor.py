from typing import List

from dotenv import load_dotenv
from langchain_community.tools import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.prebuilt.tool_node import ToolNode
from chain import parser
from schemas import AnswerQuestion, Reflection

load_dotenv()

search = TavilySearchAPIWrapper()
tavily_tool = TavilySearchResults(api_wrapper=search, max_results=5)


def execute_tools(state: List[BaseMessage]) -> List[BaseMessage]:
    tool_invocation: AIMessage = state[-1]
    parsed_tool_calls = parser.invoke(tool_invocation)

    ids = []
    tool_invocations = []

    for parsed_call in parsed_tool_calls:
        for query in parsed_call["args"]["search_queries"]:
            tool_invocations.append(ToolNode(
                tool="tavily_search_results_json",
                tool_input=query,
            ))


if __name__ == "__main__":
    print("Tool Executor Enter")

    human_message = HumanMessage(
        content="Write about AI-powered SOC / autonomous soc problem domain, list startups that do that and raised capital."
    )

    answer = AnswerQuestion(
        answer="",
        reflection=Reflection(missing="", superfluous=""),
        search_queries=[
            "AI-powered SOC startup funding",
            "AI SOC problem domain specifics",
            "Technologies used by AI-powered SOC startups"
        ],
    )

    raw_res = execute_tools(
        state=[
            human_message,
            AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": AnswerQuestion.__name__,
                        "args": answer.model_dump(),
                        "id": "call_1"
                    }
                ]
            )
        ]
    )
