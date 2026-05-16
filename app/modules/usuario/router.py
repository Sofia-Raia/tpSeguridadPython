from fastapi import APIRouter, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from app.modules.usuario.schemas import UsuarioCreate, UsuarioPublic
from app.modules.usuario.service import UsuarioService
from app.core.unit_of_work import UnitOfWork, get_uow  # <- Añadimos get_uow
from app.core.security import verify_password, create_access_token
from app.core.deps import get_current_user
from app.modules.usuario.models import UsuarioModel

router = APIRouter(prefix="/auth", tags=["Autenticación"])

# <- Quitamos el tipado : UnitOfWork para evitar el error de Pydantic
def get_usuario_service(uow = Depends(get_uow)):
    return UsuarioService(uow)

# ─────────────────────────────────────────────────────────────────────────────
# REGISTRO
# ─────────────────────────────────────────────────────────────────────────────
@router.post("/register", response_model=UsuarioPublic, status_code=status.HTTP_201_CREATED)
def registrar(usuario_in: UsuarioCreate, service: UsuarioService = Depends(get_usuario_service)):
    """
    Registra un nuevo usuario en el sistema.
    La contraseña se almacena hasheada (bcrypt).
    """
    return service.registrar_usuario(usuario_in)

# ─────────────────────────────────────────────────────────────────────────────
# LOGIN (Emisión de Token en Cookie HttpOnly)
# ─────────────────────────────────────────────────────────────────────────────
@router.post("/token")
def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    uow = Depends(get_uow)  # <- Quitamos el tipado : UnitOfWork y usamos get_uow
):
    """
    Endpoint de Login estándar de OAuth2.
    Verifica las credenciales y guarda el JWT en una Cookie HttpOnly segura.
    """
    from fastapi import HTTPException
    
    # 1. Buscar el usuario por username usando el UOW
    with uow:
        usuario = uow.usuarios.get_by_username(form_data.username)
        
    # 2. Defensa frente a ataques de enumeración (Mensaje genérico si no existe o clave errónea)
    if not usuario or not verify_password(form_data.password, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
        
    # 3. Validar si la cuenta no está desactivada
    if usuario.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cuenta de usuario desactivada"
        )
        
    # 4. Crear el payload con los claims del usuario (incluyendo su rol)
    token_data = {
        "sub": usuario.username,
        "role": usuario.role
    }
    token_de_acceso = create_access_token(data=token_data)
    
    # 5. Inyectar el token en las Cookies de la respuesta HTTP
    # HttpOnly=True evita que scripts maliciosos de JS roben el token (Defensa contra XSS)
    response.set_cookie(
        key="access_token",
        value=token_de_acceso,
        httponly=True,
        max_age=1800,  # 30 minutos en segundos
        expires=1800,
        samesite="lax",
        secure=False  # Cambiar a True cuando uses HTTPS en producción
    )
    
    return {"message": "Inicio de sesión exitoso", "token_type": "bearer"}

# ─────────────────────────────────────────────────────────────────────────────
# RUTA PROTEGIDA DE PRUEBA (/me)
# ─────────────────────────────────────────────────────────────────────────────
@router.get("/me", response_model=UsuarioPublic)
def obtener_perfil_actual(current_user: UsuarioModel = Depends(get_current_user)):
    """
    Retorna los datos públicos del usuario autenticado leyendo su cookie.
    """
    return current_user