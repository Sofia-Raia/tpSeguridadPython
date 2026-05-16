from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from app.modules.categoria.schemas import CategoriaRead

class ProductoBase(BaseModel):
    nombre: str = Field(..., max_length=150)
    descripcion: Optional[str] = None
    precio_base: float = Field(gt=0)
    imagen_url: List[str] = Field(default=[])
    stock_cantidad: int = Field(default=0, ge=0)
    disponible: bool = True

class ProductoCreate(ProductoBase):
    categoria_ids: List[int] = Field(..., min_length=1)  # ← obligatorio, al menos 1
    ingrediente_ids: List[int] = []

    @field_validator("categoria_ids")
    @classmethod
    def categorias_no_vacias(cls, v):
        if not v:
            raise ValueError("Debe asignar al menos una categoría al producto")
        return v

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=150)
    descripcion: Optional[str] = None
    precio_base: Optional[float] = Field(None, gt=0)
    stock_cantidad: Optional[int] = Field(None, ge=0)
    disponible: Optional[bool] = None
    categoria_ids: Optional[List[int]] = None
    ingrediente_ids: Optional[List[int]] = None

    @field_validator("categoria_ids")
    @classmethod
    def categorias_no_vacias_en_update(cls, v):
        # Si se envía, no puede ser lista vacía
        if v is not None and len(v) == 0:
            raise ValueError("Si se envía categoria_ids, debe contener al menos una categoría")
        return v

class ProductoRead(ProductoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    categorias: List[CategoriaRead] = []   # ← nuevo
    class Config:
        from_attributes = True