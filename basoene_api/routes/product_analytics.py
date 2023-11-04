from fastapi import APIRouter
from fastapi import Response, Depends, HTTPException
from sqlmodel import Session, select, func, extract
from typing import Generator
from datetime import date
from basoene_api.models.products import Products, ProductSales, engine
from basoene_api.models.product_analysis import DateResults, ProductResults, HourResults, DayResults, MonthResults, SalesSummary

router = APIRouter()


def get_session() -> Generator[Session, None, None]:
    with Session(engine, autoflush=True) as session:
        yield session

@router.get("/analysis/product", response_model=list[ProductResults])
async def analysis(session: Session = Depends(get_session)):
     query = (select(Products.product_name, 
                     func.sum(ProductSales.quantity * Products.unit_price).label("total"))
                    .where(Products.id == ProductSales.product_id)
                    .where(extract("year", ProductSales.sale_date) == date.today().year)
                    .group_by(Products.product_name)
                    .order_by("total")
                )
     result = session.exec(query).all()
     return result


@router.get("/analysis/product/date", response_model=list[DateResults])
async def analysis(session: Session = Depends(get_session)):
     query = (select(ProductSales.sale_date, 
                     func.sum(ProductSales.quantity * Products.unit_price).label("total"))
                    .where(Products.id == ProductSales.product_id)
                    .where(extract("year", ProductSales.sale_date) == date.today().year)
                    .group_by(ProductSales.sale_date)
                )
     result = session.exec(query).all()

     return result


@router.get("/analysis/product/month", response_model=list[MonthResults])
async def analysis(session: Session = Depends(get_session)):
     query = (select(extract("month",ProductSales.sale_date).label("month"),
                      func.sum(ProductSales.quantity * Products.unit_price).label("total"))
                        .where(Products.id == ProductSales.product_id)
                        .where(extract("year", ProductSales.sale_date) == date.today().year)
                        .group_by("month")
                        .order_by("month")
                    )
     result = session.exec(query).all()

     return result


@router.get("/analysis/product/day", response_model=list[DayResults])
async def analysis(session: Session = Depends(get_session)):
     query = (select(extract("dow",ProductSales.sale_date).label("day"),
                      func.sum(ProductSales.quantity * Products.unit_price).label("total"))
                        .where(Products.id == ProductSales.product_id)
                        .where(extract("year", ProductSales.sale_date) == date.today().year)
                        .group_by("day")
                        .order_by("day")
                    )
     result = session.exec(query).all()

     return result


@router.get("/analysis/product/hour", response_model=list[HourResults])
async def analysis(session: Session = Depends(get_session)):
     query = (select(extract("hour", ProductSales.time).label("hour"),
                     func.sum(ProductSales.quantity * Products.unit_price).label("total")
                     )
                    .where(Products.id == ProductSales.product_id)
                    .where(extract("year", ProductSales.sale_date) == date.today().year)
                    .group_by("hour")
                    .order_by("total")

                    )
     result = session.exec(query).all()
     return result



@router.get("/analysis/product/summary", response_model=SalesSummary)
async def analysis(session: Session = Depends(get_session)):
     total_sales = (select(
                      func.sum(
                         ProductSales.quantity * Products.unit_price
                     ).label("total_sales")
                     )
                .where(Products.id == ProductSales.product_id)
                .where(extract("year",ProductSales.sale_date) == date.today().year)
                )
     
     daily_sales = (select(ProductSales.sale_date,
                      func.sum(
                         ProductSales.quantity * Products.unit_price
                     ).label("total")
                     )
                .where(Products.id == ProductSales.product_id)
                .where(extract("year",ProductSales.sale_date) == date.today().year)
                .group_by(ProductSales.sale_date)
                )
     daily_average = select(func.round(
                            func.avg(daily_sales.c.total), 2
                            ).label("avg_daily_sales")
                        )
     
     total_quantity = (select(func.sum(ProductSales.quantity).label("total_drinks"))
                .where(extract("year",ProductSales.sale_date) == date.today().year))
     

     result = {"total_sales": session.exec(total_sales).first(),
               "avg_daily_sales": session.exec(daily_average).first(),
               "total_products_sold": session.exec(total_quantity).first()
               }

     return result


