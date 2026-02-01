import tiktoken
import json
from config import groq_client, MODEL_NAME, MEMORY_LOG_FILE, CURRENT_SUMMARY_FILE
from .schemas import SessionSummary, SummaryContent, UserProfile
from core.utils import load_last_summary, load_json, save_json

class MemoryManager:
    def __init__(self, threshold=500):
        self.threshold = threshold
        self.history = []
        last_data = load_last_summary(MEMORY_LOG_FILE)
        snapshot = load_json(CURRENT_SUMMARY_FILE)

        if snapshot:
            self.summary_obj = SessionSummary.model_validate(snapshot)
        else:
            last_data = load_last_summary(MEMORY_LOG_FILE)
            if last_data:
                self.summary_obj = SessionSummary.model_validate(last_data)
            else:
                self.summary_obj = SessionSummary(
                    session_summary=SummaryContent(user_profile=UserProfile()),
                    message_range_summarized={"from": 0, "to": 0}
                )
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self) -> int:
        text = " ".join([m['content'] for m in self.history])
        return len(self.tokenizer.encode(text))

    def trigger_summarization(self) -> bool:
        if self.count_tokens() < self.threshold:
            return False

        system_msg = """Summarize the conversation into the following JSON schema. 
                        Always stick to the facts in the conversation. 
                        Do not invent project names or technologies not mentioned by the user. Return ONLY valid JSON:
                        {
                        "user_profile": {
                            "prefs": ["list of user preferences"],
                            "constraints": ["list of constraints"]
                        },
                        "key_facts": ["important facts from conversation"],
                        "decisions": ["decisions made"],
                        "open_questions": ["questions that need answering"],
                        "todos": ["action items"]
                        }
                    """
        user_msg = f"History: {self.history}\nCurrent Summary: {self.summary_obj.session_summary.model_dump_json()}\n\nExtract and update the summary based on the conversation history above."
        
        completion = groq_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            response_format={"type": "json_object"}
        )
        
        self.summary_obj.session_summary = SummaryContent.model_validate_json(completion.choices[0].message.content)
        current_len = len(self.history)
        self.summary_obj.message_range_summarized["to"] += current_len
        self.history = self.history[-5:]
        save_json(CURRENT_SUMMARY_FILE, self.summary_obj.model_dump())

        with open(MEMORY_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(self.summary_obj.model_dump_json() + "\n") 
            
        return True