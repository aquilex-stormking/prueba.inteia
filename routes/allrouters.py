from fastapi import APIRouter,Depends
from models.model import Model_Program
from utils import connection
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/eventos")
async def get_all_eventos(db: Session = Depends(connection.get_db)):
    return Model_Program.get_all_eventos(db)