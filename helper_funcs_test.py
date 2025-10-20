from openai import OpenAI

from helper_funcs import get_api_key_url

def test_openai_connection():
    """Test whether the OpenAI API connection works."""
    api_key, api_url = get_api_key_url("OPENAI")
    if not api_key:
        raise ValueError("❌ No API key found in .env file!")

    client = OpenAI(api_key=api_key, base_url=api_url)

    try:
        models = client.models.list()
        print("✅ OpenAI API connection successful!")
        print("Available models (first 3):", [m.id for m in models.data[:3]])
    except Exception as e:
        print("❌ OpenAI API connection failed:", str(e))