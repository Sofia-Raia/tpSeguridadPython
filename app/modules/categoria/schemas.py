from pydantic import BaseModel, Field
from typing import Optional, Generic, TypeVar, List
from datetime import datetime

T = TypeVar("T")


class RespuestaEstandar(BaseModel, Generic[T]):
    message: str
    data: T


# ── Schemas base ──────────────────────────────────────────────────────────────

class CategoriaBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None


# ── Create / Update ───────────────────────────────────────────────────────────

class CategoriaCreate(CategoriaBase):
    """Para crear una categoría. `parent_id=None` implica que es raíz."""
    parent_id: Optional[int] = Field(default=None, gt=0)


class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None
    parent_id: Optional[int] = Field(default=None, gt=0)


# ── Read (plano, sin hijos) ───────────────────────────────────────────────────

class CategoriaRead(CategoriaBase):
    """Vista plana: útil para listados donde no necesitamos el árbol completo."""
    id: int
    parent_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ── Read con árbol recursivo ──────────────────────────────────────────────────

class CategoriaTree(CategoriaBase):
    """
    Vista recursiva: cada nodo incluye su lista de hijos (subcategorias),
    que a su vez pueden tener los suyos. Ideal para devolver el árbol completo.
    """
    id: int
    parent_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    subcategorias: List["CategoriaTree"] = []

    class Config:
        from_attributes = True


# Necesario para que Pydantic resuelva la auto-referencia
CategoriaTree.model_rebuild()
