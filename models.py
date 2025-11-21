# models.py
# ---------------------------------------------
# Define el modelo de la base de datos (tabla "usuarios")
# usando SQLAlchemy ORM.
# ---------------------------------------------

from sqlalchemy import Column, Integer, String
from database import Base

# Modelo de usuario
class Usuario(Base):
    __tablename__ = "usuarios"  # Nombre de la tabla en la BD

    # Columnas
    id = Column(Integer, primary_key=True, index=True)  # Clave primaria
    nombre = Column(String, index=True)                 # Nombre del usuario
    email = Column(String, unique=True, index=True)     # Email único
