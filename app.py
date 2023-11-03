from fastapi import FastAPI, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
import json
from typing import Generator

from basoene_api.routes import product_analytics, products, rooms, sales, bookings, room_analytics


app = FastAPI()
app.include_router(products.router)
app.include_router(rooms.router)
app.include_router(sales.router)
app.include_router(bookings.router)
app.include_router(product_analytics.router)
app.include_router(room_analytics.router)

origns = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origns,
    allow_credentials = True,
    allow_headers = ["*"],
    allow_methods = ["*"]
)



