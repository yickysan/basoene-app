import React from "react"
import {useState, useEffect} from "react"
import { Product } from "../App"
import SellProduct from "./sell"

type Sales = {
    id: number;
    quantity: number;
    sales_date: string;
    time: string;
    product_id: number
}

type SalesData = {
    product_name: string;
    unit_price : number;
    ProductSales: Sales ;
}

export interface SalesProps{
    data: Product[],
    fetch: Function
}

const SalesPage = (props: SalesProps) => {

    const productData = props.data;
    const fetchProducts = props.fetch

    const [sales, setSales] = useState<SalesData[]>(
        [
            {product_name: "",
             unit_price: 0,
            ProductSales: {
                id: 0,
                quantity: 0,
                sales_date: "",
                time: "",
                product_id: 0
            }
        }
        ]
        );


    const totalSales = (): number =>{

        const quantity = sales.map((sale: SalesData) => ( sale.ProductSales.quantity));

        const unitPrices = sales.map((sale: SalesData) => (sale.unit_price));

        // return the sum of the product of quantity and unit price 
        // e.g (quantity1 * unitPrice1) + (quantity2 * uniprice2)

        const sumQuantity = (sum: number, val: number, index: number) => { 
            return sum  + (val * unitPrices[index])
        }

        return quantity.reduce(sumQuantity, 0);
    }


    
    
    const url: string = "localhost:8000/sales/today"

    const fetchSales = (): void => {
        fetch(url)
            .then(response => {
                if (!response.ok){
                    throw new Error("No sales data for today!")
                }
                return response.json();
            })
            .then(result => {
                setSales(result)
            })
            .catch(error => {
               console.log(error.message)
            });
         }

    useEffect(() => {
        fetchSales()
    },[]);

      
    return (
        <div className="sales">
       
            <div className="table-container">
                <table className="sales-table">
                    <caption>Today's Sales
                        <p>Total - NGN ₦{totalSales()}</p>
                    </caption>
                    <thead>
                        <tr>
                            <th>Drink</th>
                            <th>Date</th>
                            <th>Time</th>
                            <th>Quantity</th>
                            <th>Unit Price (₦)</th>
                            <th>Total (₦)</th>

                        </tr>
                    </thead>
                    <tbody>
                        {sales.map((data: SalesData) => (
                            <tr key={data.ProductSales.id}>
                                <td>{data.product_name}</td>
                                <td>{data.ProductSales.time.substring(0, 10)}</td>
                                <td>{data.ProductSales.time.substring(11, 16)}</td>
                                <td>{data.ProductSales.quantity}</td>
                                <td>{data.unit_price}</td>
                                <td>{data.unit_price * data.ProductSales.quantity}</td>
                            </tr>
                            
                            
                        ))}

                    </tbody>
                </table> 
            </div>
            <div className="sales-card">
                <h3> Enter Sales</h3>
                <SellProduct data={productData} fetchSales={fetchSales} fetchProducts={fetchProducts}/>
            </div>
            
        </div>
    );
}
 
export default SalesPage;