import os
from qdrant_client import QdrantClient
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# 🚀 Initialize Vector Database
if QDRANT_URL and QDRANT_API_KEY:
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    # FastEmbed AI model set kar rahe hain
    client.set_model("sentence-transformers/all-MiniLM-L6-v2")
    
    # Collection (Table) banayenge agar pehle se nahi hai
    if not client.collection_exists(collection_name="jarvis_memory"):
        client.create_collection(
            collection_name="jarvis_memory",
            vectors_config=client.get_fastembed_vector_params(),
        )
else:
    client = None
    print("⚠️ Long-Term Memory Offline: Qdrant keys missing in .env!")

def save_long_term_memory(text):
    """Important data ko hamesha ke liye vector banakar save karega"""
    if not client: return False
    try:
        client.add(
            collection_name="jarvis_memory",
            documents=[text],
        )
        return True
    except Exception as e:
        print(f"⚠️ Qdrant Save Error: {e}")
        return False

def search_long_term_memory(query, limit=2):
    """User ke sawal ke hisaab se purani yaadein dhoondh kar layega"""
    if not client: return ""
    try:
        results = client.query(
            collection_name="jarvis_memory",
            query_text=query,
            limit=limit
        )
        # Match hue results ko combine karna
        memory_texts = [res.document for res in results]
        return "\n".join(memory_texts)
    except Exception as e:
        print(f"⚠️ Qdrant Search Error: {e}")
        return ""