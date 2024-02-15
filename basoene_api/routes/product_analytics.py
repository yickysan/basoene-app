from fastapi import APIRouter
from fastapi import Response, Depends, HTTPException
from sqlmodel import Session, select, func, extract
from typing import Generator
from datetime import date
from basoene_api.models.products import Products, ProductSales, engine
from basoene_api.models.product_analysis import DateResults, ProductResults, HourResults, DayResults, MonthResults, SalesSummary
from basoene_api.db.product_analytics import(
     db_product_analysis,
     db_trend_analysis,
     db_month_analysis,
     db_daily_analysis,
     db_hourly_analysis,
     db_summary_analysis
)

router = APIRouter()


def get_session() -> Generator[Session, None, None]:
    with Session(engine, autoflush=True) as session:
        yield session

@router.get("/analysis/product", response_model=list[ProductResults])
async def product_analysis(session: Session = Depends(get_session)):
     return db_product_analysis(session)


@router.get("/analysis/product/date", response_model=list[DateResults])
async def trend_analysis(session: Session = Depends(get_session)):
    return db_trend_analysis(session)


@router.get("/analysis/product/month", response_model=list[MonthResults])
async def month_analysis(session: Session = Depends(get_session)):
     return db_month_analysis(session)



@router.get("/analysis/product/day", response_model=list[DayResults])
async def daily_analysis(session: Session = Depends(get_session)):
     return db_daily_analysis(session)


@router.get("/analysis/product/hour", response_model=list[HourResults])
async def hourly_analysis(session: Session = Depends(get_session)):
     return db_hourly_analysis(session)


@router.get("/analysis/product/summary", response_model=SalesSummary)
async def summary_analysis(session: Session = Depends(get_session)):
     return db_summary_analysis(session)


# Return analytics results for specific years.
# Contains the same data as the routes above
# While the routes above returns every data from the data base
# The below routes return data for the year passed as ann argument.

@router.get("/analysis/product/{year}", response_model=list[ProductResults])
async def product_analysis(year: str, session: Session = Depends(get_session)):
    return db_product_analysis(session, year)


@router.get("/analysis/product/date/{year}", response_model=list[DateResults])
async def trend_analysis(year: str, session: Session = Depends(get_session)):
     return db_trend_analysis(session, year)


@router.get("/analysis/product/month/{year}", response_model=list[MonthResults])
async def month_analysis(year: str, session: Session = Depends(get_session)):
    return db_month_analysis(session, year)


@router.get("/analysis/product/day/{year}", response_model=list[DayResults])
async def daily_analysis(year: str, session: Session = Depends(get_session)):
     return db_daily_analysis(session, year)


@router.get("/analysis/product/hour/{year}", response_model=list[HourResults])
async def hourly_analysis(year: str, session: Session = Depends(get_session)):
     return db_hourly_analysis(session, year)


@router.get("/analysis/product/summary/{year}", response_model=SalesSummary)
async def summary_analysis(year: str, session: Session = Depends(get_session)):
     return db_summary_analysis(session, year)


