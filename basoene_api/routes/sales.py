from fastapi import APIRouter
from fastapi import Response, Depends, HTTPException
from sqlmodel import Session, select
from typing import Generator
from datetime import date
from basoene_api.models.products import ProductSales, Products, SalesPost
from basoene_api.routes.products import get_session

router = APIRouter()

@router.get("/sales") 
async def sales(session: Session = Depends(get_session)):
    
    query = select(Products.product_name, ProductSales).where(Products.id == ProductSales.product_id)
    result = session.exec(query).all()
    return result


@router.get("/sales/today")
async def get_todays_sale(response: Response, session: Session = Depends(get_session)):
    sales = session.exec(
        (select(Products.product_name, ProductSales)
         .where(Products.id == ProductSales.product_id)
         .where(ProductSales.sale_date == date.today())
         .order_by(ProductSales.time.desc())
         )
    ).all()

    if len(sales) < 1:
        raise HTTPException(status_code=404, headers={"message": "No sales have been made today"})

    return sales


@router.get("/sales/{date}/")
async def get_sale(date: str, response: Response, session: Session = Depends(get_session)):

    sales = session.exec(
        (select(Products.product_name, ProductSales)
         .where(Products.id == ProductSales.product_id)
         .where(ProductSales.sale_date == date)
         )
    ).all()

    if len(sales) < 1:
         response.status_code = 404
    
    return sales
    
@router.post("/sales", response_model = ProductSales, response_model_exclude_defaults=True)
async def add_sales(sales: SalesPost, session: Session = Depends(get_session)):
    db_sales = ProductSales.from_orm(sales)
    session.add(db_sales)
    session.commit()
    session.refresh(db_sales)

    return db_sales