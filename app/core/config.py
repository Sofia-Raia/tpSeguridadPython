from pydantic_settings import BaseSettings
from pydantic import computed_field

class Settings(BaseSettings):
    # Variables por defecto para MySQL
    mysql_user: str = "root"
    mysql_password: str = "" 
    mysql_db: str = "tp2_db" 
    mysql_host: str = "localhost"
    mysql_port: int = 3306

    # ─────────────────────────────────────────────────────────────────────────────
    # Configuración de Seguridad y JWT
    # ─────────────────────────────────────────────────────────────────────────────
    # IMPORTANTE: En producción, cambia esta clave por una secreta generada al azar
    SECRET_KEY: str = "super_secreta_y_segura_para_el_proyecto_integrador_2026_jwt"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        # URL de conexión para MySQL usando pymysql
        return (
            f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_db}"
        )

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }

settings = Settings()