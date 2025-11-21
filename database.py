# database.py
# ---------------------------------------------
# Configura la conexión a la base de datos SQLite
# y define la sesión de SQLAlchemy para interactuar con ella.
# ---------------------------------------------

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de la base de datos (en este caso SQLite local)
SQLALCHEMY_DATABASE_URL = "sqlite:///./usuarios.db"

# Crea el motor que maneja la conexión
# "check_same_thread=False" es necesario para SQLite cuando se usa con FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Crea una fábrica de sesiones para conectarse a la BD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base de donde heredarán todos los modelos (tablas)
Base = declarative_base()
