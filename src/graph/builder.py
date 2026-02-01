from langgraph.graph import StateGraph, END
from .state import State
from .conditions import is_ambiguous, is_clarified, should_summarize

from .nodes.query import check_ambiguity
from .nodes.rewrite import rewrite_query
from .nodes.context import augment_query_with_context
from .nodes.clarification import clarify_question
from .nodes.ask_user import ask_user
from .nodes.response import respond
from .nodes.memory import (
    check_conversation_length,
    summarize_conversation,
    store_session_memory
)
from .nodes.history import append_user_message, append_assistant_message

def build_graph():

    workflow = StateGraph(State)

    workflow.add_node("Append User", append_user_message)
    workflow.add_node("Append Assistant", append_assistant_message)
    workflow.add_node("Query", check_ambiguity)
    workflow.add_node("Query Rewrite", rewrite_query)
    workflow.add_node("Context Augmentation", augment_query_with_context)
    workflow.add_node("Question Clarification", clarify_question)
    workflow.add_node("Ask User", ask_user)
    workflow.add_node("Response", respond)
    workflow.add_node("Conversation check", check_conversation_length)
    workflow.add_node("Summarization", summarize_conversation)
    workflow.add_node("Session memory store", store_session_memory)

    workflow.set_entry_point("Append User")
    workflow.add_edge("Append User", "Query")


    workflow.add_conditional_edges(
        "Query",
        is_ambiguous,
        {
            "ambiguous": "Query Rewrite",
            "not_ambiguous": "Context Augmentation"
        }
    )

    workflow.add_edge("Query Rewrite", "Context Augmentation")
    workflow.add_edge("Context Augmentation", "Question Clarification")

    workflow.add_conditional_edges(
        "Question Clarification",
        is_clarified,
        {
            "clarified": "Response",
            "not_clarified": "Ask User"
        }
    )

    workflow.add_edge("Ask User", "Append Assistant")
    workflow.add_edge("Append Assistant", END)

    workflow.add_edge("Response", "Append Assistant")
    workflow.add_edge("Append Assistant", "Conversation check")


    workflow.add_conditional_edges(
        "Conversation check",
        should_summarize,
        {
            "summarize": "Summarization",
            "continue": END
        }
    )

    workflow.add_edge("Summarization", "Session memory store")
    workflow.add_edge("Session memory store", END)

    return workflow.compile()
