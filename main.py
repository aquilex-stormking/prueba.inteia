from routes.allrouters import router
from fastapi import FastAPI,Depends,HTTPException
from models.model import Model_Program,Base, Evento ,TipoEvento
from shemas import schema 
from utils import connection
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError


app = FastAPI()

engine = create_engine('postgresql://postgres:12345678@bd_postgres:5432/eventos')

@app.on_event("startup")
async def startup():
    # Crea las tablas si no existen
    
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        Model_Program.create_multiple_tipo_eventos(db)
        db.close()
    except IntegrityError:
        db.rollback()
        return {"error": "El nombre del tipo de evento ya existe."}


#GET
#trae eventos
@app.get("/eventos")
async def get_all_eventos(db: Session = Depends(connection.get_db)):
    return Model_Program.get_all_eventos(db)

@app.get("/eventos/{id}")
async def get_all_evento_id(id:int,db: Session = Depends(connection.get_db)):
    return Model_Program.get_evento_by_id(db,id)

#GET
#trae eventos
@app.get("/tipodeeventos")
async def get_all_eventos(db: Session = Depends(connection.get_db)):
    return Model_Program.get_all_tipo_eventos(db)

@app.get("/tipodeeventos/{id}")
async def get_all_tipo_evento_id(id:int,db: Session = Depends(connection.get_db)):
    return Model_Program.get_tipo_evento_by_id(db,id)

# POST
#Crea tiposdeevento
@app.post("/tipoevento", response_model = schema.TipoEventoBase)
async def post(tipe_event_found: schema.TipoEventoCreate, db: Session = Depends(connection.get_db)):

    tipoevento = TipoEvento(nombre = tipe_event_found.nombre)
    return Model_Program.create_tipo_evento(db,tipoevento)


# POST
#Crea evento
@app.post("/evento", response_model=schema.EventoBase)
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
    
    return Model_Program.create_evento(db,evento)


# PUT
#Edita evento
@app.put("/evento/{id}", response_model=schema.EventoBase)
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
    
    return evento

# PUT
#Edita tipo de evento
@app.put("/tipoevento/{id}", response_model=schema.TipoEventoBase)
async def post(id: int, event_found: schema.TipoEventoCreate, db: Session = Depends(connection.get_db)):
    
    tipoevento =  Model_Program.get_tipo_evento_by_id(db,id)
    

    if tipoevento:
        tipoevento.nombre = event_found.nombre
        db.commit()
        db.refresh(tipoevento)        
    
    if not tipoevento:
        raise HTTPException(status_code=404, detail=f" Tipo de evento con ID {id} no encontrado")
    
    return tipoevento

# DELETE
#Elimina evento
@app.delete("/evento/{id}")
async def post(id: int,  db: Session = Depends(connection.get_db)):
    evento =  Model_Program.get_evento_by_id(db,id)
    if evento:
        db.delete(evento)
        db.commit()

    if not evento:
        raise HTTPException(status_code=404, detail=f" Evento con ID {id} no encontrado")

    raise HTTPException(status_code=200, detail=f"Evento con ID {id} fue eliminado con exito ")