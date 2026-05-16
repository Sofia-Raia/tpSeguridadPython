from fastapi import Depends, HTTPException, status, Request
from jose import jwt
from app.core.config import settings
from app.core.security import decode_access_token
from app.core.unit_of_work import get_uow  # <- Cambiado para usar la función proveedora
from app.modules.usuario.models import UsuarioModel

# ─────────────────────────────────────────────────────────────────────────────
# EXTRAER TOKEN DESDE COOKIES
# ─────────────────────────────────────────────────────────────────────────────
def get_token_from_cookie(request: Request) -> str:
    """
    Dependencia que extrae el JWT directamente de las cookies de la petición.
    Si no encuentra la cookie 'access_token', frena con un 401.
    """
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado. Inicie sesión para obtener una cookie de acceso."
        )
    return token

# ─────────────────────────────────────────────────────────────────────────────
# AUTENTICACIÓN: OBTENER USUARIO ACTUAL
# ─────────────────────────────────────────────────────────────────────────────
def get_current_user(
    token: str = Depends(get_token_from_cookie),
    uow = Depends(get_uow)  # <- Cambiado: Quitamos el tipado : UnitOfWork y usamos get_uow
) -> UsuarioModel:
    """
    Valida el token extraído. Si es válido, carga al usuario desde MySQL
    usando el Unit of Work.
    """
    # 1. Decodificar y validar criptográficamente el JWT
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas o sesión expirada"
        )
    
    # 2. Extraer el subject (username) del payload
    username: str = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token malformado: falta el identificador de usuario"
        )
    
    # 3. Buscar el usuario en la base de datos a través del UOW
    with uow:
        usuario = uow.usuarios.get_by_username(username)
        
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El usuario asociado a este token ya no existe"
        )
        
    # 4. Verificar que la cuenta no esté inhabilitada
    if usuario.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cuenta de usuario desactivada"
        )
        
    return usuario

# ─────────────────────────────────────────────────────────────────────────────
# AUTORIZACIÓN: CONTROL DE ACCESO POR ROLES (RBAC)
# ─────────────────────────────────────────────────────────────────────────────
class RoleChecker:
    """
    Permite restringir endpoints según una lista de roles permitidos.
    Uso: Depends(RoleChecker(["admin"]))
    """
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: UsuarioModel = Depends(get_current_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permisos insuficientes. Se requiere uno de los siguientes roles: {self.allowed_roles}"
            )
        return current_user