from fastapi import APIRouter
from fastapi import Response, Depends
from sqlmodel import Session, select
from typing import Generator
from basoene_api.models.products import ProductSales
from basoene_api.routes.products import get_session

router = APIRouter()

@router.get("/sales", response_model = list[ProductSales])
async def sales(session: Session = Depends(get_session)):
    
    query = select(ProductSales)
    result = session.exec(query).all()
    return result


@router.get("/sales/{date}/", response_model = list[ProductSales] | str)
async def get_sale(date: str, response: Response, session: Session = Depends(get_session)):

    sales = session.exec(
        select(ProductSales).where(ProductSales.sale_date == date)
    ).all()

    if len(sales) < 1:
        response.status_code = 404
        return "Could not find record"
    
    return sales
    
@router.post("/sales", response_model = ProductSales)
async def add_sales(sales: ProductSales, session: Session = Depends(get_session)):
    session.add(sales)
    session.commit()
    session.refresh(sales)

    return sales