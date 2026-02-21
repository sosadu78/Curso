from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column

class ItemDB(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    price: Mapped[float]
    is_offer: Mapped[bool] = mapped_column(default=False)
    # Le decimos a Postgres que ponga un 0 en los registros existentes
    stock: Mapped[int] = mapped_column(server_default="0")