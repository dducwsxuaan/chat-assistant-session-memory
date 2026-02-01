import json
import os

def save_json(file_path, data):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    temp_path = file_path + ".tmp"

    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    os.replace(temp_path, file_path)

def load_json(file_path):
    if not os.path.exists(file_path):
        return None

    if os.path.getsize(file_path) == 0:
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()

            if not content:
                return None

            return json.loads(content)

    except json.JSONDecodeError:
        print(f"[WARNING] Corrupted JSON file: {file_path}")
        return None

    except Exception as e:
        print(f"[ERROR] Failed loading {file_path}: {e}")
        return None



def load_last_summary(file_path):
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if lines:
                return json.loads(lines[-1]) # Lấy bản ghi cuối cùng
    except Exception as e:
        print(f"Error loading memory: {e}")
    return None
