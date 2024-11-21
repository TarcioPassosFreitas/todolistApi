from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar, Optional, Type

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from repositories.helpers.db_operations import copy_attributes, RepositoryDBException

T = TypeVar("T")
ID = TypeVar("ID")


class BaseRepository(ABC, Generic[T, ID]):
    def __init__(self, db: Session):
        self.db = db

    def add(self, entity: T) -> T:
        """Adiciona uma nova entidade ao banco de dados."""
        try:
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
            return entity
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryDBException(
                original_exception=e,
                message="Erro ao salvar no banco de dados"
            ) from e

    def delete_entity(self, entity_id: ID, model: Type[T]) -> bool:
        """Exclui uma entidade do banco de dados pelo ID."""
        try:
            entity = self.db.get(model, entity_id)
            if entity:
                self.db.delete(entity)
                self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryDBException(
                original_exception=e,
                message="Erro ao deletar do banco de dados"
            ) from e

    def update_entity(self, entity: T) -> T:
        """Atualiza uma entidade no banco de dados."""
        try:
            self.db.commit()
            self.db.refresh(entity)
            return entity
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryDBException(
                original_exception=e,
                message="Erro ao atualizar o banco de dados"
            ) from e

    def copy_attributes(self, target: T, source: T):
        """Copia atributos de uma entidade para outra."""
        copy_attributes(target, source)

    @abstractmethod
    def create(self, entity: T) -> T:
        pass

    @abstractmethod
    def delete(self, entity_id: ID) -> None:
        pass

    @abstractmethod
    def get(self, entity_id: ID) -> Optional[T]:
        pass

    @abstractmethod
    def list(self, limit: int = 10, offset: int = 0) -> List[T]:
        pass

    @abstractmethod
    def update(self, entity_id: ID, entity: T) -> T:
        pass
