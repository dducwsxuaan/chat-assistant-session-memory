from typing import TypedDict, List, Dict, Any, Optional
from core.schemas import QueryUnderstanding
from core.memory_manager import MemoryManager
from core.query_processor import QueryProcessor

class State(TypedDict):
    user_query: str
    messages: List[Dict[str, str]]

    # Injected dependencies
    mm: MemoryManager
    qp: QueryProcessor

    # Query understanding
    query_analysis: Optional[QueryUnderstanding]
    active_query: Optional[str]
    augmented_context: Optional[str]

    # Clarification
    should_ask_user: Optional[bool]
    assistant_output: Optional[str]

    # Response
    final_response: Optional[str]

    # Memory
    should_summarize: Optional[bool]
