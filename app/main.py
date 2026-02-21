from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine, Base
from app.routers import items, admin

# ¡ESTA LÍNEA ES LA CLAVE!
# Importamos models para que ItemDB se registre en Base.metadata
from app import models 

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ahora Base.metadata sí contiene 'items'
    #async with engine.begin() as conn:
    #    await conn.run_sync(Base.metadata.create_all)
    #yield
    # Ya NO usamos Base.metadata.create_all
    # Aquí en el futuro puedes poner lógica como cargar caché en Redis
    yield
app = FastAPI(lifespan=lifespan)

# Prefix: Todas las rutas de items empezarán con /items
app.include_router(items.router, prefix="/items", tags=["items"])

# Prefix: Todas las de admin con /admin
app.include_router(admin.router, prefix="/admin", tags=["admin"])

@app.get("/")
async def root():
    return {"message": "API Hot Update Corriendo"}