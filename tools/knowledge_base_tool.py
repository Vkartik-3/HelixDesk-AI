import os
import requests
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

# Config
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_SEARCH_INDEX_NAME = "it-ticket-solutions-index"
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
AZURE_OPENAI_API_VERSION = "2024-02-15-preview"

# Clients
openai_client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

def embed_text(text: str):
    response = openai_client.embeddings.create(
        input=[text],
        model=AZURE_OPENAI_DEPLOYMENT
    )
    return response.data[0].embedding

def search_similar_solution(query: str, category: str) -> str:
    embedding = embed_text(query)

    url = f"{AZURE_SEARCH_ENDPOINT}/indexes/{AZURE_SEARCH_INDEX_NAME}/docs/search?api-version=2023-07-01-Preview"

    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_SEARCH_KEY
    }

    payload = {
        "search": "",
        "vectors": [
            {
                "value": embedding,
                "fields": "embedding",
                "k": 3
            }
        ],
        "select": "category,problem,solution",
        "filter": f"category eq '{category}'"
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        return f"Error while searching: {response.text}"

    results = response.json().get("value", [])

    if not results:
        return "No matching solutions found."

    response_text = ""
    for idx, doc in enumerate(results, 1):
        response_text += (
            f"\nResult {idx}:\n"
            f"Category: {doc.get('category')}\n"
            f"Problem: {doc.get('problem')}\n"
            f"Solution: {doc.get('solution')}\n"
        )

    return response_text

if __name__ == "__main__":
    query = "My Outlook crashes every time I open it"
    rag_output = search_similar_solution(query, category="Software Bug")
    print(rag_output)