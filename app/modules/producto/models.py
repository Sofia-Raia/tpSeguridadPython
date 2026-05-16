from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import Column, ForeignKey, Integer, JSON
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime, timezone

# Evitamos importaciones circulares para los tipados (List["..."])
if TYPE_CHECKING:
    from app.modules.categoria.models import Categoria
    from app.modules.ingrediente.models import Ingrediente

# ─────────────────────────────────────────────────────────────────────────────
# Tabla de enlace N:M  →  Producto ↔ Categoria
# ─────────────────────────────────────────────────────────────────────────────
class ProductoCategoriaLink(SQLModel, table=True):
    __tablename__ = "producto_categoria" # type: ignore

    producto_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("productos.id", ondelete="CASCADE"),
            primary_key=True,
            nullable=False,
        )
    )
    categoria_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("categorias.id", ondelete="CASCADE"),
            primary_key=True,
            nullable=False,
        )
    )
    es_principal: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# ─────────────────────────────────────────────────────────────────────────────
# Tabla de enlace N:M  →  Producto ↔ Ingrediente
# ─────────────────────────────────────────────────────────────────────────────
class ProductoIngredienteLink(SQLModel, table=True):
    __tablename__ = "producto_ingrediente" # type: ignore
    
    producto_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("productos.id", ondelete="CASCADE"),
            primary_key=True,
            nullable=False,
        )
    )
    ingrediente_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("ingredientes.id", ondelete="CASCADE"),
            primary_key=True,
            nullable=False,
        )
    )
    es_removible: bool = Field(default=False)


# ─────────────────────────────────────────────────────────────────────────────
# Producto
# ─────────────────────────────────────────────────────────────────────────────
class Producto(SQLModel, table=True):
    __tablename__ = "productos" # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=150)
    descripcion: Optional[str] = Field(default=None)
    precio_base: float
    
    imagen_url: list[str] = Field(default=[], sa_column=Column(JSON))
    stock_cantidad: int = Field(default=0, ge=0)
    disponible: bool = Field(default=True)

    # Auditoría
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[datetime] = Field(default=None)

    # ── Relaciones N:M ────────────────────────────────────────────────────────
    categorias: List["Categoria"] = Relationship(
        back_populates="productos",
        link_model=ProductoCategoriaLink,
    )
    
    # Acá usamos "Ingrediente" entre comillas y la clase ProductoIngredienteLink sin comillas
    ingredientes: List["Ingrediente"] = Relationship(
        back_populates="productos",
        link_model=ProductoIngredienteLink,
    )