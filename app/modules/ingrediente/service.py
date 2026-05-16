from datetime import datetime, timezone
from .unit_of_work import IngredienteUnitOfWork
from .schemas import IngredienteCreate, IngredienteUpdate
from .models import Ingrediente

def crear(uow: IngredienteUnitOfWork, ingrediente_in: IngredienteCreate):
    with uow:
        db_ingrediente = Ingrediente(**ingrediente_in.model_dump())
        return uow.ingredientes.add(db_ingrediente)

def obtener_todos(uow: IngredienteUnitOfWork, skip: int = 0, limit: int = 50):
    with uow:
        return uow.ingredientes.get_all(skip, limit)

def obtener_por_id(uow: IngredienteUnitOfWork, id: int):
    with uow:
        return uow.ingredientes.get_by_id(id)

def actualizar(uow: IngredienteUnitOfWork, id: int, ingrediente_in: IngredienteUpdate):
    with uow:
        db_ingrediente = uow.ingredientes.get_by_id(id)
        if not db_ingrediente:
            return None
        
        ingrediente_data = ingrediente_in.model_dump(exclude_unset=True)
        for key, value in ingrediente_data.items():
            setattr(db_ingrediente, key, value)
            
        db_ingrediente.updated_at = datetime.now(timezone.utc)
        return uow.ingredientes.add(db_ingrediente)

def eliminar(uow: IngredienteUnitOfWork, id: int):
    with uow:
        db_ingrediente = uow.ingredientes.get_by_id(id)
        if not db_ingrediente:
            return False
        
        uow.ingredientes.delete(db_ingrediente)
        return True