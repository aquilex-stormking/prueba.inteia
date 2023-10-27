from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import Settings, get_settings
from fastapi import Depends
from models.model import Model_Program
from sqlalchemy.exc import IntegrityError

# Create a Declarative Meta instance
Base = declarative_base()
settings = get_settings()
engine = create_engine(f"postgresql://{settings.DB_UID}:{settings.DB_PWD}@{settings.DB_SERVER}:{settings.DB_PORT}/{settings.DB_NAME}")

# DB Dependency
def get_db(settings: Settings = Depends(get_settings)): 
   
    # Create engine
    
    Base.metadata.create_all(bind=engine)
    # Create Session
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    

    try:
        db = session_local()
        try:
            Model_Program.create_multiple_tipo_eventos(db)
            db.close()
        except IntegrityError:
            db.rollback()
            return {"error": "El nombre del tipo de evento ya existe."}
        yield db
    finally:
        db.close()