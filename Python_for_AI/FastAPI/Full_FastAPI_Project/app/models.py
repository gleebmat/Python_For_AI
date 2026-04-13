from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal
from sqlalchemy import Numeric


class Wallet(Base):
    __tablename__ = "wallet"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    balance: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))
