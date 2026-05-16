from sqlmodel import SQLModel, Field

class UsuarioModel(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: int | None = Field(default=None, primary_key=True, index=True)
    username: str = Field(index=True, unique=True, nullable=False, max_length=50)
    full_name: str = Field(nullable=False, max_length=100)
    email: str = Field(index=True, unique=True, nullable=False, max_length=100)
    hashed_password: str = Field(nullable=False, max_length=255)
    role: str = Field(default="user", nullable=False, max_length=20)  # "user" o "admin"
    disabled: bool = Field(default=False, nullable=False)