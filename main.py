# main.py
# ---------------------------------------------
# API REST CRUD con FastAPI y SQLite
# Incluye endpoints para crear, leer, actualizar y eliminar usuarios.
# ---------------------------------------------

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal

USUARIO_NO_ENCONTRADO = 'Usuario no encontrado'

# Crea las tablas en la base de datos (si no existen)
models.Base.metadata.create_all(bind=engine)

# Inicializa la aplicación FastAPI
app = FastAPI(title="CRUD con FastAPI y SQLite")

# ---------------------------------------------
# DEPENDENCIA DE BASE DE DATOS
# ---------------------------------------------
def get_db():
    """
    Crea una sesión de base de datos para cada request.
    Usa 'yield' para devolver la sesión al endpoint,
    y luego asegura su cierre con el bloque 'finally'.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------------------------
# ENDPOINTS DEL CRUD
# ---------------------------------------------

# 🧩 Crear un nuevo usuario
@app.post("/usuarios/", response_model=schemas.Usuario)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    """
    Crea un usuario en la base de datos.
    - Recibe un objeto JSON con 'nombre' y 'email'.
    - Devuelve el usuario creado con su 'id'.
    """
    db_usuario = models.Usuario(nombre=usuario.nombre, email=usuario.email)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# 📋 Listar todos los usuarios
@app.get("/usuarios/", response_model=list[schemas.Usuario])
def listar_usuarios(db: Session = Depends(get_db)):
    """
    Retorna una lista con todos los usuarios registrados.
    """
    return db.query(models.Usuario).all()

# 🔍 Obtener un usuario por su ID
@app.get("/usuarios/{usuario_id}", response_model=schemas.Usuario)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """
    Busca y devuelve un usuario específico por ID.
    Si no existe, lanza un error 404.
    """
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail=USUARIO_NO_ENCONTRADO)
    return usuario

# ✏️ Actualizar un usuario existente
@app.put("/usuarios/{usuario_id}", response_model=schemas.Usuario)
def actualizar_usuario(usuario_id: int, datos: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un usuario existente.
    - Recibe el ID en la URL y el cuerpo con los nuevos datos.
    - Si el usuario no existe, devuelve error 404.
    """
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail=USUARIO_NO_ENCONTRADO)

    usuario.nombre = datos.nombre
    usuario.email = datos.email
    db.commit()
    db.refresh(usuario)
    return usuario

# 🗑️ Eliminar un usuario por ID
@app.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """
    Elimina un usuario existente de la base de datos.
    Devuelve un mensaje de confirmación.
    """
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail=USUARIO_NO_ENCONTRADO)

    db.delete(usuario)
    db.commit()
    return {"mensaje": "Usuario eliminado correctamente"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
