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
        text: "Total Sales By Hour",
      },
    },
  };

  type HourResult = {
    hour: number;
    total: number;
  }

 const SalesHour = () => {

    const {data, isLoading, error} = useFetchChartData("product/hour");

    const chartData = {
        labels : data.map((value: HourResult) => (value.hour as unknown as string)).reverse(),
        datasets: [{
            label: "Sales (₦)",
            data: data.map((value: HourResult) => (value.total)).reverse(),
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
  
 export default SalesHour;