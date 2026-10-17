from typing import Optional
from sqlmodel import Field, SQLModel


class Hero(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secrect_name: str
    age: int = Field(default=None)


class Product(SQLModel, table=True):
    __tablename__ = "products"
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    price: float = Field(nullable=False)
    description: str | None = Field(nullable=True)
