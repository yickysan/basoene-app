from fastapi import APIRouter
from fastapi import Response, Depends, HTTPException
from sqlmodel import Session, select, func, extract, case
from typing import Generator
from datetime import date
from basoene_api.models.rooms import Rooms, Bookings, engine
from basoene_api.models.room_analysis import DateResults, RoomResults, HourCount, DayResults, BookingSummary
from basoene_api.db.room_analytics import (
    db_room_analysis,
    db_trend_analysis,
    db_daily_analysis,
    db_hourly_analysis,
    db_summary_analysis
)

router = APIRouter()

def get_session() -> Generator[Session, None, None]:
    with Session(engine, autoflush=True) as session:
        yield session


@router.get("/analysis/room", response_model=list[RoomResults])
async def room_analysis(session: Session = Depends(get_session)):
    return db_room_analysis(session)


@router.get("/analysis/room/date", response_model=list[DateResults])
async def trend_analysis(session: Session = Depends(get_session)):
    return db_trend_analysis(session)



@router.get("/analysis/room/daily_revenue", response_model=list[DayResults])
async def daily_analysis(session: Session = Depends(get_session)):
     
    return db_daily_analysis(session)

    

@router.get("/analysis/room/hour_count", response_model=list[HourCount])
async def analysis(session: Session = Depends(get_session)):
    return db_hourly_analysis(session)



@router.get("/analysis/room/summary", response_model=BookingSummary)
async def analysis(session: Session = Depends(get_session)):
    return db_summary_analysis(session)

# Return analytics results for specific years.
# Contains the same data as the routes above
# While the routes above returns every data from the data base
# The below routes return data for the year passed as ann argument.

@router.get("/analysis/room/{year}", response_model=list[RoomResults])
async def room_analysis(year: str, session: Session = Depends(get_session)):
    return db_room_analysis(session, year)


@router.get("/analysis/room/date/{year}", response_model=list[DateResults])
async def trend_analysis(year: str, session: Session = Depends(get_session)):
    return db_trend_analysis(session, year)



@router.get("/analysis/room/daily_revenue/{year}", response_model=list[DayResults])
async def daily_analysis(year: str, session: Session = Depends(get_session)):
    return db_daily_analysis(session, year)

    

@router.get("/analysis/room/hour_count/{year}", response_model=list[HourCount])
async def analysis(year: str, session: Session = Depends(get_session)):
    return db_hourly_analysis(session, year)


@router.get("/analysis/room/summary/{year}", response_model=BookingSummary)
async def analysis(year: str, session: Session = Depends(get_session)):
     return db_summary_analysis(session, year)


