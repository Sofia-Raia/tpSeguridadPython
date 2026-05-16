from fastapi import HTTPException, status
from app.modules.usuario.schemas import UsuarioCreate
from app.modules.usuario.models import UsuarioModel
from app.core.security import hash_password  # Lo crearemos en core/security.py

class UsuarioService:
    def __init__(self, uow):
        self.uow = uow

    def registrar_usuario(self, usuario_in: UsuarioCreate) -> UsuarioModel:
        with self.uow:
            # 1. Validar que el username no exista
            if self.uow.usuarios.get_by_username(usuario_in.username):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="El nombre de usuario ya está en uso"
                )
            
            # 2. Validar que el email no exista
            if self.uow.usuarios.get_by_email(usuario_in.email):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="El email ya está registrado"
                )

            # 3. Hachear la contraseña (Seguridad de datos en reposo)
            password_hasheada = hash_password(usuario_in.password)

            # 4. Crear modelo e insertar
            nuevo_usuario = UsuarioModel(
                username=usuario_in.username,
                full_name=usuario_in.full_name,
                email=usuario_in.email,
                hashed_password=password_hasheada,
                role="user"  # Por defecto siempre es user
            )
            
            self.uow.usuarios.add(nuevo_usuario)
            self.uow.commit()
            return nuevo_usuario