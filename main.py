from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Definir la aplicación FastAPI
app = FastAPI()

# Configuración de la base de datos
MYSQL_HOST = "mysql"
MYSQL_PORT = "3306"
MYSQL_USER = "adsa"
MYSQL_PASSWORD = "2006"
MYSQL_DB = "test_db"

# Crear la cadena de conexión
DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

# Crear el motor de SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)

# Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear la base de datos declarativa
Base = declarative_base()

# Definir el modelo para la tabla `items`
class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(String(255))

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Modelo para recibir datos en las peticiones
class ItemCreate(BaseModel):
    name: str
    description: str

# Ruta para obtener todos los items
@app.get("/getAllItems/")
def get_items():
    db = SessionLocal()
    items = db.query(Item).all()
    db.close()
    return items

# Ruta para crear un nuevo item
@app.post("/addItem/")
def create_item(item: ItemCreate):
    db = SessionLocal()
    new_item = Item(name=item.name, description=item.description)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    db.close()
    return new_item
