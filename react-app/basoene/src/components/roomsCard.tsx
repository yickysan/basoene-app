import React from "react"
import { Rooms } from "./booking"


interface RoomsProp{
    rooms: Rooms[],
}

const RoomsCard = (props: RoomsProp) => {

    const rooms = props.rooms;

        
    return (
        <div className="flex-body">
            {rooms.map((room: Rooms) => (
                <div id= {room.room_name} key={room.id} className="room-card">
                    <h5>{room.room_name}</h5>
                    <h6 className="status">Status: Available</h6>
                    <h6 className="availabilty">Available in - 00:00:00</h6>
                </div>
                
                
            ))}

        </div>
      );
}
 
export default RoomsCard;