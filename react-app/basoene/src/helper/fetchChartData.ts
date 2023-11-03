import {useState, useEffect} from "react"

type fetchResult = {
    data: [];
    isLoading: boolean;
    error: string | null ;
}

export type salesSummary = {
    total_sales: number;
    avg_daily_sales: number;
    total_products_sold: number
}

export type bookingsSummary = {
    total_revenue: number;
    avg_daily_revenue: number;
    total_bookings: number
}

const useFetchChartData = (endpoint: string): fetchResult => {

    const [data, setData] = useState<[]>([]);
    
    const [isLoading, setLoading] = useState<boolean>(true)

    const [error, setError] = useState<string|null>(null);

    useEffect(() => {
        fetch("http://localhost:8000/analysis/" + endpoint)
            .then(response => {
                if (!response.ok){
                    throw new Error("Could not get messages!")
                }
                return response.json();
            })
            .then(data => {
                setData(data);
                setLoading(false);
                setError(null);
            })
            .catch(error => {
                setError(error.message);
                setLoading(false);
            });;
    }, [endpoint]);

    return {data, isLoading, error};
}

export const useFetchBookingsSummary = (): bookingsSummary => {

    const [data, setData] = useState<bookingsSummary>({total_revenue:0, avg_daily_revenue:0, total_bookings:0});
    

    useEffect(() => {
        fetch("http://localhost:8000/analysis/room/summary")
            .then(response => {
                if (!response.ok){
                    throw new Error("Could not get messages!")
                }
                return response.json();
            })
            .then(data => {
                setData(data);
            })
            .catch(error => {
                console.log(error)
            });
    }, []);

    return data;
}


export const useFetchSalesSummary = (): salesSummary => {

    const [data, setData] = useState<salesSummary>({total_sales:0, avg_daily_sales:0, total_products_sold:0});
    

    useEffect(() => {
        fetch("http://localhost:8000/analysis/product/summary")
            .then(response => {
                if (!response.ok){
                    throw new Error("Could not get messages!")
                }
                return response.json();
            })
            .then(data => {
                setData(data);
            })
            .catch(error => {
                console.log(error)
            });
    }, []);

    return data;
}

export default useFetchChartData
