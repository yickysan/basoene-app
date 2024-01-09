from fastapi import APIRouter
from fastapi import Response, Depends, HTTPException
from sqlmodel import Session, select, func, extract, case
from typing import Generator
from datetime import date
from basoene_api.models.rooms import Rooms, Bookings, engine
from basoene_api.models.room_analysis import DateResults, RoomResults, HourCount, DayResults, BookingSummary

router = APIRouter()

def get_session() -> Generator[Session, None, None]:
    with Session(engine, autoflush=True) as session:
        yield session


@router.get("/analysis/room", response_model=list[RoomResults])
async def analysis(session: Session = Depends(get_session)):
    query = (select(Rooms.room_name,
                     func.sum(
                         case(
                             (func.lower(Bookings.booking_type) == "short", Rooms.price_short),
                             else_ = Rooms.price_full
                             )
                     ).label("revenue")
                  )
                .where(Bookings.room_id == Rooms.id)
                .group_by(Rooms.room_name)
                .order_by("revenue")
         
        )
    result = session.exec(query).all()
    return result


@router.get("/analysis/room/date", response_model=list[DateResults])
async def analysis(session: Session = Depends(get_session)):
    query = (select(Bookings.booking_date, 
                      func.sum(
                         case(
                             (func.lower(Bookings.booking_type) == "short", Rooms.price_short),
                             else_ = Rooms.price_full
                             )
                     ).label("revenue"))
                    .where(Rooms.id == Bookings.room_id)
                    .group_by(Bookings.booking_date)
                )
    result = session.exec(query).all()

    return result



@router.get("/analysis/room/daily_revenue", response_model=list[DayResults])
async def analysis(session: Session = Depends(get_session)):
     
    query = (select(extract("dow",Bookings.booking_date).label("day"),
                      func.sum(
                         case(
                             (func.lower(Bookings.booking_type) == "short", Rooms.price_short),
                             else_ = Rooms.price_full
                             )
                     ).label("revenue")
                     )
                .where(Rooms.id == Bookings.room_id)
                .group_by("day")
                .order_by("day")
                )
    
    result = session.exec(query).all()#
    return result

    

@router.get("/analysis/room/hour_count", response_model=list[HourCount])
async def analysis(session: Session = Depends(get_session)):
     
    query = (select(extract("hour", Bookings.time).label("hour"),
                    func.count(Bookings.time).label("booking_count"))
            .group_by("hour")
            .order_by("booking_count")
            )  
         
    result = session.exec(query).all()
    return result



@router.get("/analysis/room/summary", response_model=BookingSummary)
async def analysis(session: Session = Depends(get_session)):
     
    total_revenue = (select(func.sum(
                         case(
                             (func.lower(Bookings.booking_type) == "short", Rooms.price_short),
                             else_ = Rooms.price_full
                             )
                     ).label("revenue")
                  )
         .where(Bookings.room_id == Rooms.id)  
        )
    


    daily_revenue = (select(func.sum(
                         case(
                             (func.lower(Bookings.booking_type) == "short", Rooms.price_short),
                             else_ = Rooms.price_full
                             )
                        ).label("revenue")
                        )
                .where(Bookings.room_id == Rooms.id)
                .group_by(Bookings.booking_date)
                )
    avg_daily_revenue = select(func.round(
                        func.avg(daily_revenue.c.revenue), 2
                        ).label("avg_daily_revenue")
                        )

    total_bookings = (select(func.count(Bookings.time)))

         
    result = {"total_revenue": session.exec(total_revenue).first(),
              "avg_daily_revenue": session.exec(avg_daily_revenue).first(),
              "total_bookings": session.exec(total_bookings).first()
              }

    return result

# Return analytics results for specific years.
# Contains the same data as the routes above
# While the routes above returns every data from the data base
# The below routes return data for the year passed as ann argument.

@router.get("/analysis/room/{year}", response_model=list[RoomResults])
async def analysis(year: str, session: Session = Depends(get_session)):
    query = (select(Rooms.room_name,
                     func.sum(
                         case(
                             (func.lower(Bookings.booking_type) == "short", Rooms.price_short),
                             else_ = Rooms.price_full
                             )
                     ).label("revenue")
                  )
                .where(Bookings.room_id == Rooms.id)
                .where(extract("year",Bookings.booking_date) == year)
                .group_by(Rooms.room_name)
                .order_by("revenue")
         
        )
    result = session.exec(query).all()
    return result


@router.get("/analysis/room/date/{year}", response_model=list[DateResults])
async def analysis(year: str, session: Session = Depends(get_session)):
    query = (select(Bookings.booking_date, 
                      func.sum(
                         case(
                             (func.lower(Bookings.booking_type) == "short", Rooms.price_short),
                             else_ = Rooms.price_full
                             )
                     ).label("revenue"))
                    .where(Rooms.id == Bookings.room_id)
                    .where(extract("year", Bookings.booking_date) == year)
                    .group_by(Bookings.booking_date)
                )
    result = session.exec(query).all()

    return result



@router.get("/analysis/room/daily_revenue/{year}", response_model=list[DayResults])
async def analysis(year: str, session: Session = Depends(get_session)):
     
    query = (select(extract("dow",Bookings.booking_date).label("day"),
                      func.sum(
                         case(
                             (func.lower(Bookings.booking_type) == "short", Rooms.price_short),
                             else_ = Rooms.price_full
                             )
                     ).label("revenue")
                     )
                .where(Rooms.id == Bookings.room_id)
                .where(extract("year",Bookings.booking_date) == year)
                .group_by("day")
                .order_by("day")
                )
    
    result = session.exec(query).all()#
    return result

    

@router.get("/analysis/room/hour_count/{year}", response_model=list[HourCount])
async def analysis(year: str, session: Session = Depends(get_session)):
     
    query = (select(extract("hour", Bookings.time).label("hour"),
                    func.count(Bookings.time).label("booking_count"))
            .where(extract("year", Bookings.booking_date) == year)
            .group_by("hour")
            .order_by("booking_count")
            )  
         
    result = session.exec(query).all()
    return result


@router.get("/analysis/room/summary/{year}", response_model=BookingSummary)
async def analysis(year: str, session: Session = Depends(get_session)):
     
    total_revenue = (select(func.sum(
                         case(
                             (func.lower(Bookings.booking_type) == "short", Rooms.price_short),
                             else_ = Rooms.price_full
                             )
                     ).label("revenue")
                  )
         .where(Bookings.room_id == Rooms.id)
         .where(extract("year",Bookings.booking_date) == year)   
        )
    


    daily_revenue = (select(func.sum(
                         case(
                             (func.lower(Bookings.booking_type) == "short", Rooms.price_short),
                             else_ = Rooms.price_full
                             )
                        ).label("revenue")
                        )
                .where(Bookings.room_id == Rooms.id)
                .where(extract("year",Bookings.booking_date) == year)
                .group_by(Bookings.booking_date)
                )
    avg_daily_revenue = select(func.round(
                        func.avg(daily_revenue.c.revenue), 2
                        ).label("avg_daily_revenue")
                        )

    total_bookings = (select(func.count(Bookings.time))
              .where(extract("year",Bookings.booking_date) == year)
              )

         
    result = {"total_revenue": session.exec(total_revenue).first(),
              "avg_daily_revenue": session.exec(avg_daily_revenue).first(),
              "total_bookings": session.exec(total_bookings).first()
              }

    return result




