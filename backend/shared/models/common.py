from pydantic import BaseModel
from typing import TypeVar, Generic, Optional, List
from uuid import UUID

T = TypeVar('T')

class StandardResponse(BaseModel, Generic[T]):
    status: str = "success"
    message: Optional[str] = None
    data: Optional[T] = None

class ErrorResponse(BaseModel):
    status: str = "error"
    code: str
    message: str
    details: Optional[dict] = None

class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 20

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int