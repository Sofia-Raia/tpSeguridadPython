from fastapi import APIRouter, HTTPException, Path, Query, status, Depends
from sqlmodel import Session
from typing import List

from . import schemas, service
from .unit_of_work import CategoriaUnitOfWork
from app.core.database import get_session

router = APIRouter(prefix="/categorias", tags=["Categorías"])


def get_categoria_uow(session: Session = Depends(get_session)) -> CategoriaUnitOfWork:
    return CategoriaUnitOfWork(session)


# ── CREATE ────────────────────────────────────────────────────────────────────

@router.post(
    "/",
    response_model=schemas.RespuestaEstandar[schemas.CategoriaRead],
    status_code=status.HTTP_201_CREATED,
    summary="Crear categoría (raíz o nodo hijo)",
)
def alta_categoria(
    categoria: schemas.CategoriaCreate,
    uow: CategoriaUnitOfWork = Depends(get_categoria_uow),
):
    """
    - Sin `parent_id` → categoría raíz.
    - Con `parent_id` → subcategoría del nodo indicado.
    """
    nuevo = service.crear(uow, categoria)
    return {"message": "Categoría creada", "data": nuevo}


# ── READ: lista plana ─────────────────────────────────────────────────────────

@router.get(
    "/",
    response_model=schemas.RespuestaEstandar[List[schemas.CategoriaRead]],
    summary="Listar todas las categorías (plano)",
)
def listar_categorias(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, le=100),
    uow: CategoriaUnitOfWork = Depends(get_categoria_uow),
):
    categorias = service.obtener_todos(uow, skip, limit)
    return {"message": "Lista de categorías", "data": categorias}


# ── READ: solo raíces ─────────────────────────────────────────────────────────

@router.get(
    "/roots",
    response_model=schemas.RespuestaEstandar[List[schemas.CategoriaRead]],
    summary="Listar categorías raíz (sin padre)",
)
def listar_roots(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, le=100),
    uow: CategoriaUnitOfWork = Depends(get_categoria_uow),
):
    roots = service.obtener_roots(uow, skip, limit)
    return {"message": "Categorías raíz", "data": roots}


# ── READ: árbol completo ──────────────────────────────────────────────────────

@router.get(
    "/tree",
    response_model=schemas.RespuestaEstandar[List[schemas.CategoriaTree]],
    summary="Árbol completo de categorías (recursivo)",
)
def obtener_arbol(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, le=100),
    uow: CategoriaUnitOfWork = Depends(get_categoria_uow),
):
    """
    Devuelve las categorías raíz con todo su árbol de subcategorías anidadas.
    Cada nodo incluye el campo `subcategorias` con sus hijos directos,
    que a su vez contienen los suyos, y así recursivamente.
    """
    arbol = service.obtener_arbol(uow, skip, limit)
    return {"message": "Árbol de categorías", "data": arbol}


# ── READ: detalle de un nodo ──────────────────────────────────────────────────

@router.get(
    "/{id}",
    response_model=schemas.RespuestaEstandar[schemas.CategoriaTree],
    status_code=status.HTTP_200_OK,
    summary="Detalle de categoría con sus subcategorías directas",
)
def detalle_categoria(
    id: int = Path(..., gt=0),
    uow: CategoriaUnitOfWork = Depends(get_categoria_uow),
):
    categoria = service.obtener_por_id(uow, id)
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    return {"message": "Categoría encontrada", "data": categoria}


# ── READ: hijos directos ──────────────────────────────────────────────────────

@router.get(
    "/{id}/hijos",
    response_model=schemas.RespuestaEstandar[List[schemas.CategoriaRead]],
    status_code=status.HTTP_200_OK,
    summary="Hijos directos de una categoría",
)
def listar_hijos(
    id: int = Path(..., gt=0),
    uow: CategoriaUnitOfWork = Depends(get_categoria_uow),
):
    padre = service.obtener_por_id(uow, id)
    if not padre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    hijos = service.obtener_hijos(uow, id)
    return {"message": f"Hijos de la categoría {id}", "data": hijos}


# ── UPDATE ────────────────────────────────────────────────────────────────────

@router.put(
    "/{id}",
    response_model=schemas.RespuestaEstandar[schemas.CategoriaRead],
    status_code=status.HTTP_200_OK,
    summary="Actualizar categoría (puede reasignar padre)",
)
def actualizar_categoria(
    categoria: schemas.CategoriaUpdate,
    id: int = Path(..., gt=0),
    uow: CategoriaUnitOfWork = Depends(get_categoria_uow),
):
    try:
        actualizado = service.actualizar(uow, id, categoria)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not actualizado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    return {"message": "Categoría actualizada con éxito", "data": actualizado}


# ── DELETE ────────────────────────────────────────────────────────────────────

@router.delete(
    "/{id}",
    response_model=schemas.RespuestaEstandar[None],
    status_code=status.HTTP_200_OK,
    summary="Eliminar categoría",
)
def borrar_categoria(
    id: int = Path(..., gt=0),
    uow: CategoriaUnitOfWork = Depends(get_categoria_uow),
):
    eliminado = service.eliminar(uow, id)
    if not eliminado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    return {"message": "Categoría eliminada con éxito", "data": None}
