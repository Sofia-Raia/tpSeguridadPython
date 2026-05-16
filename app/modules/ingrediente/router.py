from fastapi import APIRouter, HTTPException, Path, Query, status, Depends
from sqlmodel import Session
from typing import List

from . import schemas, service
from .unit_of_work import IngredienteUnitOfWork
from app.core.database import get_session
# Importamos la RespuestaEstandar (asumiendo que la dejaste en categorias como hicimos antes)
from app.modules.categoria.schemas import RespuestaEstandar 

router = APIRouter(prefix="/ingredientes", tags=["Ingredientes"])

def get_ingrediente_uow(session: Session = Depends(get_session)) -> IngredienteUnitOfWork:
    return IngredienteUnitOfWork(session)

@router.post("/", response_model=RespuestaEstandar[schemas.IngredienteRead], status_code=status.HTTP_201_CREATED)
def alta_ingrediente(ingrediente: schemas.IngredienteCreate, uow: IngredienteUnitOfWork = Depends(get_ingrediente_uow)):
    nuevo = service.crear(uow, ingrediente)
    return {"message": "Ingrediente creado con éxito", "data": nuevo}

@router.get("/", response_model=RespuestaEstandar[List[schemas.IngredienteRead]], status_code=status.HTTP_200_OK)
def listar_ingredientes(skip: int = Query(0, ge=0), limit: int = Query(50, le=100), uow: IngredienteUnitOfWork = Depends(get_ingrediente_uow)):
    ingredientes = service.obtener_todos(uow, skip, limit)
    return {"message": "Ingredientes listados con éxito", "data": ingredientes}

@router.get("/{id}", response_model=RespuestaEstandar[schemas.IngredienteRead], status_code=status.HTTP_200_OK)
def detalle_ingrediente(id: int = Path(..., gt=0), uow: IngredienteUnitOfWork = Depends(get_ingrediente_uow)):
    ingrediente = service.obtener_por_id(uow, id)
    if not ingrediente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingrediente no encontrado")
    return {"message": "Ingrediente encontrado", "data": ingrediente}

@router.put("/{id}", response_model=RespuestaEstandar[schemas.IngredienteRead], status_code=status.HTTP_200_OK)
def actualizar_ingrediente(ingrediente: schemas.IngredienteUpdate, id: int = Path(..., gt=0), uow: IngredienteUnitOfWork = Depends(get_ingrediente_uow)):
    actualizado = service.actualizar(uow, id, ingrediente)
    if not actualizado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingrediente no encontrado")
    return {"message": "Ingrediente actualizado con éxito", "data": actualizado}

@router.delete("/{id}", response_model=RespuestaEstandar[None], status_code=status.HTTP_200_OK)
def borrar_ingrediente(id: int = Path(..., gt=0), uow: IngredienteUnitOfWork = Depends(get_ingrediente_uow)):
    eliminado = service.eliminar(uow, id)
    if not eliminado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingrediente no encontrado")
    return {"message": "Ingrediente eliminado con éxito", "data": None}