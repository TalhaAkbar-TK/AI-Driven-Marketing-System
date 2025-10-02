"""
LangGraph Workflow Definition
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END
from agents.discovery_agent import discover_companies_node
from agents.research_agent import research_node
from agents.outreach_agent import outreach_node
from utils import to_serializable  # For final state


class AppState(TypedDict):
    companies: list
    high_fit_companies: list
    processed_companies: list
    sent_emails: list


def build_graph() -> StateGraph:
    workflow = StateGraph(AppState)

    workflow.add_node("discover", discover_companies_node)
    workflow.add_node("research", research_node)
    workflow.add_node("outreach", outreach_node)
    
    workflow.set_entry_point("discover")
    workflow.add_edge("discover", "research")
    workflow.add_edge("research", "outreach")
    workflow.add_edge("outreach", END)
    
    return workflow.compile()