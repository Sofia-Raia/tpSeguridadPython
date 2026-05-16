from sqlmodel import Session, select
from typing import Optional, Sequence
from app.core.repository import BaseRepository
from .models import Producto

class ProductoRepository(BaseRepository[Producto]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Producto)

    # REQUERIMIENTO DEL PARCIAL: Filtros personalizados y borrado lógico
    def get_all_active(self, offset: int = 0, limit: int = 50, nombre: Optional[str] = None) -> Sequence[Producto]:
        statement = select(self.model).where(self.model.deleted_at is None)
        if nombre:
            statement = statement.where(self.model.nombre.contains(nombre)) # type: ignore
        return self.session.exec(statement.offset(offset).limit(limit)).all()