from fastapi import HTTPException, status
async def verify_token(token: str | None = None):
    if token != "supersecreto":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o ausente"
        )
    return True