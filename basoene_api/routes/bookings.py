from fastapi import APIRouter
from fastapi import Response, Depends, HTTPException
from sqlmodel import Session, select
from typing import Generator
from datetime import date
from basoene_api.models.rooms import Bookings, Rooms, BookRoom, engine
from basoene_api.routes.rooms import get_session

router = APIRouter()

@router.get("/bookings")
async def bookings(session: Session = Depends(get_session)):
    
    query = (select(Bookings,Rooms.room_name, Rooms.price_short, Rooms.price_full)
            .where(Bookings.room_id == Rooms.id))
    result = session.exec(query).all()
    return result


@router.get("/bookings/today")
async def get_todays_bookings(session: Session = Depends(get_session)):

    bookings = session.exec(
        (select(Bookings, Rooms.room_name, Rooms.price_short, Rooms.price_full)
         .where(Bookings.booking_date == date.today())
         .where(Bookings.room_id == Rooms.id)
         .order_by(Bookings.time.desc())
        )
    ).all()

    if len(bookings) < 1:
        raise HTTPException(status_code=404, headers={"message": "No room has been booked today"})
    
    return bookings


@router.get("/bookings/{date}")
async def get_bookings(date: str, response: Response, session: Session = Depends(get_session)):

    bookings = session.exec(
        (select(Bookings, Rooms.room_name, Rooms.price_short, Rooms.price_full)
         .where(Bookings.booking_date == date)
         .where(Bookings.room_id == Rooms.id)
        )
    ).all()

    if len(bookings) < 1:
        raise HTTPException(status_code=404, headers={"message": "No room has been booked today"})
    
    return bookings




   
@router.post("/bookings", response_model = Bookings)
async def book_room(booking: BookRoom, session: Session = Depends(get_session)):
    db_booking = Bookings.from_orm(booking)
    session.add(db_booking)
    session.commit()
    session.refresh(db_booking)

    return booking