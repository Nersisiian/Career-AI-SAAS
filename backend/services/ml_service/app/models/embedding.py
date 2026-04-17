from pydantic import BaseModel
from typing import List, Optional

class JobEmbedding(BaseModel):
    job_id: str
    embedding: List[float]
    text_used: Optional[str] = None