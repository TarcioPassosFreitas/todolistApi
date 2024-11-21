from typing import List, Optional, Dict

from fastapi import APIRouter, Depends, status

from schemas.task_schema import TaskCreateSchema, TaskUpdateSchema, TaskSchema
from services.task_service import TaskService
from schemas.enums import TaskStatus

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post(
    "/",
    response_model=TaskSchema,
    status_code=status.HTTP_201_CREATED,
)
def add(task: TaskCreateSchema, service: TaskService = Depends()):
    """
    Cria uma nova tarefa no sistema.
    **Campos esperados**:
    - **title (str)**: O título da tarefa. **Obrigatório e único**.
    - **description (str)**: Descrição opcional da tarefa.
    - **status (int)**: O status da tarefa. Use um dos valores:
        - `1`: pending
        - `2`: in progress
        - `3`: completed
    - **created_at (datetime)**: A data de criação da tarefa.
        - **Nota**: Se não fornecido, será gerado automaticamente.
    """
    return service.create_task(task)


@router.get(
    "/",
    response_model=List[TaskSchema],
)
def get_all(
        status: Optional[TaskStatus] = None,
        limit: int = 50,
        offset: int = 0,
        service: TaskService = Depends()
):
    """
    Retorna uma lista de tarefas cadastradas no sistema.

    **Parâmetros**:
    - **status (int)**: Filtra tarefas por status (opcional). Use um dos valores:
        - `1`: pending
        - `2`: in progress
        - `3`: completed
    - **limit**: Limita o número de tarefas retornadas (padrão: 50).
    - **offset**: Define o deslocamento inicial para paginação (padrão: 0).
    """
    return service.list_tasks(status=status, limit=limit, offset=offset)


@router.get(
    "/{task_id}",
    response_model=TaskSchema,
)
def get(task_id: int, service: TaskService = Depends()):
    """
    Obtém os detalhes de uma tarefa específica.

    **Parâmetros**:
    - **task_id (int)**: O identificador único da tarefa.
    """
    return service.get_task(task_id)


@router.patch(
    "/{task_id}",
    response_model=TaskSchema,
)
def update(task_id: int, task: TaskUpdateSchema, service: TaskService = Depends()):
    """
    Atualiza os detalhes de uma tarefa existente.

     **Parâmetros**:
    - **task_id (int)**: O identificador único da tarefa.

    **Campos esperados**:
    - **title (str)**: O título atualizado da tarefa. **Opcional**.
    - **description (str)**: A descrição atualizada da tarefa. **Opcional**.
    - **status (int)**: O status atualizado da tarefa. Use um dos valores:
        - `1`: pending
        - `2`: in progress
        - `3`: completed
    """
    return service.update_task(task_id, task)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    response_description="Mensagem sobre a exclusão da tarefa."
)
def delete(task_id: int, service: TaskService = Depends()) -> Dict[str, str | int]:
    """
    Exclui uma tarefa específica do sistema.

    **Parâmetros**:
    - **task_id (int)**: O identificador único da tarefa.
    """
    return service.delete_task(task_id)
