from fastapi import APIRouter
from fastapi import Response, Depends, HTTPException
from sqlmodel import Session, select
from typing import Generator
from datetime import date
from basoene_api.models.rooms import Bookings, Rooms, BookRoom
from basoene_api.db.bookings import(
    db_bookings,
    db_book_room,
    db_get_todays_bookings,
    db_get_bookings,
    NoBookingsError
)
from basoene_api.routes.rooms import get_session

router = APIRouter()

@router.get("/bookings")
async def bookings(session: Session = Depends(get_session)):
    return db_bookings(session)


@router.get("/bookings/today")
async def get_todays_bookings(session: Session = Depends(get_session)):

    try:
        return db_get_todays_bookings(session)

    except NoBookingsError:
        raise HTTPException(status_code=404, headers={"message": "No room has been booked today"})
    


@router.get("/bookings/{date}")
async def get_bookings(date: str, response: Response, session: Session = Depends(get_session)):

    try:
        return db_get_bookings(date, session)

    except NoBookingsError:
        raise HTTPException(status_code=404, headers={"message": "No was booked on this day"})




   
@router.post("/bookings", response_model = Bookings)
async def book_room(booking: BookRoom, session: Session = Depends(get_session)):

    return db_book_room(booking, session)