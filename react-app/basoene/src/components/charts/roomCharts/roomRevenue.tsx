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
  
    export const options = {
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
          text: "Total Revenue By Room",
        },
      },
    };
  
    type RoomResult = {
      room_name: string;
      revenue: number;
    }
  
   const RoomRevenue = () => {
  
      const {data, isLoading, error} = useFetchChartData("room");
  
      const chartData = {
          labels : data.map((value: RoomResult) => (value.room_name)).reverse(),
          datasets: [{
              label: "Revenue (₦)",
              data: data.map((value: RoomResult) => (value.revenue)).reverse(),
              backgroundColor: "rgb(165, 80, 199)",
              borderColor : "rgb(165, 80, 199)"
          }]
      }
  
      return (
          
              <div className="chart-wrapper product">
                  <Bar data={chartData} options={options}/>
              </div> 
        );
   }
    
   export default RoomRevenue;