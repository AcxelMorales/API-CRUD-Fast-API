# schemas.py
# ---------------------------------------------
# Define los modelos de datos (entrada y salida)
# para las peticiones y respuestas del API.
# ---------------------------------------------

from pydantic import BaseModel

# Modelo base con campos comunes
class UsuarioBase(BaseModel):
    nombre: str
    email: str


# Modelo para crear usuarios (entrada)
class UsuarioCreate(UsuarioBase):
    pass  # No agrega campos nuevos, hereda de UsuarioBase


# Modelo para retornar usuarios (salida)
class Usuario(UsuarioBase):
    id: int  # Incluye el ID generado por la BD

    # 🔥 Pydantic v2: reemplazo de orm_mode
    model_config = {
        "from_attributes": True
    }
