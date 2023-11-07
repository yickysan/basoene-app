import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
  } from "chart.js";
  import { Bar } from "react-chartjs-2";
  import useFetchChartData from "../../../helper/fetchChartData";
  
  ChartJS.register(
      CategoryScale,
      LinearScale,
      BarElement,
      Title,
      Tooltip,
      Legend
    );
  
    const options = {
      indexAxis: "y" as const,
      elements: {
        bar: {
          borderWidth: 2,
        },
      },
      responsive: true,
      plugins: {
        legend: {
          position: "right" as const,
        },
        title: {
          display: true,
          text: "Total Room Bookings By Hour",
        },
      },
    };
  
    type HourCount = {
      hour: number;
      booking_count: number;
    }
  
   const BookingCount = () => {
  
      const data = useFetchChartData("room/hour_count").data;
  
      const chartData = {
          labels : data.map((value: HourCount) => (value.hour as unknown as string)).reverse(),
          datasets: [{
              label: "Bookings",
              data: data.map((value: HourCount) => (value.booking_count)).reverse(),
              backgroundColor: "rgb(165, 80, 199)",
              borderColor : "rgb(165, 80, 199)"
          }]
      }
  
      return (
          
              <div className="chart-wrapper">
                  <Bar data={chartData} options={options}/>
              </div> 
        );
   }
    
   export default BookingCount;