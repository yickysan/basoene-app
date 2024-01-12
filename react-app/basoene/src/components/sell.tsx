import React, {useState} from "react"
import { Product } from "../App";



interface SellProps{
    data: Product[],
    fetchSales: Function
    fetchProducts: Function
}


const SellProduct = (props: SellProps) => {
    const productData = props.data;
    const fetchSales = props.fetchSales;
    const fetchProducts = props.fetchProducts

    const [formProduct, setFormProduct] = useState("")
    const [formQuantity, setFormQuantity] = useState(0)

    const [submitting, setSubmitting] = useState(false);

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>): void => {
        e.preventDefault()
        setFormProduct("");
        setFormQuantity(0);
        setSubmitting(true);
        const requiredProduct = productData.filter((product) => (product.product_name === formProduct))[0];
        const productId = requiredProduct.id;
        requiredProduct.quantity = requiredProduct.quantity - formQuantity;

        const newSales = {product_id: productId, quantity: formQuantity}

        fetch(`${process.env.REACT_APP_URL}/sales`, {
                method : "POST", 
                headers : {"Content-Type": "application/json"},
                body : JSON.stringify(newSales)
            }).then(() => {
                setSubmitting(false);
            }).then(() => {fetchSales();})

        fetch(`${process.env.REACT_APP_URL}/products/` + productId, {
            method : "PUT", 
            headers : {"Content-Type": "application/json"},
            body : JSON.stringify(requiredProduct)
        }).then(() => {fetchProducts();})

        
        
    }
    
    return ( 
        <div className="sales-form">
            <form className="sell" onSubmit={handleSubmit}>
                <div className="sales-input">
                    <label>Drinks</label>
                    <input name="Drink" 
                    value={formProduct}
                    list="drink-list" 
                    onChange={(e) =>{setFormProduct(e.target.value);}}
                    onFocus={(e) => {setFormProduct("");}}
                    required/>
                    <datalist id = "drink-list">
                        {
                            productData.map((product: Product) => {
                                if(product.quantity !== 0){
                                 return <option key={product.id} value={product.product_name}/>
                                } else{
                                    return ""
                                }
                            }
                            )
                            }
                        

                    </datalist>
                </div>
                
                <div className="sales-input">
                    <label>Quantity</label>
                    <input type="number" 
                    value={formQuantity}
                    onChange={(e) => {setFormQuantity(e.target.value as unknown as number)}}
                    required/>
                </div>
                {!submitting && 
                    <button className="submit-sales">
                        Sell
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
 
export default SellProduct;