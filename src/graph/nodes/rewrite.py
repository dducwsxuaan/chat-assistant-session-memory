from graph.state import State

def rewrite_query(state: State):
    analysis = state["query_analysis"]

    return {
        **state,
        "active_query": analysis.rewritten_query
    }
