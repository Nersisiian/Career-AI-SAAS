from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
import numpy as np

from app.core.model_loader import get_embedding_model
from app.api.deps import get_redis

router = APIRouter()

class EmbeddingRequest(BaseModel):
    texts: List[str]
    cache_key_prefix: str = "emb"

class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]

@router.post("/generate", response_model=EmbeddingResponse)
async def generate_embeddings(
    request: EmbeddingRequest,
    redis_client = Depends(get_redis)
):
    model = get_embedding_model()
    embeddings = []
    
    for idx, text in enumerate(request.texts):
        cache_key = f"{request.cache_key_prefix}:{hash(text)}"
        cached = redis_client.get(cache_key)
        if cached:
            import json
            emb = json.loads(cached)
        else:
            emb = model.encode([text])[0].tolist()
            redis_client.setex(cache_key, 86400, json.dumps(emb))  # cache for 24h
        embeddings.append(emb)
    
    return EmbeddingResponse(embeddings=embeddings)

@router.post("/resume/{resume_id}")
async def embed_resume(
    resume_id: str,
    resume_text: str,
    redis_client = Depends(get_redis)
):
    model = get_embedding_model()
    embedding = model.encode([resume_text])[0]
    # Store as binary for FAISS
    redis_client.set(f"emb:resume:{resume_id}", embedding.tobytes())
    return {"status": "success", "dimension": len(embedding)}