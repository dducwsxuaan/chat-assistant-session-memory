import json
from typing import List
from core.schemas import QueryUnderstanding
from config import groq_client, MODEL_NAME, QUERY_LOG_FILE

class QueryProcessor:
    def __init__(self, memory_manager):
        self.mm = memory_manager
    
    def _get_selective_memory(self, fields: List[str]) -> str:
        content = self.mm.summary_obj.session_summary
        extracted = []
        mapping = {
            "user_profile.prefs": content.user_profile.prefs,
            "user_profile.constraints": content.user_profile.constraints,
            "key_facts": content.key_facts,
            "decisions": content.decisions,
            "open_questions": content.open_questions,
            "todos": content.todos
        }
        for f in fields:
            if f in mapping and mapping[f]:
                extracted.append(f"{f}: {mapping[f]}")
        return "\n".join(extracted)

    def process(self, query: str) -> QueryUnderstanding:
        system_prompt = """
        You are the "Query Understanding" module for a sophisticated AI Assistant.
        Your goal is to analyze the user's latest query within the context of the conversation history and existing session memory.

        ### SESSION MEMORY STRUCTURE:
        The memory contains the following keys. You must decide which ones are necessary to answer the current query:
        1. "user_profile.prefs": User's specific preferences, style, or likes.
        2. "user_profile.constraints": Hard limits, laws (like GDPR), budgets, or "must-haves".
        3. "key_facts": General information provided about the project or topic.
        4. "decisions": Specific choices already agreed upon.
        5. "open_questions": Matters that still need clarification from previous turns.
        6. "todos": Pending tasks or next steps.

        ### YOUR TASKS:
        1. **Ambiguity Check**: Is the query unclear ON ITS OWN and WITHOUT context from the last Assistant question?
        2. **Query Rewriting**: If the query is related to the project in memory, rewrite it to be specific. 
           - Example: "Is it expensive?" -> "Is the security architecture for the Go/Next.js e-commerce platform expensive?"
           - Example: Assistant asks "Do you mean AWS?" -> User says "yes" -> Rewritten: "The user wants to proceed with AWS cloud hosting details."
        3. **Selective Retrieval**: List the exact memory keys required to provide a high-quality, context-aware answer. 
           - *Self-Correction Rule*: If the user asks about a technology mentioned in 'key_facts' (e.g., Next.js), you MUST include "key_facts" in 'needed_context_from_memory'.
        4. **Clarification**: Only generate new questions if the user's confirmation still leaves the intent vague.

        ### OUTPUT FORMAT (Strict JSON):
        Return ONLY a JSON object with this schema:
        {
          "is_ambiguous": boolean,
          "rewritten_query": "string",
          "needed_context_from_memory": ["key1", "key2"],
          "clarifying_questions": []
        }
        """

        current_memory = self.mm.summary_obj.session_summary.model_dump_json()
        recent_history = self.mm.history
        
        
        completion = groq_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Current Memory: {current_memory}\nRecent History: {recent_history}\nNew Query: {query}"}
            ],
            response_format={"type": "json_object"}
        )
        
        raw = json.loads(completion.choices[0].message.content)
        # needed = raw.get("needed_context_from_memory", [])
        rewritten = raw.get("rewritten_query", query)
        needed = raw.get("needed_context_from_memory", [])
        mem_context = self._get_selective_memory(needed)
        history_str = "\n".join([f"{m['role']}: {m['content']}" for m in self.mm.history[-8:]])

        final_ctx = f"Query: {raw.get('rewritten_query')}\n\nContext:\n{mem_context}\n\nHistory:\n{history_str}"

        analysis = QueryUnderstanding(
            original_query=query,
            is_ambiguous=raw.get("is_ambiguous", False),
            rewritten_query=raw.get("rewritten_query", query),
            needed_context_from_memory=needed,
            clarifying_questions=raw.get("clarifying_questions", []),
            final_augmented_context=final_ctx
        )

        with open(QUERY_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(analysis.model_dump_json() + "\n") 

        return analysis