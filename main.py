from fastapi import FastAPI
import mysql.connector
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Configuración de la base de datos
MYSQL_HOST = "mysql"
MYSQL_PORT = 3306
MYSQL_USER = "adsa"
MYSQL_PASSWORD = "2006"
MYSQL_DB = "test_db"

# Definir el modelo de los usuarios
class User(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

# Función para conectar a la base de datos
def get_db_connection():
    connection = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )
    return connection

@app.get("/users", response_model=List[User])
def get_users():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return users

# Ruta para ver un mensaje
@app.get("/")
def read_root():
    return {"message": "¡Hola Mundo! Este es un ejemplo de FastAPI con Docker."}
