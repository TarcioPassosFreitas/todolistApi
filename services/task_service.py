from typing import List, Optional, Dict

from fastapi import Depends, HTTPException

from repositories.models import Task
from repositories.task_repository import TaskRepository
from schemas.task_schema import TaskCreateSchema, TaskUpdateSchema, TaskSchema
from schemas.enums import TaskStatus


class TaskService:
    def __init__(self, repository: TaskRepository = Depends()):
        self.repository = repository

    def create_task(self, task_data: TaskCreateSchema) -> TaskSchema:
        existing_task = self.repository.get_by_title(task_data.title)
        if existing_task:
            raise HTTPException(
                status_code=400,
                detail=f"A task with title '{task_data.title}' already exists."
            )

        task = Task(**task_data.model_dump(exclude_unset=True))
        self.repository.create(task)
        return task

    def get_task(self, task_id: int) -> TaskSchema:
        task = self.repository.get(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return TaskSchema.model_validate(task.normalize())

    def list_tasks(self, status: Optional[TaskStatus] = None, limit: int = 100, offset: int = 0) -> List[TaskSchema]:
        tasks = self.repository.list(status=status, limit=limit, offset=offset)
        return [TaskSchema.model_validate(task.normalize()) for task in tasks]

    def update_task(self, task_id: int, task_data: TaskUpdateSchema) -> TaskSchema:
        task = self.repository.get(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        updated_data = task_data.model_dump(exclude_unset=True)
        if not updated_data:
            raise HTTPException(status_code=400, detail="No fields to update provided")

        for key, value in updated_data.items():
            setattr(task, key, value)

        self.repository.update(task_id, task)
        return task

    def delete_task(self, task_id: int) -> Dict[str, str | int]:
        task = self.repository.get(task_id)
        if not task:
            raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")

        if self.repository.delete(task_id):
            return {"message": f"Tarefa com ID {task_id} foi excluída com sucesso.", "task_id": task_id}

        raise HTTPException(
            status_code=500,
            detail=f"Erro ao tentar excluir a tarefa com ID {task_id}.",
        )
