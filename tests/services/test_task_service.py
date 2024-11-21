import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from faker import Faker
from schemas.task_schema import TaskCreateSchema, TaskUpdateSchema
from schemas.enums import TaskStatus
from services.task_service import TaskService
from repositories.models.task_model import Task

faker = Faker()


@pytest.fixture
def mock_repository():
    """
    Mock do repositório para uso nos testes de TaskService.
    """
    return MagicMock()


@pytest.fixture
def task_service(mock_repository):
    """
    Instância de TaskService com repositório mockado.
    """
    return TaskService(repository=mock_repository)


def test_create_task(task_service, mock_repository):
    """
    Testa a criação de uma nova tarefa com título único.
    """
    mock_repository.get_by_title.return_value = None
    mock_repository.create.return_value = Task(
        id=1,
        title=faker.sentence(nb_words=3),
        description=faker.text(),
        status=TaskStatus.PENDING,
    )

    task_data = TaskCreateSchema(
        title=mock_repository.create.return_value.title,
        description=mock_repository.create.return_value.description,
    )
    created_task = task_service.create_task(task_data)

    assert created_task.title == task_data.title
    assert created_task.description == task_data.description
    mock_repository.get_by_title.assert_called_once_with(task_data.title)
    mock_repository.create.assert_called_once()


def test_create_task_with_existing_title(task_service, mock_repository):
    """
    Testa a criação de uma tarefa com título duplicado.
    """
    existing_task_title = faker.sentence(nb_words=3)
    mock_repository.get_by_title.return_value = Task(
        id=1, title=existing_task_title, description=faker.text(), status=TaskStatus.PENDING
    )

    task_data = TaskCreateSchema(title=existing_task_title)
    with pytest.raises(HTTPException) as exc_info:
        task_service.create_task(task_data)

    assert exc_info.value.status_code == 400
    assert "already exists" in str(exc_info.value.detail)
    mock_repository.get_by_title.assert_called_once_with(existing_task_title)


def test_get_task(task_service, mock_repository):
    """
    Testa a recuperação de uma tarefa existente por ID.
    """
    mock_repository.get.return_value = Task(
        id=1, title=faker.sentence(nb_words=3), description=faker.text(), status=TaskStatus.PENDING
    )

    task = task_service.get_task(1)

    assert task.id == 1
    assert task.title == mock_repository.get.return_value.title
    mock_repository.get.assert_called_once_with(1)


def test_get_task_not_found(task_service, mock_repository):
    """
    Testa a recuperação de uma tarefa inexistente.
    """
    mock_repository.get.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        task_service.get_task(999)

    assert exc_info.value.status_code == 404
    assert "Task not found" in str(exc_info.value.detail)
    mock_repository.get.assert_called_once_with(999)


def test_list_tasks(task_service, mock_repository):
    """
    Testa a listagem de todas as tarefas.
    """
    mock_repository.list.return_value = [
        Task(id=1, title=faker.sentence(nb_words=3), description=faker.text(), status=TaskStatus.PENDING),
        Task(id=2, title=faker.sentence(nb_words=3), description=faker.text(), status=TaskStatus.COMPLETED),
    ]

    tasks = task_service.list_tasks()

    assert len(tasks) == 2
    assert tasks[0].title == mock_repository.list.return_value[0].title
    assert tasks[1].title == mock_repository.list.return_value[1].title
    mock_repository.list.assert_called_once()


def test_update_task(task_service, mock_repository):
    """
    Testa a atualização de uma tarefa existente.
    """
    mock_repository.get.return_value = Task(
        id=1, title=faker.sentence(nb_words=3), description=faker.text(), status=TaskStatus.PENDING
    )
    mock_repository.update.return_value = Task(
        id=1, title=faker.sentence(nb_words=3), description=faker.text(), status=TaskStatus.COMPLETED
    )

    update_data = TaskUpdateSchema(
        title=mock_repository.update.return_value.title,
        description=mock_repository.update.return_value.description,
        status=mock_repository.update.return_value.status,
    )
    updated_task = task_service.update_task(1, update_data)

    assert updated_task.title == update_data.title
    assert updated_task.description == update_data.description
    assert updated_task.status == update_data.status
    mock_repository.get.assert_called_once_with(1)
    mock_repository.update.assert_called_once()


def test_update_task_not_found(task_service, mock_repository):
    """
    Testa a atualização de uma tarefa inexistente.
    """
    mock_repository.get.return_value = None

    update_data = TaskUpdateSchema(title=faker.sentence(nb_words=3))
    with pytest.raises(HTTPException) as exc_info:
        task_service.update_task(999, update_data)

    assert exc_info.value.status_code == 404
    assert "Task not found" in str(exc_info.value.detail)
    mock_repository.get.assert_called_once_with(999)


def test_delete_task(task_service, mock_repository):
    """
    Testa a exclusão de uma tarefa existente.
    """
    mock_repository.get.return_value = Task(
        id=1, title=faker.sentence(nb_words=3), description=faker.text(), status=TaskStatus.PENDING
    )
    mock_repository.delete.return_value = True

    result = task_service.delete_task(1)

    assert result["task_id"] == 1
    assert "excluída com sucesso" in result["message"]
    mock_repository.get.assert_called_once_with(1)
    mock_repository.delete.assert_called_once_with(1)


def test_delete_task_not_found(task_service, mock_repository):
    """
    Testa a exclusão de uma tarefa inexistente.
    """
    mock_repository.get.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        task_service.delete_task(999)

    assert exc_info.value.status_code == 404
    assert "Task with id 999 not found" in str(exc_info.value.detail)
    mock_repository.get.assert_called_once_with(999)
