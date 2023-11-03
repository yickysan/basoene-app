from sqlmodel import Field, SQLModel, create_engine
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


DB = "rooms.sqlite3"
engine = create_engine(f"sqlite:///{DB}", echo=True, connect_args={"check_same_thread": False})

class Rooms(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    room_name: str = Field(index=True)
    room_type: str
    price_short: int 
    price_full: int 


class Bookings(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    booking_date: date = Field(default_factory=date.today, nullable=False)
    time: datetime = Field(default_factory=datetime.now, nullable=False)
    customer_name = str
    booking_type: str
    room_id: int = Field(foreign_key="products.id")


class RoomsAdd(BaseModel):
    room_name: str 
    room_type: str
    price_short: int
    price_full: int


class BookRoom(BaseModel):
    customer_name = str
    booking_type: str
    room_id: int





def create_tables() -> None:
    Rooms.__table__.create(engine)
    Bookings.__table__.create(engine)