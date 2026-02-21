from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.database import get_db
from app.models import ItemDB
from app.schemas import ItemCreate, ItemRead # <-- Tus esquemas

router = APIRouter()

# GET ONE: Obtener un solo item por ID
@router.get("/{item_id}", response_model=ItemRead)
async def read_item(item_id: int, db: AsyncSession = Depends(get_db)):
    # 1. Query con filtro WHERE
    # Usamos scalar_one_or_none() que es más seguro y moderno que .first()
    result = await db.execute(select(ItemDB).where(ItemDB.id == item_id))
    item = result.scalar_one_or_none()
    
    # 2. Manejo de Error 404
    if item is None:
        raise HTTPException(status_code=404, detail="Item no encontrado")
        
    return item

# GET: Usamos ItemRead para serializar (incluye ID)
@router.get("/", response_model=List[ItemRead])
async def read_items(db: AsyncSession = Depends(get_db)):
    # Select asíncrono estilo SQLAlchemy 2.0
    result = await db.execute(select(ItemDB))
    return result.scalars().all()

# POST: Recibimos ItemCreate (sin ID), devolvemos ItemRead (con ID generado)
@router.post("/", response_model=ItemRead)
async def create_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    # 1. Convertir DTO (Pydantic) a Entidad (SQLAlchemy)
    db_item = ItemDB(**item.model_dump())
    
    # 2. Guardar en DB
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item) # Recuperamos el ID generado por SQLite
    
    return db_item