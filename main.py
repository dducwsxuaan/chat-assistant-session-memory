from core.memory_manager import MemoryManager
from core.query_processor import QueryProcessor
from config import groq_client, MODEL_NAME

def main():
    memory = MemoryManager(threshold=50)
    processor = QueryProcessor(memory)
    ans = ""

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['exit', 'quit']:
            break

        memory.history.append({"role": "user", "content": user_input})
        

        analysis = processor.process(user_input)

        if analysis.is_ambiguous and analysis.clarifying_questions:
            ans = analysis.clarifying_questions[0]
            
        else:
            response = groq_client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Answer based on the provided context and history. Just need to provide the answer, no need to talk about what user expect or your steps of reasoning. You may include relevant details from the session memory as needed."},
                    {"role": "user", "content": analysis.final_augmented_context}
                ]
            )
            ans = response.choices[0].message.content

        print(f"Assistant: {ans}")

        
        memory.history.append({"role": "assistant", "content": ans})
        if memory.trigger_summarization():
            print("\n[System: Context threshold exceeded. Session memory updated via summarization.]")

if __name__ == "__main__":
    main()