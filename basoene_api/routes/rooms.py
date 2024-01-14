from fastapi import APIRouter
from fastapi import Response, Depends, HTTPException
from sqlmodel import Session, select
from typing import Generator
from basoene_api.models.rooms import Rooms, RoomsAdd, RoomsUpdate, engine

router = APIRouter()

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


@router.get("/rooms", response_model = list[Rooms])
async def room_home(session: Session = Depends(get_session)):
    
    query = select(Rooms)
    result = session.exec(query).all()
    return result


@router.get("/rooms/{room_name}/", response_model = list[Rooms])
async def get_room(room_name: str, response: Response, session: Session = Depends(get_session)):

    rooms = session.exec(
        select(Rooms).where(Rooms.room_name == room_name)
    ).all()

    if len(rooms) < 1:
        raise HTTPException(status_code=404, headers={"message": "Room not found"})
    
    return rooms
    
@router.post("/rooms", response_model = Rooms)
async def add_room(room: RoomsAdd, session: Session = Depends(get_session)):
    db_room = Rooms.from_orm(room)
    session.add(db_room)
    session.commit()
    session.refresh(db_room)

    return room


@router.put("/rooms/{id}", response_model = Rooms)
async def update_room(id: int, 
                   room: RoomsUpdate,
                   response: Response,
                   session: Session = Depends(get_session)):
    
    db_room = session.get(Rooms, id)

    if not db_room:
        raise HTTPException(status_code=404, headers={"message": "Room not found"})

    updated_data = room.dict(exclude_unset=True)

    for k, v in updated_data.items():
        setattr(db_room, k, v)

    session.add(db_room)
    session.commit()
    session.refresh(db_room)

    return db_room


@router.delete("/rooms/{id}", response_model = str)
async def delete_room(id: int, 
                   response: Response,
                   session: Session = Depends(get_session)):
    
    room = session.get(Rooms, id)

    if not room:
        raise HTTPException(status_code=404, headers={"message": "Room not found"})
    
    session.delete(room)
    session.commit()

    return Response(status_code=200)


