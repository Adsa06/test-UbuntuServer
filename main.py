from fastapi import FastAPI
import mysql.connector
from pydantic import BaseModel

# Inicializamos FastAPI
app = FastAPI()

# Conexión a la base de datos MySQL
def get_db_connection():
    connection = mysql.connector.connect(
        host="mysql",  # Nombre del servicio de MySQL en docker-compose.yml
        user="user",   # Usuario de la base de datos
        password="userpassword",  # Contraseña de la base de datos
        database="test_db"  # Nombre de la base de datos
    )
    return connection

# Definir un modelo de datos para la API
class Item(BaseModel):
    name: str
    description: str

# Ruta para ver un mensaje
@app.get("/")
def read_root():
    return {"message": "¡Hola Mundo! Este es un ejemplo de FastAPI con Docker."}

# Ruta para obtener datos desde la base de datos MySQL
@app.get("/items/{item_id}")
def get_item(item_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
    item = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if item is None:
        return {"message": "Item no encontrado"}
    return item

# Ruta para agregar un nuevo item a la base de datos
@app.post("/items/")
def create_item(item: Item):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, description) VALUES (%s, %s)", (item.name, item.description))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Item creado correctamente"}
