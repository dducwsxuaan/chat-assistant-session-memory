from graph.state import State

def augment_query_with_context(state: State):
    analysis = state["query_analysis"]

    return {
        **state,
        "augmented_context": analysis.final_augmented_context
    }
