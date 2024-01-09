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
      indexAxis: "x" as const,
      elements: {
        bar: {
          borderWidth: 1,
        },
      },
      responsive: true,
      plugins: {
        legend: {
          position: "right" as const,
          display: false
        },
        title: {
          display: true,
          text: "Total Sales By Day",
        },
      },
    };

  
    type DayResult = {
      day: number;
      total: number;
    }

    const dayMap = new Map(
        [
            [0, "Sun"],
            [1, "Mon"],
            [2, "Tue"],
            [3, "Wed"],
            [4, "Thu"],
            [5, "Fri"],
            [6, "Sat"],
    
        ]
        
    )
  
   const SalesDay = () => {
  
      const data = useFetchChartData("product/day").data;
  
      const chartData = {
          labels : data.map((value: DayResult) => (dayMap.get(value.day))),
          datasets: [{
              label: "Sales (₦)",
              data: data.map((value: DayResult) => (value.total)),
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
    
   export default SalesDay;