from graph.state import State

def clarify_question(state: State):
    analysis = state["query_analysis"]

    should_ask = len(analysis.clarifying_questions) > 0

    return {
        **state,
        "should_ask_user": should_ask
    }
