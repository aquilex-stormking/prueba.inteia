from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class TipoEvento(Base):
    __tablename__ = 'tipo_evento'
    id = Column(Integer, primary_key=True)
    nombre = Column(String,unique=True)

    # Relación uno a muchos
    eventos = relationship("Evento", back_populates="tipo_evento")

class Evento(Base):
    __tablename__ = 'evento'

    id = Column(Integer, primary_key=True)
    tipo_evento_id = Column(Integer, ForeignKey('tipo_evento.id'))
    descripcion = Column(String)
    fecha = Column(Date)
    estado = Column(Enum('Pendiente', 'Revisado',name='estados'))

    # Relación inversa
    tipo_evento = relationship("TipoEvento", back_populates="eventos")

    # Campo(s) adicional(es)
    gestion = Column(String)


class Model_Program():

    def get_all_eventos(db):
        return db.query(Evento).all()
    
    def get_all_tipo_eventos(db):
        return db.query(TipoEvento).all()
    
    # Create
    def create_tipo_evento(db, tipo_evento: TipoEvento):
        db.add(tipo_evento)
        db.commit()
        db.refresh(tipo_evento)
        return tipo_evento

    def create_evento(db, evento: Evento):
        db.add(evento)
        db.commit()
        db.refresh(evento)
        return evento

    # Read
    def get_tipo_eventos(db):
        return db.query(TipoEvento).all()

    def get_eventos(db):
        return db.query(Evento).all()

    def get_evento_by_id(db, evento_id):
        return db.query(Evento).filter(Evento.id == evento_id).first()
    
    def get_tipo_evento_by_id(db, tipo_evento_id: int):
        return db.query(TipoEvento).filter(TipoEvento.id == tipo_evento_id).first()

    # Update
    def update_evento(db, evento: Evento):
        db_evento = get_evento_by_id(db, evento.id)
        if db_evento is None:
            return None
        for key, value in evento.dict().items():
            setattr(db_evento, key, value)
        db.commit()
        db.refresh(db_evento)
        return db_evento

    # Delete
    def delete_evento(db, evento_id):
        db_evento = get_evento_by_id(db, evento_id)
        if db_evento is None:
            return None
        db.delete(db_evento)
        db.commit()
        return db_evento
    
    def create_multiple_tipo_eventos(db):
        tipo_eventos = [
            TipoEvento(nombre='tipo evento1'),
            TipoEvento(nombre='tipo evento2'),
            TipoEvento(nombre='tipo evento3')
        ]

        db.add_all(tipo_eventos)
        db.commit()

        return tipo_eventos