import React from "react"
import RevenueTrend from "./charts/roomCharts/revenueTrend";
import  BookingCount from "./charts/roomCharts/bookingHourCount";
import RoomRevenue from "./charts/roomCharts/roomRevenue";
import RoomRevenueDay from "./charts/roomCharts/dailyRevenue";
import { useFetchBookingsSummary, bookingsSummary } from "../helper/fetchChartData";


interface statsProps{
    summary: string
}
const RoomStats = (props: statsProps) => {

    const summaryData = useFetchBookingsSummary();
    const totalRevenue = new Intl.NumberFormat().format(summaryData.total_revenue);
    const avgRevenue = new Intl.NumberFormat().format(summaryData.avg_daily_revenue);
    return ( 
        <div className="stats">
            <div className="stat-title">
                <h3>Room Booking Summary</h3>
                <div className="summary-card-wrapper">
                    <div className="summary-card">
                        <h5>Total Revenue</h5>
                        <p>{`₦${totalRevenue}`}</p>
                    </div>
                    <div className="summary-card">
                        <h5>Avg Daily Revenue</h5>
                        <p>{`₦${avgRevenue}`}</p>
                    </div>
                    <div className="summary-card">
                        <h5>Total No of Bookings</h5>
                        <p>{summaryData.total_bookings}</p>
                    </div>
                </div>
            </div>
             <div className="chart-grid">
            <BookingCount/>
            <RevenueTrend/>
            <RoomRevenue/>
            <RoomRevenueDay/>
            </div> 
        </div>
         
     );
}
 
export default RoomStats;