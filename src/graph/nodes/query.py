from graph.state import State

def check_ambiguity(state: State):
    qp = state["qp"]

    analysis = qp.process(state["user_query"])

    return {
        **state,
        "query_analysis": analysis
    }
