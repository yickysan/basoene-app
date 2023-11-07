import React from "react";
import { useState } from "react";
import { Product } from "../App";
import {BiSolidXSquare} from "react-icons/bi"


  

  interface UpdateProps{
    update: Function,
    productUpdated: Product,
    request: string,
    refresh: Function
  }

const Update = (props: UpdateProps) => {

    const toggleUpdate = props.update;
    const product = props.productUpdated;
    const request = props.request;
    const fetchProducts = props.refresh;

    const [productName, setProductName] = useState(product.product_name);
    const [productCategory, setProductCategory] = useState(product.product_category);
    const [quantity, setQuantity] = useState(product.quantity);
    const [unitPrice, setUnitPrice] = useState(product.unit_price);

    const [submitting, setSubmitting] = useState(false);
    
   const handleSubmit = (e: React.FormEvent<HTMLFormElement>): void => {
        e.preventDefault()
        const updatedProduct: Product = {
            product_name: productName,
            product_category: productCategory,
            quantity: quantity,
            unit_price: unitPrice,
            id: product.id
        }
         
        setSubmitting(true);

        if(request === "PUT"){
            fetch(`${process.env.REACT_APP_URL}/products/` + updatedProduct.id, {
                method : request, 
                headers : {"Content-Type": "application/json"},
                body : JSON.stringify(updatedProduct)
            }).then(() => {
                setSubmitting(false);
                toggleUpdate();
    
            }).then(() => {fetchProducts();})
           ;
        } else if(request === "POST"){
            fetch(`${process.env.REACT_APP_URL}/products`, {
                method : request, 
                headers : {"Content-Type": "application/json"},
                body : JSON.stringify(updatedProduct)
            }).then(() => {
                setSubmitting(false);
                toggleUpdate();
            }).then(() => {fetchProducts();})
        }
       
        
   }

    return ( 
        <div className="form-wrapper">
            <div className="overlay">
                <form className="update-form" onSubmit={handleSubmit}>
                    <button aria-label="close-popup"
                    style={{background: "none",
                            border: "none",
                            transform: "translate(35rem, -1rem)"}}
                    onClick={() => {toggleUpdate();}}>
                        <BiSolidXSquare size="2.5rem" color="var(--main-clr)" />
                    </button>
                    <div className="form-inputs">
                        <div className="input-container">
                            <label>Product</label>
                            <input type="text" 
                            value={productName}
                            onChange={(e) => {setProductName(e.target.value)}}>
                                
                            </input>
                        </div>
                        

                        <div className="input-container">
                            <label>Category</label>
                            <input type="text" 
                            value={productCategory}
                            onChange={(e) => {setProductCategory(e.target.value)}}>
                                
                            </input>
                        </div>

                        <div className="input-container">
                            <label>Quantity</label>
                            <input type="number"
                            value={quantity}
                            onChange={(e) => {setQuantity(e.target.value as unknown as number)}}>
                                
                            </input>
                        </div>

                        <div className="input-container">
                            <label>Unit Price</label>
                            <input type="number" 
                            value={unitPrice}
                            onChange={(e) => {setUnitPrice(e.target.value as unknown as number)}}>
                                
                            </input>
                        </div>

                        {!submitting && 
                        <button className="submit-product">
                            Submit
                        </button>
                        }
                        {submitting && 
                        <button className="submit-product" disabled>
                                <div className="submitting"></div>
                        </button>
                        }
                                
                    </div>
                    
                </form>
            </div>
        </div>
     );
}
 
export default Update;