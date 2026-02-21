from typing import Optional
from pydantic import BaseModel, Field, EmailStr, field_validator

class Subscription(BaseModel):
    plan_name: str
    price: float= Field(gt=0)

class User(BaseModel):
    username: str
    email: EmailStr
    age: int = Field(ge=18, le=120)
    subscription: Subscription | None = None
    is_active: bool = True
    @field_validator("username")
    @classmethod
    def no_admin(cls, v: str) -> str:
        if "admin" in v.lower():
            raise ValueError('username no debe contener "admin"')
        return v

# Uso
sub = Subscription(plan_name="Pro", price=29.99)
user = User(username="DevSenior", email="dev@example.com", age=18, subscription=sub)

print(user.model_dump())     # Reemplaza to_dict()
print(user.model_dump_json())# JSON automático