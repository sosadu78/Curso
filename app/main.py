import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine, Base
from app.routers import items, admin

# ¡ESTA LÍNEA ES LA CLAVE!
# Importamos models para que ItemDB se registre en Base.metadata
from app import models 

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
is_production = ENVIRONMENT == "production"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ahora Base.metadata sí contiene 'items'
    #async with engine.begin() as conn:
    #    await conn.run_sync(Base.metadata.create_all)
    #yield
    # Ya NO usamos Base.metadata.create_all
    # Aquí en el futuro puedes poner lógica como cargar caché en Redis
    yield
#app = FastAPI(lifespan=lifespan)
app = FastAPI(
    lifespan=lifespan,
    root_path="/curso",
    #Si es producción, asignamos None para apagar la ruta. Si no, usamos las rutas por defecto.
    docs_url=None if is_production else "/docs",
    redoc_url=None if is_production else "/redoc",
    openapi_url=None if is_production else "/openapi.json"
)
# Prefix: Todas las rutas de items empezarán con /items
app.include_router(items.router, prefix="/items", tags=["items"])

# Prefix: Todas las de admin con /admin
app.include_router(admin.router, prefix="/admin", tags=["admin"])

@app.get("/")
async def root():
    return {"message": "API Hot Update Corriendo"}

@app.get("/enviroment")
async def root():
    return {"enviroment": ENVIRONMENT}