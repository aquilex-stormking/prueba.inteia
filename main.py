from fastapi import FastAPI,Depends,HTTPException
from models.model import Model_Program,Base, Evento ,TipoEvento
from shemas import schema 
from utils.connection import engine
from routers.allrouters import router
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine

app = FastAPI()

app.include_router(router)

@app.on_event("startup")
async def startup():
    # Crea las tablas si no existen
    Base.metadata.create_all(bind=engine)