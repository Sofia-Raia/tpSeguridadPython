from datetime import datetime, timezone
from typing import List, Optional

from .unit_of_work import CategoriaUnitOfWork
from .schemas import CategoriaCreate, CategoriaUpdate
from .models import Categoria


def crear(uow: CategoriaUnitOfWork, categoria_in: CategoriaCreate) -> Categoria:
    """Crea una categoría. Si tiene parent_id es subcategoría, si no es raíz."""
    with uow:
        db_categoria = Categoria(**categoria_in.model_dump())
        return uow.categorias.add(db_categoria)


def obtener_todos(uow: CategoriaUnitOfWork, skip: int = 0, limit: int = 50) -> List[Categoria]:
    """Lista plana de todas las categorías (raíces + nodos)."""
    with uow:
        return uow.categorias.get_all(skip, limit)


def obtener_roots(uow: CategoriaUnitOfWork, skip: int = 0, limit: int = 50) -> List[Categoria]:
    """Lista solo las categorías raíz (sin padre)."""
    with uow:
        return uow.categorias.get_roots(skip, limit)


def obtener_arbol(uow: CategoriaUnitOfWork, skip: int = 0, limit: int = 50) -> List[Categoria]:
    """
    Devuelve las raíces con todo el árbol de subcategorías anidadas.
    La carga recursiva la hace SQLAlchemy via selectin lazy loading.
    """
    with uow:
        return uow.categorias.get_full_tree(skip, limit)


def obtener_por_id(uow: CategoriaUnitOfWork, id: int) -> Optional[Categoria]:
    """Obtiene una categoría por id (incluye su lista de subcategorías directas)."""
    with uow:
        return uow.categorias.get_by_id(id)


def obtener_hijos(uow: CategoriaUnitOfWork, parent_id: int) -> List[Categoria]:
    """Devuelve los hijos directos de una categoría."""
    with uow:
        return uow.categorias.get_children(parent_id)


def actualizar(uow: CategoriaUnitOfWork, id: int, categoria_in: CategoriaUpdate) -> Optional[Categoria]:
    with uow:
        db_categoria = uow.categorias.get_by_id(id)
        if not db_categoria:
            return None

        # Evitar que una categoría se asigne a sí misma como padre
        data = categoria_in.model_dump(exclude_unset=True)
        if data.get("parent_id") == id:
            raise ValueError("Una categoría no puede ser su propio padre.")

        for key, value in data.items():
            setattr(db_categoria, key, value)
        db_categoria.updated_at = datetime.now(timezone.utc)
        return uow.categorias.add(db_categoria)


def eliminar(uow: CategoriaUnitOfWork, id: int) -> bool:
    with uow:
        db_categoria = uow.categorias.get_by_id(id)
        if not db_categoria:
            return False
        uow.categorias.delete(db_categoria)
        return True
