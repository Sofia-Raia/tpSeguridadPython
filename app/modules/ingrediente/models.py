from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime, timezone

# 1. Importamos la tabla intermedia de forma real acá arriba (esto NO rompe nada)
from app.modules.producto.models import ProductoIngredienteLink

# 2. Dejamos solo a Producto en el TYPE_CHECKING
if TYPE_CHECKING:
    from app.modules.producto.models import Producto

class Ingrediente(SQLModel, table=True):
    __tablename__ = "ingredientes" # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100, unique=True)
    descripcion: Optional[str] = Field(default=None)
    es_alergeno: bool = Field(default=False)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # 3. Le pasamos la CLASE a link_model, ¡sin comillas!
    productos: List["Producto"] = Relationship(
        back_populates="ingredientes",
        link_model=ProductoIngredienteLink
    )