from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.modules.producto.models import ProductoCategoriaLink

if TYPE_CHECKING:
    from app.modules.producto.models import Producto


class Categoria(SQLModel, table=True):
    __tablename__ = "categorias"

    id: Optional[int] = Field(default=None, primary_key=True)
    parent_id: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, ForeignKey("categorias.id", ondelete="SET NULL"), nullable=True),
    )
    nombre: str = Field(index=True, max_length=100)
    descripcion: Optional[str] = Field(default=None)
    imagen_url: Optional[str] = Field(default=None)

    # --- Auditoría ---
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[datetime] = Field(default=None)

    # ── Relación N:M via ProductoCategoriaLink ────────────────────────────
    productos: List["Producto"] = Relationship(
        back_populates="categorias",
        link_model=ProductoCategoriaLink,
    )

    # ── Auto-referencia: padre e hijos ────────────────────────────────────
    # "remote_side=[id]" indica que `id` es el lado "uno" (el padre),
    # y `parent_id` es el lado "muchos" (los hijos). Así cada Categoria
    # apunta a su padre y expone una lista de sus subcategorías.
    subcategorias: List["Categoria"] = Relationship(
        sa_relationship=relationship(
            "Categoria",
            primaryjoin="Categoria.parent_id == Categoria.id",
            foreign_keys="[Categoria.parent_id]",
            back_populates="parent",
            lazy="selectin",          # carga recursiva automática
        )
    )

    parent: Optional["Categoria"] = Relationship(
        sa_relationship=relationship(
            "Categoria",
            primaryjoin="Categoria.id == Categoria.parent_id",
            foreign_keys="[Categoria.parent_id]",
            back_populates="subcategorias",
            remote_side="[Categoria.id]",
        )
    )
