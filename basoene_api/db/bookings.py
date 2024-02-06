from sqlmodel import Session, select
from basoene_api.models.rooms import Rooms, Bookings, BookRoom
from datetime import date

class NoBookingsError(Exception):
    ...


def db_bookings(session: Session):
    
    query = (select(Bookings,Rooms.room_name, Rooms.price_short, Rooms.price_full)
            .where(Bookings.room_id == Rooms.id))
    result = session.exec(query).all()
    return result


def db_get_todays_bookings(session: Session):

    bookings = session.exec(
        (select(Bookings, Rooms.room_name, Rooms.price_short, Rooms.price_full)
         .where(Bookings.booking_date == date.today())
         .where(Bookings.room_id == Rooms.id)
         .order_by(Bookings.time.desc())
        )
    ).all()

    if len(bookings) < 1:
        raise NoBookingsError("No room has been booked today")
    
    return bookings


def db_get_bookings(date: str, session: Session):

    bookings = session.exec(
        (select(Bookings, Rooms.room_name, Rooms.price_short, Rooms.price_full)
         .where(Bookings.booking_date == date)
         .where(Bookings.room_id == Rooms.id)
        )
    ).all()

    if len(bookings) < 1:
        raise NoBookingsError("No room was booked on this date")
    
    return bookings


def db_book_room(booking: BookRoom, session: Session) -> Bookings:
    db_booking = Bookings.from_orm(booking)
    session.add(db_booking)
    session.commit()
    session.refresh(db_booking)

    return booking