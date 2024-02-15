from sqlmodel import Session, select, func, extract
from typing import Optional
from datetime import date
from basoene_api.models.products import Products, ProductSales
from basoene_api.models.product_analysis import DateResults, ProductResults, HourResults, DayResults, MonthResults, SalesSummary




def db_product_analysis(session: Session, year: Optional[str] = None) -> list[ProductResults]:
     
    if year:
        query = (select(Products.product_name, 
                     func.sum(ProductSales.quantity * Products.unit_price).label("total"))
                    .where(Products.id == ProductSales.product_id)
                    .where(extract("year", ProductSales.sale_date) == year)
                    .group_by(Products.product_name)
                    .order_by("total")
                )
        result = session.exec(query).all()
        return result
     
    query = (select(Products.product_name, 
                        func.sum(ProductSales.quantity * Products.unit_price).label("total"))
                        .where(Products.id == ProductSales.product_id)
                        .group_by(Products.product_name)
                        .order_by("total")
                    )
    result = session.exec(query).all()
    return result



def db_trend_analysis(session: Session, year: Optional[str] = None) -> list[DateResults]:

    if year:
        query = (select(ProductSales.sale_date, 
                    func.sum(ProductSales.quantity * Products.unit_price).label("total"))
                .where(Products.id == ProductSales.product_id)
                .where(extract("year", ProductSales.sale_date) == year)
                .group_by(ProductSales.sale_date)
            )
        result = session.exec(query).all()
        return result
         
    query = (select(ProductSales.sale_date, 
                    func.sum(ProductSales.quantity * Products.unit_price).label("total"))
                .where(Products.id == ProductSales.product_id)
                .group_by(ProductSales.sale_date)
            )
    result = session.exec(query).all()
    return result


def db_month_analysis(session: Session, year: Optional[str] = None):

    if year:
        query = (select(extract("month",ProductSales.sale_date).label("month"),
                    func.sum(ProductSales.quantity * Products.unit_price).label("total"))
                    .where(Products.id == ProductSales.product_id)
                    .where(extract("year", ProductSales.sale_date) == year)
                    .group_by("month")
                    .order_by("month")
                )
        result = session.exec(query).all()
        return result
         
    query = (select(extract("month",ProductSales.sale_date).label("month"),
                    func.sum(ProductSales.quantity * Products.unit_price).label("total"))
                    .where(Products.id == ProductSales.product_id)
                    .group_by("month")
                    .order_by("month")
                )
    result = session.exec(query).all()
    return result




def db_daily_analysis(session: Session, year: Optional[str] = None) -> list[DayResults]:

    if year:
        query = (select(extract("dow",ProductSales.sale_date).label("day"),
                    func.sum(ProductSales.quantity * Products.unit_price).label("total"))
                    .where(Products.id == ProductSales.product_id)
                    .where(extract("year", ProductSales.sale_date) == year)
                    .group_by("day")
                    .order_by("day")
                )
        result = session.exec(query).all()
        return result

    query = (select(extract("dow",ProductSales.sale_date).label("day"),
                    func.sum(ProductSales.quantity * Products.unit_price).label("total"))
                    .where(Products.id == ProductSales.product_id)
                    .group_by("day")
                    .order_by("day")
                )
    result = session.exec(query).all()
    return result



def db_hourly_analysis(session: Session, year: Optional[str] = None) -> list[HourResults]:

    if year:
        query = (select(extract("hour", ProductSales.time).label("hour"),
                     func.sum(ProductSales.quantity * Products.unit_price).label("total")
                     )
                    .where(Products.id == ProductSales.product_id)
                    .where(extract("year", ProductSales.sale_date) == year)
                    .group_by("hour")
                    .order_by("total")

                    )
        result = session.exec(query).all()
        return result
    
    query = (select(extract("hour", ProductSales.time).label("hour"),
                    func.sum(ProductSales.quantity * Products.unit_price).label("total")
                    )
                .where(Products.id == ProductSales.product_id)
                .group_by("hour")
                .order_by("total")

                )
    result = session.exec(query).all()
    return result



def db_summary_analysis(session: Session, year: Optional[str] = None) -> SalesSummary:

    if year:
        total_sales = (select(
                      func.sum(
                         ProductSales.quantity * Products.unit_price
                     ).label("total_sales")
                     )
                .where(Products.id == ProductSales.product_id)
                .where(extract("year",ProductSales.sale_date) == year)
                )
     
        daily_sales = (select(ProductSales.sale_date,
                        func.sum(
                            ProductSales.quantity * Products.unit_price
                        ).label("total")
                        )
                    .where(Products.id == ProductSales.product_id)
                    .where(extract("year",ProductSales.sale_date) == year)
                    .group_by(ProductSales.sale_date)
                    )
        daily_average = select(func.round(
                                func.avg(daily_sales.c.total), 2
                                ).label("avg_daily_sales")
                            )
        
        total_quantity = (select(func.sum(ProductSales.quantity).label("total_drinks"))
                    .where(extract("year",ProductSales.sale_date) == year))
        

        result = {"total_sales": session.exec(total_sales).first(),
                "avg_daily_sales": session.exec(daily_average).first(),
                "total_products_sold": session.exec(total_quantity).first()
                }

        return result


    total_sales = (select(
                    func.sum(
                        ProductSales.quantity * Products.unit_price
                    ).label("total_sales")
                    )
                .where(Products.id == ProductSales.product_id)
                )
    
    daily_sales = (select(ProductSales.sale_date,
                    func.sum(
                        ProductSales.quantity * Products.unit_price
                    ).label("total")
                    )
            .where(Products.id == ProductSales.product_id)
            .group_by(ProductSales.sale_date)
            )
    daily_average = select(func.round(
                        func.avg(daily_sales.c.total), 2
                        ).label("avg_daily_sales")
                    )
    
    total_quantity = (select(func.sum(ProductSales.quantity).label("total_drinks")))
    

    result = {"total_sales": session.exec(total_sales).first(),
            "avg_daily_sales": session.exec(daily_average).first(),
            "total_products_sold": session.exec(total_quantity).first()
            }

    return result


