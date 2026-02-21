from fastapi import APIRouter, Depends
from app.dependencies import verify_token # Importamos la dependencia

router = APIRouter()

@router.get("/", dependencies=[Depends(verify_token)])
async def admin_dashboard():
    return {"message": "Panel de Control Secreto"}