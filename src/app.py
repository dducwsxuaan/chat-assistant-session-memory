from core.memory_manager import MemoryManager
from core.query_processor import QueryProcessor
from graph.builder import build_graph

mm = MemoryManager()
qp = QueryProcessor(mm)
graph = build_graph()

while True:
    user_input = input("User: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Exiting session...")
        break
    state = {
        "user_query": user_input,
        "messages": mm.history,
        "mm": mm,
        "qp": qp
    }

    result = graph.invoke(state)

    print(result["assistant_output"])
