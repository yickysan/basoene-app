import os
from fastapi import FastAPI, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
import sqlite3
from typing import Generator
from dotenv import load_dotenv

from basoene_api.models.products import create_tables as product_tables
from basoene_api.models.rooms import create_tables as room_tables
from basoene_api.routes import product_analytics, products, rooms, sales, bookings, room_analytics

load_dotenv("db.env")

app = FastAPI()
app.include_router(products.router)
app.include_router(rooms.router)
app.include_router(sales.router)
app.include_router(bookings.router)
app.include_router(product_analytics.router)
app.include_router(room_analytics.router)

origns = [
    "https://basoenesnug.vercel.app" 
    os.environ["origins"]
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origns,
    allow_credentials = True,
    allow_headers = ["*"],
    allow_methods = ["*"]
)


@app.on_event("startup")
async def create_tables():
        product_tables()
        room_tables()

   



@app.get("/")
async def home():
    return {"Message": "Welcome!"}



