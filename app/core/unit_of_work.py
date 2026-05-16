from sqlmodel import Session
from app.modules.usuario.repository import UsuarioRepository
from app.core.database import get_session  # <- Asegurate de que tu archivo database.py tenga get_session o la sesión de SQLModel
from fastapi import Depends

class UnitOfWork:
    def __init__(self, session: Session) -> None:
        self._session = session
        # Registramos el repositorio de usuarios pasándole la sesión interna
        self.usuarios = UsuarioRepository(self._session)

    def __enter__(self) -> "UnitOfWork":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is None:
            self._session.commit()
        else:
            self._session.rollback()

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()


def get_uow(session = Depends(get_session)):
    return UnitOfWork(session)