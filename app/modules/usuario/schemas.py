from pydantic import BaseModel, EmailStr, Field

# Esquema base con datos comunes
class UsuarioBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    full_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr

# Datos necesarios para registrarse
class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=8, description="La contraseña debe tener al menos 8 caracteres")

# Datos que devolvemos a la API (Filtro de seguridad: ¡No viaja la password!)
class UsuarioPublic(UsuarioBase):
    id: int
    role: str
    disabled: bool

    class Config:
        from_attributes = True