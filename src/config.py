import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "qwen/qwen3-32b"


LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
MEMORY_LOG_FILE = os.path.join(LOG_DIR, "session_memory.jsonl")
QUERY_LOG_FILE = os.path.join(LOG_DIR, "query_analysis.jsonl")
CURRENT_SUMMARY_FILE = os.path.join(LOG_DIR, "current_summary.json")

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found. Please set it as environment variable."
        )

    return Groq(api_key=api_key)

groq_client = get_groq_client()