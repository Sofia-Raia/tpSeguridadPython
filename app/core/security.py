from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

# ─────────────────────────────────────────────────────────────────────────────
# 1. HASHING DE CONTRASEÑAS (Datos en Reposo)
# ─────────────────────────────────────────────────────────────────────────────

# Configuramos el contexto de hashing usando el algoritmo seguro Bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain_password: str) -> str:
    """
    Recibe una contraseña en texto plano y devuelve su hash irreversible.
    Bcrypt se encarga de generar y añadir el 'salt' de forma automática.
    """
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Compara de forma segura una contraseña en texto plano con el hash guardado.
    Es resistente a ataques de tiempo (timing-attacks).
    """
    return pwd_context.verify(plain_password, hashed_password)

# ─────────────────────────────────────────────────────────────────────────────
# 2. GENERACIÓN Y DECODIFICACIÓN DE JWT (Datos en Transporte)
# ─────────────────────────────────────────────────────────────────────────────

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Genera un JSON Web Token firmado digitalmente (HS256).
    """
    to_encode = data.copy()  # Copia defensiva para evitar mutaciones
    
    # Calculamos el tiempo de expiración usando hora UTC
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Añadimos los claims estándar del protocolo
    to_encode.update({
        "type": "access",  # Defensa: diferencia tokens de acceso de tokens de refresco
        "exp": expire      # Claim estándar de expiración
    })
    
    # Firmamos el token con nuestra clave secreta
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict | None:
    """
    Decodifica y valida un JWT.
    Verifica automáticamente: la firma válida, el algoritmo y que no esté expirado.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        # Filtro extra de seguridad: verificar el tipo de token
        if payload.get("type") != "access":
            return None
            
        return payload
        
    except JWTError:
        # Si la firma fue manipulada, expiró o el formato está roto, es inválido
        return None