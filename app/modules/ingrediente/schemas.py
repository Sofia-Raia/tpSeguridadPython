from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class IngredienteBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    descripcion: Optional[str] = None
    es_alergeno: bool = False

class IngredienteCreate(IngredienteBase): pass  # noqa: E701

class IngredienteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    es_alergeno: Optional[bool] = None

class IngredienteRead(IngredienteBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config: from_attributes = True  # noqa: E701
