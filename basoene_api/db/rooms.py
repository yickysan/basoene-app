from sqlmodel import Session, select
from basoene_api.models.rooms import Rooms, RoomsAdd, RoomsUpdate

class RoomNotFoundError(Exception):
    ...

def db_room_home(session: Session) -> list[Rooms]:
    
    query = select(Rooms)
    result = session.exec(query).all()
    return result


def db_get_room(room_name, session: Session) -> list[Rooms]:

    rooms = session.exec(
        select(Rooms).where(Rooms.room_name == room_name)
    ).all()

    if len(rooms) < 1:
        raise RoomNotFoundError("Room not found")
    
    return rooms
    
def db_add_room(room: RoomsAdd, session: Session) -> Rooms:
    db_room = Rooms.from_orm(room)
    session.add(db_room)
    session.commit()
    session.refresh(db_room)

    return room


def db_update_room(id: int, room: RoomsUpdate, session: Session) -> Rooms:
    
    db_room = session.get(Rooms, id)

    if not db_room:
        raise RoomNotFoundError("Room not found")

    updated_data = room.dict(exclude_unset=True)

    for k, v in updated_data.items():
        setattr(db_room, k, v)

    session.add(db_room)
    session.commit()
    session.refresh(db_room)

    return db_room



def db_delete_room(id: int, session: Session) -> None:
    
    room = session.get(Rooms, id)

    if not room:
        raise RoomNotFoundError("Room not found")
    
    session.delete(room)
    session.commit()

