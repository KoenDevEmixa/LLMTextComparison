from dotenv import load_dotenv
import os
from pathlib import Path


def read_txt_file_to_string(filepath: str):
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        doc = f.read()
    return doc


def get_api_key_url(client: str = "OPENAI"):
    # Only allow supported clients
    assert client in ["OPENAI", "MISTRAL", "GEMINI"], f"Unsupported client: {client}"

    # Load .env and get API key
    load_dotenv()
    if client == "OPENAI":
        api_key = os.getenv("OPENAI_API_KEY")
        api_url = "https://api.openai.com/v1"
    elif client == "MISTRAL":
        api_key = os.getenv("MISTRAL_API_KEY")
        api_url = "https://api.mistral.ai/v1"
    else:
        api_key = os.getenv("GEMINI_API_KEY")
        api_url = "https://generativelanguage.googleapis.com/v1beta"

    return api_key, api_url



