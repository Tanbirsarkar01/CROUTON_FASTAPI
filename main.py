from sqlalchemy import Column, String, Float, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#setup
DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base() 

class PotatoModel(Base):
    __tablename__ = 'potatoes'
    id = Column(Integer, primary_key=True, index=True)
    thickness = Column(Float)
    mass = Column(Float)
    color = Column(String)
    type = Column(String)

# the database tables
Base.metadata.create_all(bind=engine)

from pydantic import BaseModel

#Pydantic schema for creating a new Potato record
class PotatoCreate(BaseModel):
    thickness: float
    mass: float
    color: str
    type: str

# Define Pydantic schema for reading Potato records
class Potato(PotatoCreate):
    id: int

    class Config:
        orm_mode = True

from fastapi import FastAPI, Depends
from crouton import SQLAlchemyCRUDRouter

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create FastAPI app
app = FastAPI()

# Create the CRUD router
router = SQLAlchemyCRUDRouter(
    schema=Potato,
    create_schema=PotatoCreate,
    db_model=PotatoModel,
    db=get_db,
    prefix='potato'
)

# Include the router in the FastAPI app
app.include_router(router)