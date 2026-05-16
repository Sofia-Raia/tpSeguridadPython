from sqlmodel import Session
from app.core.repository import BaseRepository  # <- Corregido a tu archivo real
from app.modules.usuario.models import UsuarioModel

class UsuarioRepository(BaseRepository[UsuarioModel]):
    def __init__(self, db: Session):
        super().__init__(db, UsuarioModel)

    def get_by_username(self, username: str) -> UsuarioModel | None:
        from sqlmodel import select
        query = select(UsuarioModel).where(UsuarioModel.username == username)
        return self.session.execute(query).scalar_one_or_none()

    def get_by_email(self, email: str) -> UsuarioModel | None:
        from sqlmodel import select
        query = select(UsuarioModel).where(UsuarioModel.email == email)
        return self.session.execute(query).scalar_one_or_none()