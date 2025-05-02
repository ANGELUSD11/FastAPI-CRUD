import zoneinfo
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from sqlmodel import SQLModel, Field

class CustomerBase(SQLModel):
    name: str = Field(default=None)
    description: str | None = Field(default=None) # | indica que puede ser None o str, es opcional
    email: str = Field(default=None)
    phone: int = Field(default=None)

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class Transaction(BaseModel):
    id: int
    amount: int
    description: str

class Invoice(BaseModel):
    id: int
    customer: Customer
    transactions: list[Transaction]
    total: int

    @property
    def total(self):
        return sum(transaction.amount for transaction in self.transactions)