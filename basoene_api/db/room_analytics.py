from sqlmodel import Session, select, func, extract, case
from typing import Optional
from datetime import date
from basoene_api.models.rooms import Rooms, Bookings
from basoene_api.models.room_analysis import DateResults, RoomResults, HourCount, DayResults, BookingSummary



def db_room_analysis(session: Session, year: Optional[str] = None) -> list[RoomResults]:

    if year:
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


def db_trend_analysis(session: Session, year: Optional[str] = None) -> list[DateResults]:

    if year:
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


def db_daily_analysis(session: Session, year: Optional[str] = None) -> list[DayResults]:

    if year:
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

    


def db_hourly_analysis(session: Session, year: Optional[str] = None) -> list[HourCount]:

    if year:
        query = (select(extract("hour", Bookings.time).label("hour"),
                    func.count(Bookings.time).label("booking_count"))
            .where(extract("year", Bookings.booking_date) == year)
            .group_by("hour")
            .order_by("booking_count")
            )  
         
        result = session.exec(query).all()
        return result

    query = (select(extract("hour", Bookings.time).label("hour"),
                    func.count(Bookings.time).label("booking_count"))
            .group_by("hour")
            .order_by("booking_count")
            )  
         
    result = session.exec(query).all()
    return result



def db_summary_analysis(session: Session, year: Optional[str] = None) -> BookingSummary:

    if year:
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




    

     
    



