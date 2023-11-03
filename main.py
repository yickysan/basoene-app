from sqlmodel import Session, select, func, extract, case, literal_column
from typing import Generator
# from basoene_api.models.products import Products, ProductSales, engine
from basoene_api.models.rooms import Bookings, Rooms, engine
from datetime import date



with Session(engine) as session:
    
    query = (select(func.sum(
                         case(
                             (func.lower(Bookings.booking_type) == "short", Rooms.price_short),
                             else_ = Rooms.price_full
                             )
                     ).label("revenue")
                  )
         .where(Bookings.room_id == Rooms.id)
         .where(extract("year",Bookings.booking_date) == date.today().year)   
        )
    


    daily_revenue = (select(func.sum(
                         case(
                             (func.lower(Bookings.booking_type) == "short", Rooms.price_short),
                             else_ = Rooms.price_full
                             )
                        ).label("revenue")
                        )
                .where(Bookings.room_id == Rooms.id)
                .where(extract("year",Bookings.booking_date) == date.today().year)
                .group_by(Bookings.booking_date)
                )
    avg_daily_revenue = select(func.round(
                        func.avg(daily_revenue.c.revenue), 2
                        ).label("avg_daily_revenue")
                        )

    query3 = (select(func.count(Bookings.time))
              .where(extract("year",Bookings.booking_date) == date.today().year)
              )

    result1 = session.exec(query).first()
    result2 = session.exec(query3).first()
    


if __name__ == "__main__":
    print(result1)
    print()
    print("---------------------------------------------")
    print(result2)
    print()
    print("---------------------------------------------")
    print(session.exec(avg_daily_revenue).first())
   
   

          
    
    
    


