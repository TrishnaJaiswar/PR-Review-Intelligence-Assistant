
import os
from typing import TypedDict

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq

from backend.schemas import AIAnalysis
from backend.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE


load_dotenv()


class ReviewState(TypedDict):
    title: str
    description: str
    changed_code: str
    static_findings: list
    analysis: dict


def ai_review_node(state: ReviewState):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is missing from .env")

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0,
        api_key=api_key
    )

    structured_llm = llm.with_structured_output(
        AIAnalysis,
        method="json_mode"
    )

    prompt = USER_PROMPT_TEMPLATE.format(
        title=state["title"],
        description=state["description"][:3000],
        changed_code=state["changed_code"][:15000],
        static_findings=str(state["static_findings"])[:5000]
    )

    result = structured_llm.invoke([
        ("system", SYSTEM_PROMPT),
        ("human", prompt)
    ])

    return {"analysis": result.model_dump()}


builder = StateGraph(ReviewState)

builder.add_node("ai_review", ai_review_node)

builder.set_entry_point("ai_review")

builder.add_edge("ai_review", END)

review_graph = builder.compile()


def run_ai_review(
    title: str,
    description: str,
    changed_code: str,
    static_findings: list
):
    result = review_graph.invoke({
        "title": title,
        "description": description,
        "changed_code": changed_code,
        "static_findings": static_findings,
        "analysis": {}
    })

    return result["analysis"]
