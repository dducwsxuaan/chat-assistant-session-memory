from graph.state import State

def append_user_message(state: State):
    mm = state["mm"]

    mm.history.append({
        "role": "user",
        "content": state["user_query"]
    })

    return state

def append_assistant_message(state: State):
    mm = state["mm"]

    mm.history.append({
        "role": "assistant",
        "content": state["assistant_output"]
    })

    return state
