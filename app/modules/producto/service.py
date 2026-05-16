from datetime import datetime, timezone
from typing import Optional
from fastapi import HTTPException, status
from .unit_of_work import ProductoUnitOfWork
from .schemas import ProductoCreate, ProductoUpdate
from .models import Producto


def _resolver_categorias(uow: ProductoUnitOfWork, categoria_ids: list) -> list:
    """Valida que todas las categorías existan y las retorna. Lanza 404 si alguna no existe."""
    categorias = []
    for c_id in categoria_ids:
        cat = uow.categorias.get_by_id(c_id)
        if not cat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría con id {c_id} no existe"
            )
        categorias.append(cat)
    return categorias


def _resolver_ingredientes(uow: ProductoUnitOfWork, ingrediente_ids: list) -> list:
    """Valida que todos los ingredientes existan y los retorna. Silencia los no encontrados."""
    return [
        ing for i_id in ingrediente_ids
        if (ing := uow.ingredientes.get_by_id(i_id)) is not None
    ]


def crear(uow: ProductoUnitOfWork, producto_in: ProductoCreate):
    with uow:
        prod_data = producto_in.model_dump(exclude={"categoria_ids", "ingrediente_ids"})
        db_producto = Producto(**prod_data)

        # Categoría obligatoria — valida existencia de cada id
        categorias = _resolver_categorias(uow, producto_in.categoria_ids)
        db_producto.categorias.extend(categorias)

        # Ingredientes opcionales
        if producto_in.ingrediente_ids:
            ingredientes = _resolver_ingredientes(uow, producto_in.ingrediente_ids)
            db_producto.ingredientes.extend(ingredientes)

        return uow.productos.add(db_producto)


def obtener_todos(uow: ProductoUnitOfWork, skip: int, limit: int, nombre: Optional[str] = None):
    with uow:
        return uow.productos.get_all_active(skip, limit, nombre)


def obtener_por_id(uow: ProductoUnitOfWork, id: int):
    with uow:
        return uow.productos.get_by_id(id)


def eliminar(uow: ProductoUnitOfWork, id: int):
    with uow:
        db_producto = uow.productos.get_by_id(id)
        if not db_producto or db_producto.deleted_at is not None:
            return False
        db_producto.deleted_at = datetime.now(timezone.utc)
        uow.productos.add(db_producto)
        return True


def actualizar(uow: ProductoUnitOfWork, id: int, producto_in: ProductoUpdate):
    with uow:
        db_producto = uow.productos.get_by_id(id)
        if not db_producto or db_producto.deleted_at is not None:
            return None

        prod_data = producto_in.model_dump(
            exclude={"categoria_ids", "ingrediente_ids"},
            exclude_unset=True
        )
        for key, value in prod_data.items():
            setattr(db_producto, key, value)

        # Si se envían categorías, valida existencia antes de reemplazar
        if producto_in.categoria_ids is not None:
            categorias = _resolver_categorias(uow, producto_in.categoria_ids)
            db_producto.categorias.clear()
            db_producto.categorias.extend(categorias)

        if producto_in.ingrediente_ids is not None:
            ingredientes = _resolver_ingredientes(uow, producto_in.ingrediente_ids)
            db_producto.ingredientes.clear()
            db_producto.ingredientes.extend(ingredientes)

        db_producto.updated_at = datetime.now(timezone.utc)
        return uow.productos.add(db_producto)