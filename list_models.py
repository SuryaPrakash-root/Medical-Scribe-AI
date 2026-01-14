import os
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=api_key)

try:
    models_response = client.models.list()
    print("Available models:")
    for model in models_response.data:
        print(f"- {model.id}")
except Exception as e:
    print(f"Error listing models: {e}")
