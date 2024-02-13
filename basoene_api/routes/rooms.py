from fastapi import APIRouter
from fastapi import Response, Depends, HTTPException
from sqlmodel import Session, select
from typing import Generator
from basoene_api.models.rooms import Rooms, RoomsAdd, RoomsUpdate, engine
from basoene_api.db.rooms import(
    db_room_home,
    db_get_room,
    db_add_room,
    db_update_room,
    db_delete_room,
    RoomNotFoundError
)

router = APIRouter()

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


@router.get("/rooms", response_model = list[Rooms])
async def room_home(session: Session = Depends(get_session)):
    
    return db_room_home(session)


@router.get("/rooms/{room_name}/", response_model = list[Rooms])
async def get_room(room_name: str, session: Session = Depends(get_session)):

    try:
        return db_get_room(room_name, session)

    except RoomNotFoundError:
        raise HTTPException(status_code=404, headers={"message": "Room not found"})
    
    
@router.post("/rooms", response_model = Rooms)
async def add_room(room: RoomsAdd, session: Session = Depends(get_session)):
    return db_add_room(room, session)


@router.put("/rooms/{id}", response_model = Rooms)
async def update_room(id: int, 
                   room: RoomsUpdate,
                   session: Session = Depends(get_session)):
    
    try:
        return db_update_room(id, room, session)

    except RoomNotFoundError:
        raise HTTPException(status_code=404, headers={"message": "Room not found"})


@router.delete("/rooms/{id}", response_model = str)
async def delete_room(id: int, session: Session = Depends(get_session)):
    
    try:
        db_delete_room(id, session)
        return Response(status_code=200)

    except RoomNotFoundError:
        raise HTTPException(status_code=404, headers={"message": "Room not found"})
    

    


