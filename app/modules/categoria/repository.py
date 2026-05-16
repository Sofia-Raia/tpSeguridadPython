from sqlmodel import Session, select
from typing import List
from app.core.repository import BaseRepository
from .models import Categoria


class CategoriaRepository(BaseRepository[Categoria]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Categoria)

    def get_roots(self, skip: int = 0, limit: int = 50) -> List[Categoria]:
        """Devuelve únicamente las categorías raíz (sin padre, no eliminadas)."""
        statement = (
            select(Categoria)
            .where(Categoria.parent_id.is_(None))  # type: ignore[union-attr]
            .where(Categoria.deleted_at.is_(None))  # type: ignore[union-attr]
            .offset(skip)
            .limit(limit)
        )
        return self.session.exec(statement).all()

    def get_children(self, parent_id: int) -> List[Categoria]:
        """Devuelve los hijos directos de una categoría."""
        statement = (
            select(Categoria)
            .where(Categoria.parent_id == parent_id)
            .where(Categoria.deleted_at.is_(None))  # type: ignore[union-attr]
        )
        return self.session.exec(statement).all()

    def get_full_tree(self, skip: int = 0, limit: int = 50) -> List[Categoria]:
        """
        Devuelve las raíces con sus subcategorías cargadas recursivamente.
        Gracias a `lazy='selectin'` en el modelo, SQLAlchemy resuelve
        automáticamente los niveles de profundidad.
        """
        return self.get_roots(skip, limit)
