import React, {useState, Dispatch, SetStateAction} from "react"

import { Rooms } from "./booking";

interface BookRoomProps{
    rooms : Rooms[],
    refresh: Function,
    setRoom: [string, Dispatch<SetStateAction<string>>],
    setBooking: [string, Dispatch<SetStateAction<string>>]
}
const BookRoom = (props: BookRoomProps) => {

    const rooms = props.rooms;
    const fetchBookings = props.refresh;
    const [roomName, setRoomName] = props.setRoom;
    const [bookingType, setBookingType] = props.setBooking;
  

    const [submitting, setSubmitting] = useState(false);

    const setStatusAvailabity = (roomname: string, bookingtype: string): void =>{
        const roomcard = document.getElementById(roomname) as HTMLDivElement;
        const status  = roomcard.querySelector(".status") as HTMLHeadingElement;
        const availabilty = roomcard.querySelector(".availabilty") as HTMLHeadingElement
        
        const setExpiration = (): number => {
            if (bookingtype.toLocaleLowerCase() === "short"){
                const expiration = new Date().getTime() + 1000 * 60 ;
                return expiration
               
            } else{
                const expiration = new Date().getTime() + 1000 * 60 * 2 ;
                return expiration
            }
        }

        const expiration = setExpiration();
        
        
        

        const countDown = setInterval(() => {

            const currentTime = new Date().getTime();
            const difference = expiration - currentTime;

            // get minutes and seconds
            const minutes = Math.floor(difference % (1000 * 60 * 60) / (1000 * 60));
            const seconds = Math.floor(difference % (1000 * 60) / 1000 );

            const formatedminutes = minutes < 10? `0${minutes}` : minutes
            const formatedseconds = seconds < 10? `0${seconds}` : seconds

            status.classList.add("occupied");
            status.innerText = "Status: Occupied";
            availabilty.innerText = `Available in - 00:${formatedminutes}:${formatedseconds}`;

            if (difference <= 0){
                clearInterval(countDown);
                status.innerText = "Status: Available"
                status.classList.remove("occupied");
                availabilty.innerText = "Available in- 00:00:00"
                localStorage.removeItem("expiration");
            }
        }, 1000);
    }

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>): void => {
        e.preventDefault()
        setSubmitting(true);
        const requiredRoom = rooms.filter((room) => (room.room_name === roomName))[0];
        const roomId = requiredRoom.id;

        const newBooking = {room_id: roomId, booking_type: bookingType}

        fetch("http://localhost:8000/bookings", {
                method : "POST", 
                headers : {"Content-Type": "application/json"},
                body : JSON.stringify(newBooking)
            }).then(() => {
                setSubmitting(false);
                setStatusAvailabity(roomName, bookingType);
            }).then(() => {fetchBookings();})
            .then(() => {
                setRoomName("");
                setBookingType("");
            })
    
        }

    return (  
        <div className="sales-form booking-form">
        <form className="sell" onSubmit={handleSubmit}>
            <div className="sales-input">
                <label>Rooms</label>
                <input name="Rooms" 
                list="room-list" 
                onChange={(e) =>{setRoomName(e.target.value)}}
                required/>
                <datalist id = "room-list">
                    {
                        rooms.map((room: Rooms) => (
                             <option key={room.id} value={room.room_name}/>
                        )
                        )
                        }
                    

                </datalist>
            </div>
            
            <div className="sales-input">
                <label>Booking type</label>
                <input name="Booking type" 
                    list="booking-type" 
                    onChange={(e) =>{setBookingType(e.target.value)}}
                    required/>
                    <datalist id = "booking-type">
                        <option value="Short"/>
                        <option value="Full"/>
                    </datalist>
            </div>

            {!submitting && 
                <button className="submit-sales">
                    Book
                </button>
            }
            {submitting && 
                <button className="submit-sales" disabled>
                        <div className="submitting"></div>
                </button>
            }
        </form>
    </div>
    );
}
 
export default BookRoom;