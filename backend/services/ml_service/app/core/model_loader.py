from sentence_transformers import SentenceTransformer
from app.core.config import settings

_embedding_model = None

def load_models():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)

def get_embedding_model():
    if _embedding_model is None:
        load_models()
    return _embedding_model