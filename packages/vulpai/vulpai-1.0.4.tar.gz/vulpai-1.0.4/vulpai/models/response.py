from dataclasses import dataclass
from typing import TypeVar, Generic, List, Optional, Dict, Any

T = TypeVar('T')


@dataclass
class APIResponse(Generic[T]):
    """Resposta genérica da API"""
    
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    
    @property
    def is_error(self) -> bool:
        return not self.success


@dataclass
class PaginatedResponse(Generic[T]):
    """Resposta paginada da API"""
    
    items: List[T]
    total: int
    page: int
    page_size: int
    
    @property
    def total_pages(self) -> int:
        return (self.total + self.page_size - 1) // self.page_size
    
    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages
    
    @property
    def has_previous(self) -> bool:
        return self.page > 1