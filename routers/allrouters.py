from fastapi import APIRouter,Depends,HTTPException
from models.model import Model_Program
from utils import connection
from utils.connection import engine
from sqlalchemy.orm import Session
from models.model import Model_Program,Base, Evento ,TipoEvento
from shemas import schema 

router = APIRouter()

@router.on_event("startup")
async def startup():
    # Crea las tablas si no existen
    Base.metadata.create_all(bind=engine)

#GET
#trae eventos
@router.get("/eventos")
async def get_all_eventos(db: Session = Depends(connection.get_db)):
    eventos = Model_Program.get_all_eventos(db)
    return eventos

@router.get("/eventos/{id}")
async def get_all_evento_id(id:int,db: Session = Depends(connection.get_db)):
    eventos = Model_Program.get_evento_by_id(db,id)
    return eventos

#GET
#trae eventos
@router.get("/tipodeeventos")
async def get_all_eventos(db: Session = Depends(connection.get_db)):
    tipoeventos = Model_Program.get_all_tipo_eventos(db)
    return tipoeventos

@router.get("/tipodeeventos/{id}")
async def get_all_tipo_evento_id(id:int,db: Session = Depends(connection.get_db)):
    tipoeventos = Model_Program.get_tipo_evento_by_id(db,id)
    return tipoeventos

# POST
#Crea tiposdeevento
@router.post("/tipoevento", response_model = schema.TipoEventoBase)
async def post(tipe_event_found: schema.TipoEventoCreate, db: Session = Depends(connection.get_db)):

    tipoevento = TipoEvento(nombre = tipe_event_found.nombre)
    Model_Program.create_tipo_evento(db,tipoevento)
    raise HTTPException(status_code=200, detail=f" Tipo Evento creado con exito ")


# POST
#Crea evento
@router.post("/evento", response_model=schema.EventoBase)
async def post(event_found: schema.EventoCreate, db: Session = Depends(connection.get_db)):
    campo = 'Sin gestión'
    if event_found.tipo_evento_id in [1, 3]:
        campo = 'Requiere gestión'
    
    if event_found.estado not in ["Pendiente", "Revisado"]:
        raise HTTPException(status_code=400, detail=f"El estado debe ser Pendiente o Revisado")

    evento = Evento(tipo_evento_id = event_found.tipo_evento_id,
                    descripcion = event_found.descripcion,
                    fecha = event_found.fecha,
                    estado = event_found.estado,
                    gestion = campo)
    Model_Program.create_evento(db,evento)
    
    raise HTTPException(status_code=200, detail=f"Evento creado con exito ")


# PUT
#Edita evento
@router.put("/evento/{id}", response_model=schema.EventoBase)
async def post(id: int, event_found: schema.EventoCreate, db: Session = Depends(connection.get_db)):
    
    evento =  Model_Program.get_evento_by_id(db,id)
    gestion = 'Sin gestión'

    if event_found.tipo_evento_id in [1, 3]:
        gestion = 'Requiere gestión'

    if evento:
        evento.tipo_evento_id = event_found.tipo_evento_id
        evento.descripcion = event_found.descripcion
        evento.fecha = event_found.fecha
        evento.estado = event_found.estado
        evento.gestion = gestion
        db.commit()
        db.refresh(evento)
    
    if not evento:
        raise HTTPException(status_code=404, detail=f"Evento con ID {id} no encontrado")
    
    raise HTTPException(status_code=200, detail=f"Evento con ID {id} fue editado con exito ")

# PUT
#Edita tipo de evento
@router.put("/tipoevento/{id}", response_model=schema.TipoEventoBase)
async def post(id: int, event_found: schema.TipoEventoCreate, db: Session = Depends(connection.get_db)):
    
    tipoevento =  Model_Program.get_tipo_evento_by_id(db,id)
    

    if tipoevento:
        tipoevento.nombre = event_found.nombre
        db.commit()
        db.refresh(tipoevento)        
    
    if not tipoevento:
        raise HTTPException(status_code=404, detail=f" Tipo de evento con ID {id} no encontrado")
    
    raise HTTPException(status_code=200, detail=f"Tipo de Evento con ID {id} fue editado con exito ")

# DELETE
#Elimina evento
@router.delete("/evento/{id}")
async def post(id: int,  db: Session = Depends(connection.get_db)):
    evento =  Model_Program.get_evento_by_id(db,id)
    if evento:
        db.delete(evento)
        db.commit()

    if not evento:
        raise HTTPException(status_code=404, detail=f" Evento con ID {id} no encontrado")

    raise HTTPException(status_code=200, detail=f"Evento con ID {id} fue editado con exito ")

# DELETE
#Elimina evento
@router.delete("/tipoevento/{id}")
async def post(id: int,  db: Session = Depends(connection.get_db)):
    tipoevento =  Model_Program.get_tipo_evento_by_id(db,id)
    if tipoevento:
        db.delete(tipoevento)
        db.commit()

    if not tipoevento:
        raise HTTPException(status_code=404, detail=f"Tipo de Evento con ID {id} no encontrado")

    raise HTTPException(status_code=200, detail=f"Tipo de Evento con ID {id} fue eliminado con exito ")