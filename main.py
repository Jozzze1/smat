from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SMAT Persistente")



class EstacionCreate(BaseModel):
    id: int
    nombre: str
    ubicacion: str

class LecturaCreate(BaseModel):
    estacion_id: int
    valor: float



@app.post("/estaciones/", status_code=201)
def crear_estacion(estacion: EstacionCreate, db: Session = Depends(get_db)):
    nueva_estacion = models.EstacionDB(
        id=estacion.id,
        nombre=estacion.nombre,
        ubicacion=estacion.ubicacion
    )
    db.add(nueva_estacion)
    db.commit()
    db.refresh(nueva_estacion)

    return {"msg": "Estación guardada en DB", "data": nueva_estacion}


@app.post("/lecturas/", status_code=201)
def registrar_lectura(lectura: LecturaCreate, db: Session = Depends(get_db)):

    estacion = db.query(models.EstacionDB).filter(
        models.EstacionDB.id == lectura.estacion_id
    ).first()

    if not estacion:
        raise HTTPException(status_code=404, detail="Estación no existe")

    nueva_lectura = models.LecturaDB(
        valor=lectura.valor,
        estacion_id=lectura.estacion_id
    )

    db.add(nueva_lectura)
    db.commit()

    return {"status": "Lectura guardada en DB"}



@app.get("/estaciones/{id}/historial")
def obtener_historial(id: int, db: Session = Depends(get_db)):

    estacion = db.query(models.EstacionDB).filter(
        models.EstacionDB.id == id
    ).first()

    if not estacion:
        raise HTTPException(status_code=404, detail="Estación no encontrada")

    lecturas_db = db.query(models.LecturaDB).filter(
        models.LecturaDB.estacion_id == id
    ).all()

    valores = [l.valor for l in lecturas_db]

    conteo = len(valores)
    promedio = sum(valores) / conteo if conteo > 0 else 0.0

    return {
        "estacion_id": id,
        "lecturas": valores,
        "conteo": conteo,
        "promedio": promedio
    }
@app.get("/estaciones/{id}/historial")
def obtener_historial(id: int, db: Session = Depends(get_db)):

    
    estacion = db.query(models.EstacionDB).filter(
        models.EstacionDB.id == id
    ).first()

    if not estacion:
        raise HTTPException(status_code=404, detail="Estación no encontrada")

   
    lecturas_db = db.query(models.LecturaDB).filter(
        models.LecturaDB.estacion_id == id
    ).all()

   
    valores = [l.valor for l in lecturas_db]

    conteo = len(valores)
    promedio = sum(valores) / conteo if conteo > 0 else 0.0

   
    return {
        "estacion_id": id,
        "lecturas": valores,
        "conteo": conteo,
        "promedio": promedio
    }
