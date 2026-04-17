import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer
from typing import List, Dict
from datetime import datetime
import uuid
from app.core.config import settings

class MemorySystem:
    def __init__(self):
        self.client = chromadb.Client(ChromaSettings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=settings.CHROMA_PERSIST_DIR
        ))
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        self.collection = self.client.get_or_create_collection("conversation_memory")
    
    def add_interaction(self, user_id: str, session_id: str, query: str, response: str):
        embedding = self.encoder.encode(query).tolist()
        self.collection.add(
            embeddings=[embedding],
            documents=[f"Q: {query}\nA: {response}"],
            metadatas=[{"user_id": user_id, "session_id": session_id, "timestamp": datetime.now().isoformat()}],
            ids=[f"{session_id}_{uuid.uuid4()}"]
        )
    
    def retrieve_relevant(self, query: str, user_id: str = None, k: int = 5) -> List[str]:
        query_emb = self.encoder.encode(query).tolist()
        where_filter = {"user_id": user_id} if user_id else None
        results = self.collection.query(
            query_embeddings=[query_emb],
            n_results=k,
            where=where_filter
        )
        return results['documents'][0] if results['documents'] else []