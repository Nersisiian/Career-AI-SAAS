import faiss
import numpy as np
from typing import List, Tuple
import pickle
import os

class VectorStore:
    def __init__(self, dimension: int = 384, index_path: str = "/app/data/job_index.faiss"):
        self.dimension = dimension
        self.index_path = index_path
        self.mapping_path = index_path.replace(".faiss", ".pkl")
        self.index = None
        self.id_to_idx = {}
        self.idx_to_id = []
        self._load_or_create_index()
    
    def _load_or_create_index(self):
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.mapping_path, "rb") as f:
                data = pickle.load(f)
                self.id_to_idx = data["id_to_idx"]
                self.idx_to_id = data["idx_to_id"]
        else:
            self.index = faiss.IndexFlatIP(self.dimension)
    
    def add_embeddings(self, ids: List[str], embeddings: np.ndarray):
        faiss.normalize_L2(embeddings)
        start_idx = self.index.ntotal
        self.index.add(embeddings)
        for i, job_id in enumerate(ids):
            idx = start_idx + i
            self.id_to_idx[job_id] = idx
            self.idx_to_id.append(job_id)
        self._save()
    
    def search(self, query_embedding: np.ndarray, k: int = 20) -> List[Tuple[str, float]]:
        query_embedding = query_embedding.reshape(1, -1)
        faiss.normalize_L2(query_embedding)
        scores, indices = self.index.search(query_embedding, k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1 and idx < len(self.idx_to_id):
                results.append((self.idx_to_id[idx], float(score)))
        return results
    
    def _save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.mapping_path, "wb") as f:
            pickle.dump({"id_to_idx": self.id_to_idx, "idx_to_id": self.idx_to_id}, f)