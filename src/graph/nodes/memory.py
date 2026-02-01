from graph.state import State

def check_conversation_length(state: State):
    mm = state["mm"]

    should = mm.count_tokens() >= mm.threshold
    

    return {
        **state,
        "should_summarize": should
    }


def summarize_conversation(state: State):
    mm = state["mm"]
    mm.trigger_summarization()
    return state

def store_session_memory(state: State):
    
    return state