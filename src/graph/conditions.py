from graph.state import State

def is_ambiguous(state: State):
    if state["query_analysis"].is_ambiguous:
        return "ambiguous"
    return "not_ambiguous"


def is_clarified(state: State):
    if state["should_ask_user"]:
        return "not_clarified"
    return "clarified"


def should_summarize(state: State):
    if state["should_summarize"]:
        return "summarize"
    return "continue"
