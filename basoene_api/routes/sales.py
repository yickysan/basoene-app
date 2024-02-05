from fastapi import APIRouter
from fastapi import Response, Depends, HTTPException
from sqlmodel import Session, select
from typing import Generator
from datetime import date
from basoene_api.models.products import ProductSales, Products, SalesPost
from basoene_api.routes.products import get_session
from basoene_api.db.sales import (
    db_sales,
    db_get_todays_sale,
    db_get_sales,
    db_add_sales,
    NoSalesError
)

router = APIRouter()

@router.get("/sales") 
async def sales(session: Session = Depends(get_session)):
    
   return db_sales(session)


@router.get("/sales/today")
async def get_todays_sale(session: Session = Depends(get_session)):
    try:
        return db_get_todays_sale(session)

    except NoSalesError:
        raise HTTPException(status_code=404, headers={"message": "No sales have been made today"})


@router.get("/sales/{date}")
async def get_sale(date: str, response: Response, session: Session = Depends(get_session)):

    try:
        return db_get_sales(date, session)

    except NoSalesError:
        raise HTTPException(status_code=404, headers={"message": "No sales was made on this date"})
    
    
@router.post("/sales", response_model = ProductSales)
async def add_sales(sales: SalesPost, session: Session = Depends(get_session)):
    return db_add_sales(sales, session)