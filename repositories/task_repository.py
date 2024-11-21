from typing import List, Optional, Union

from fastapi import Depends
from sqlalchemy.orm import Session

from configs.database import get_db_connection
from repositories.models import Task
from repositories.base_repository import BaseRepository
from schemas.enums import TaskStatus


class TaskRepository(BaseRepository[Task, int]):
    def __init__(self, db: Session = Depends(get_db_connection)):
        super().__init__(db)

    def create(self, entity: Task) -> Task:
        """Adiciona uma nova tarefa usando o método add do repositório base."""
        return self.add(entity)

    def delete(self, entity_id: int) -> bool:
        """Exclui uma tarefa pelo ID usando delete_entity."""
        return self.delete_entity(entity_id, Task)

    def get(self, entity_id: int) -> Optional[Task]:
        """Recupera uma tarefa pelo ID."""
        return self.db.query(Task).filter(Task.id == entity_id).first()

    def list(self, limit: int = 10, offset: int = 0, status: Optional[TaskStatus] = None) -> Union[List[Task], list]:
        """Lista tarefas com suporte a paginação e filtro opcional por status."""
        query = self.db.query(Task)

        if status:
            query = query.filter(Task.status == status)

        return query.offset(offset).limit(limit).all()

    def update(self, entity_id: int, entity: Task) -> Optional[Task]:
        """Atualiza uma tarefa específica pelo ID usando update_entity e copy_attributes."""
        task = self.get(entity_id)
        if task:
            self.copy_attributes(task, entity)
            return self.update_entity(task)
        return None

    def get_by_title(self, title: str) -> Optional[Task]:
        """Busca uma tarefa pelo título."""
        return self.db.query(Task).filter(Task.title == title).first()
