from sqlmodel import Session, create_engine, SQLModel
from typing import Annotated
from fastapi import Depends

sqlite_name : str = "db.sqlite3"
sqlite_url: str = f"sqlite:///{sqlite_name}"

engine = create_engine(url=sqlite_url)

def create_all_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

session_dependency = Annotated[Session, Depends(get_session)]