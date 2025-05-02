import zoneinfo
from datetime import datetime
from fastapi import FastAPI
from contextlib import asynccontextmanager
from pydantic import BaseModel
from models import Customer, CustomerBase, Transaction, Invoice
from db import get_session, Session, session_dependency, create_all_tables
from sqlmodel import select

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_all_tables()
    yield

app = FastAPI(lifespan=lifespan)

country_timezones = {
    "ES": "Europe/Madrid",
    "US": "America/New_York",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "CO": "America/Bogota",
}

@app.get("/") #hay que especificar el tipo de petición en cada uno
async def root():
    return {"message": "Hello Angel"}

@app.get("/time/{iso_code}") #se especifica el tipo de petición y su variable con {}
async def get_curent_time(iso_code: str): #se convierte el tipo de dato a str
    iso = iso_code.upper() #convierte el string a mayúscula

    if iso not in country_timezones:
        return {"error": "Invalid ISO code"}
    else:
        timezone_str = country_timezones.get(iso)
        tz = zoneinfo.ZoneInfo(timezone_str)

    return {"time": datetime.now(tz)}

current_id: int = 0
db_customers: list[Customer] = []

@app.post("/customers", response_model=Customer)
async def create_customer(customer_data: CustomerBase, session: session_dependency):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@app.get("/customers", response_model=list[Customer])
async def get_customers(session: session_dependency):
    statement = select(Customer)
    customers = session.exec(statement).all()
    return customers

@app.post("/transactions")
async def create_transaction(transaction_data: Transaction):
    return transaction_data


@app.post("/invoices")
async def create_invoice(invoice_data: Invoice):
    return invoice_data