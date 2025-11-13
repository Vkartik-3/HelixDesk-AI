
import os
import json
from tqdm import tqdm
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile
)
from azure.search.documents import SearchClient
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

# ---------------- CONFIG ----------------
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")  # e.g., https://your-search.search.windows.net
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_SEARCH_INDEX_NAME = "it-ticket-solutions-index"

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")  # e.g.,
AZURE_OPENAI_API_VERSION = "2024-02-15-preview"

DATA_FILE = "data/knowledge_base.json"
VECTOR_DIMENSIONS = 1536  # Based on OpenAI embeddings
# ----------------------------------------

# ---------- Clients ----------
credential = AzureKeyCredential(AZURE_SEARCH_KEY)
index_client = SearchIndexClient(endpoint=AZURE_SEARCH_ENDPOINT, credential=credential)
search_client = SearchClient(endpoint=AZURE_SEARCH_ENDPOINT, index_name=AZURE_SEARCH_INDEX_NAME, credential=credential)
openai_client = AzureOpenAI(api_key=AZURE_OPENAI_API_KEY, api_version=AZURE_OPENAI_API_VERSION, azure_endpoint=AZURE_OPENAI_ENDPOINT)


# ---------- Index Creation ----------
def create_index():
    print("📦 Creating index...")

    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True, filterable=True, sortable=True, facetable=True),
        SearchableField(name="category", type=SearchFieldDataType.String, filterable=True, sortable=True, facetable=True),
        SearchableField(name="problem", type=SearchFieldDataType.String, filterable=True, sortable=True, facetable=True),
        SearchableField(name="solution", type=SearchFieldDataType.String, filterable=True, sortable=True, facetable=True),
        SearchField(
            name="embedding",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=VECTOR_DIMENSIONS,
            vector_search_profile_name="default"
        )
    ]

    vector_search = VectorSearch(
        algorithms=[HnswAlgorithmConfiguration(name="default")],
        profiles=[VectorSearchProfile(name="default", algorithm_configuration_name="default")]
    )

    index = SearchIndex(name=AZURE_SEARCH_INDEX_NAME, fields=fields, vector_search=vector_search)

    try:
        # Try to get the index; if it exists, we skip creation
        index_client.get_index(name=AZURE_SEARCH_INDEX_NAME)
        print(f"ℹ️ Index '{AZURE_SEARCH_INDEX_NAME}' already exists. Skipping creation.")
    except Exception:
        # If not found, create the index
        index_client.create_index(index)
        print(f"✅ Index '{AZURE_SEARCH_INDEX_NAME}' created successfully.")


# ---------- Embedding ----------
def embed_text(text: str):
    response = openai_client.embeddings.create(
        input=[text],
        model=AZURE_OPENAI_DEPLOYMENT
    )
    return response.data[0].embedding


# ---------- Upload ----------
def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def upload_documents(docs):
    print(f"\n📤 Uploading {len(docs)} documents...")
    batch_size = 10
    for i in tqdm(range(0, len(docs), batch_size)):
        chunk = docs[i:i+batch_size]
        search_client.upload_documents(documents=chunk)
    print("✅ Upload completed.")

# ---------- Main ----------
def main():
    create_index()

    raw_docs = load_data()
    enriched_docs = []

    print("🔍 Generating embeddings...")
    for doc in tqdm(raw_docs):
        embedding = embed_text(doc["problem"])
        doc["embedding"] = embedding
        enriched_docs.append(doc)

    upload_documents(enriched_docs)


if __name__ == "__main__":
    main()
