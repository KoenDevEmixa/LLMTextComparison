from dotenv import load_dotenv
import os
from pathlib import Path
import json
import pandas as pd
from pydantic.types import SecretStr

def read_txt_file_to_string(filepath: str):
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        doc = f.read()
    return doc

def json_to_table(
        output: str, 
        print_as_md: bool = True, 
        save_as_csv: bool = False, 
        filename: str = "rubric_result.csv"):
    try:
        results = json.loads(output)
    except json.JSONDecodeError:
        results = json.loads(output[output.find('['):output.rfind(']')+1])

    df = pd.DataFrame(results)

    if print_as_md:
        print(f"\n📊 {filename}:\n")
        print(df.to_markdown(index=False))

    if save_as_csv:
        df.to_csv(filename, index=False)
        print(f"💾 Tabel opgeslagen als: {filename}")

    return df

def get_api_key_url(client: str = "OPENAI", return_as_secret_strs: bool = True):
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

    if return_as_secret_strs:
        api_key = SecretStr(str(api_key))
        api_url = SecretStr(str(api_key))

    return api_key, api_url



