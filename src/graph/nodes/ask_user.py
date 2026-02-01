from graph.state import State

def ask_user(state: State):
    questions = state["query_analysis"].clarifying_questions

    formatted = "\n".join(
        [f"{i+1}. {q}" for i, q in enumerate(questions)]
    )

    return {
        **state,
        "assistant_output": formatted,
        "final_response": None
    }
