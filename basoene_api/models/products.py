from sqlmodel import Field, SQLModel, create_engine
from typing import Optional
from datetime import datetime, date


DB = "basoene.sqlite3"
engine = create_engine(f"sqlite:///{DB}", echo=True, connect_args={"check_same_thread": False})

class Products(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_name: str = Field(index=True)
    product_category: str
    unit_price: int
    quantity: int


class ProductSales(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sale_date: date = Field(default_factory=date.today, nullable=False)
    time: datetime = Field(default_factory=datetime.now, nullable=False)
    quantity: int
    product_id: int = Field(foreign_key="products.id")


def create_tables() -> None:
    SQLModel.metadata.create_all(engine)