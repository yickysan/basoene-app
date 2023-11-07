import React from "react"
import {useState, useEffect} from "react"
import RoomsCard from "./roomsCard"
import BookRoom from "./bookRoom"

type Booking = {
    id: number;
    booking_type: string;
    booking_date: string;
    time: string;
    room_id: number
}

type BookingData = {
    room_name: string;
    price_short: number;
    price_full: number;
    Bookings: Booking ;
}

export type Rooms = {
    id: number;
    room_name: string;
    room_type: string;
    price_short: number; 
    price_full: number;
}


const BookingPage = () => {

    const [bookings, setBookings] = useState<BookingData[]>(
        [
            {room_name: "",
             price_short: 0,
             price_full: 0,
            Bookings: {
                id: 0,
                room_id: 0,
                booking_date: "",
                time: "",
                booking_type: ""
            }
        }
        ]
        );

    
    const [rooms, setRooms] = useState<Rooms[]>(
        [
            {
                id: 0,
                room_name: "",
                room_type: "",
                price_short: 0,
                price_full: 0
            }
            
        ]
    )
    
    // state for managing booking of room
    const [bookingType, setBookingType] = useState("")
    const [roomName, setRoomName] = useState("")


    const totalAmount = (): number =>{

        const amount = bookings.map((booking: BookingData) => (
            booking.Bookings.booking_type.toLowerCase() === "short"?
            booking.price_short: booking.price_full)
            );

        const sumAmount = (sum: number, val: number) => { 
            return sum  + val
        }

        return amount.reduce(sumAmount, 0);
    }


    
    
    const url: string = `${process.env.REACT_APP_URL}/bookings/today`

    const fetchBookings = (): void => {
        fetch(url)
            .then(response => {
                if (!response.ok){
                    throw new Error("No sales data for today!")
                }
                return response.json();
            })
            .then(result => {
                setBookings(result)
            })
            .catch(error => {
               console.log(error.message)
            });
         }


    const fetchRooms = (): void => {
        fetch(`${process.env.REACT_APP_URL}/rooms/`)
            .then(response => {
                if (!response.ok){
                    throw new Error("No sales data for today!")
                }
                return response.json();
            })
            .then(result => {
                setRooms(result)
            })
            .catch(error => {
               console.log(error.message)
            });
         }

    useEffect(() => {
        fetchBookings();
        fetchRooms();
    },[]);

      
    return (
        <div className="bookings">
            <RoomsCard rooms = {rooms}/>

            <div className="room-grid">
                <div className="table-container">
                    <table className="bookings-table">
                        <caption>Today's Amount
                            <p>Total - NGN ₦{totalAmount()}</p>
                        </caption>
                        <thead>
                            <tr>
                                <th>Room</th>
                                <th>Date</th>
                                <th>Time</th>
                                <th>type</th>
                                <th>Amount (₦)</th>

                            </tr>
                        </thead>
                        <tbody>
                            {bookings.map((data: BookingData) => (
                                <tr key={data.Bookings.id}>
                                    <td>{data.room_name}</td>
                                    <td>{data.Bookings.booking_date}</td>
                                    <td>{data.Bookings.time.substring(11, 16)}</td>
                                    <td>{data.Bookings.booking_type}</td>
                                    <td>{data.Bookings.booking_type.toLowerCase() === "short"?
                                        data.price_short: data.price_full}</td>
                                </tr>
                                
                                
                            ))}

                        </tbody>
                    </table> 
                </div>
                <div className="sales-card booking-card">
                    <h3> Book a Room</h3>
                    <BookRoom rooms={rooms} 
                    refresh={fetchBookings}
                    setRoom={[roomName, setRoomName]}
                    setBooking={[bookingType, setBookingType]}/>
                </div>

            </div>
             
        </div>
    );
}
 
export default BookingPage;