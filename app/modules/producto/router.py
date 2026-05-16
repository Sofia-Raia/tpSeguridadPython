from fastapi import APIRouter, HTTPException, Path, Query, status, Depends
from sqlmodel import Session
from typing import List, Annotated, Optional

from . import schemas, service
from .unit_of_work import ProductoUnitOfWork
from app.core.database import get_session
from app.modules.categoria.schemas import RespuestaEstandar

router = APIRouter(prefix="/productos", tags=["Productos"])

def get_producto_uow(session: Session = Depends(get_session)) -> ProductoUnitOfWork:
    return ProductoUnitOfWork(session)

@router.post(
    "/",
    response_model=RespuestaEstandar[schemas.ProductoRead],
    status_code=status.HTTP_201_CREATED,
    responses={
        404: {"description": "Una o más categorías no existen"},
        422: {"description": "categoria_ids es obligatorio y debe tener al menos un elemento"},
    }
)
def alta_producto(producto: schemas.ProductoCreate, uow: ProductoUnitOfWork = Depends(get_producto_uow)):
    nuevo = service.crear(uow, producto)
    return {"message": "Producto creado", "data": nuevo}

@router.get("/", response_model=RespuestaEstandar[List[schemas.ProductoRead]])
def listar_productos(
    skip: Annotated[int, Query(ge=0, description="Omitir registros")] = 0,
    limit: Annotated[int, Query(le=100, description="Límite registros")] = 50,
    nombre: Annotated[Optional[str], Query(description="Filtrar por nombre")] = None,
    uow: ProductoUnitOfWork = Depends(get_producto_uow)
):
    productos = service.obtener_todos(uow, skip, limit, nombre)
    return {"message": "Productos listados", "data": productos}

@router.get("/{id}", response_model=RespuestaEstandar[schemas.ProductoRead], status_code=status.HTTP_200_OK)
def detalle_producto(id: int = Path(..., gt=0), uow: ProductoUnitOfWork = Depends(get_producto_uow)):
    producto = service.obtener_por_id(uow, id)
    if not producto or producto.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return {"message": "Producto encontrado", "data": producto}

@router.put(
    "/{id}",
    response_model=RespuestaEstandar[schemas.ProductoRead],
    status_code=status.HTTP_200_OK,
    responses={
        404: {"description": "Producto o categoría no encontrada"},
        422: {"description": "categoria_ids no puede ser lista vacía si se envía"},
    }
)
def actualizar_producto(producto: schemas.ProductoUpdate, id: int = Path(..., gt=0), uow: ProductoUnitOfWork = Depends(get_producto_uow)):
    actualizado = service.actualizar(uow, id, producto)
    if not actualizado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return {"message": "Producto actualizado con éxito", "data": actualizado}

@router.delete("/{id}", response_model=RespuestaEstandar[None], status_code=status.HTTP_200_OK)
def borrar_producto(id: int = Path(..., gt=0), uow: ProductoUnitOfWork = Depends(get_producto_uow)):
    eliminado = service.eliminar(uow, id)
    if not eliminado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return {"message": "Producto eliminado con éxito", "data": None}