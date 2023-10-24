from fastapi import APIRouter
from fastapi import Response, Depends
from sqlmodel import Session, select
from typing import Generator
from basoene_api.models.rooms import Bookings, engine
from basoene_api.routes.rooms import get_session

router = APIRouter()

@router.get("/bookings", response_model = list[Bookings])
async def bookings(session: Session = Depends(get_session)):
    
    query = select(Bookings)
    result = session.exec(query).all()
    return result


@router.get("/rooms/{date}/", response_model = list[Bookings] | str)
async def get_booking(date: str, response: Response, session: Session = Depends(get_session)):

    rooms = session.exec(
        select(Bookings).where(Bookings.date == date)
    ).all()

    if len(rooms) < 1:
        response.status_code = 404
        return "Bookings not found"
    
    return rooms
    
@router.post("/bookings", response_model = Bookings)
async def add_room(booking: Bookings, session: Session = Depends(get_session)):
    session.add(booking)
    session.commit()
    session.refresh(booking)

    return booking