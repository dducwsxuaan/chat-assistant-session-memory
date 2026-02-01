from pydantic import BaseModel, Field
from typing import List, Dict, Literal

class UserProfile(BaseModel):
    prefs: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)

class SummaryContent(BaseModel):
    user_profile: UserProfile
    key_facts: List[str] = Field(default_factory=list)
    decisions: List[str] = Field(default_factory=list)
    open_questions: List[str] = Field(default_factory=list)
    todos: List[str] = Field(default_factory=list)

class SessionSummary(BaseModel):
    session_summary: SummaryContent
    message_range_summarized: Dict[str, int] = Field(
        default_factory=lambda: {"from": 0, "to": 0}
    )

MemoryFields = Literal[
    "user_profile.prefs", 
    "user_profile.constraints", 
    "key_facts", 
    "decisions", 
    "open_questions", 
    "todos"
]

class QueryUnderstanding(BaseModel):
    original_query: str
    is_ambiguous: bool
    rewritten_query: str
    needed_context_from_memory: List[MemoryFields]
    clarifying_questions: List[str]
    final_augmented_context: str