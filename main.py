from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List
import asyncio
# 1. Definimos la dependencia (es solo una función)
async def verify_token(token: str | None = None):
    if token != "supersecreto":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o ausente"
        )
    return True

app = FastAPI()

# 2. Inyectamos la dependencia en un endpoint nuevo
@app.get("/items/admin/")
async def read_admin_items(authorized: bool = Depends(verify_token)):
    # Si llega aquí, es porque verify_token pasó sin errores.
    # El valor de retorno de verify_token se guarda en 'authorized'
    return {"message": "Bienvenido Admin", "data": inventory}

# 1. Reutilizamos tu conocimiento de Pydantic
class Item(BaseModel):
    id: int
    name: str
    price: float = Field(gt=0, description="El precio debe ser positivo")
    is_offer: bool = False

# Base de datos simulada en memoria
inventory = []

# 2. Endpoint Síncrono (Bloqueante - Evitar si hay I/O)
@app.get("/")
def read_root():
    return {"message": "Bienvenido a mi API de Inventario"}

# 3. Endpoint Asíncrono (Non-blocking)
# Simula una escritura lenta en DB
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    # Simulamos latencia de red/disco de 1 segundo
    await asyncio.sleep(1) 
    inventory.append(item)
    return item

# 4. Endpoint Asíncrono para leer
@app.get("/items/", response_model=List[Item])
async def read_items():
    # Simulamos otra latencia
    await asyncio.sleep(0.5)
    return inventory