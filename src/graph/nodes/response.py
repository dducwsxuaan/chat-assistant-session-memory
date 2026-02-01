from graph.state import State
from config import groq_client, MODEL_NAME

def respond(state: State):
    completion = groq_client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": state["augmented_context"]}
        ]
    )

    answer = completion.choices[0].message.content

    return {
        **state,
        "final_response": answer,
        "assistant_output": answer
    }
