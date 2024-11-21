import pytest
from faker import Faker
from repositories.models import Task
from repositories.task_repository import TaskRepository
from schemas.enums import TaskStatus

faker = Faker()


def test_create_task(db):
    """
    Testa a criação de uma nova tarefa no repositório.
    """
    repository = TaskRepository(db)
    task = Task(
        title=faker.sentence(nb_words=3),
        description=faker.text(),
        status=TaskStatus.PENDING
    )
    created_task = repository.create(task)

    assert created_task.id is not None
    assert created_task.title == task.title
    assert created_task.description == task.description
    assert created_task.status == TaskStatus.PENDING


def test_get_task(db):
    """
    Testa a recuperação de uma tarefa existente pelo ID.
    """
    repository = TaskRepository(db)

    task = Task(
        title=faker.sentence(nb_words=3),
        description=faker.text(),
        status=TaskStatus.IN_PROGRESS
    )
    created_task = repository.create(task)

    fetched_task = repository.get(created_task.id)

    assert fetched_task is not None
    assert fetched_task.id == created_task.id
    assert fetched_task.title == task.title
    assert fetched_task.description == task.description
    assert fetched_task.status == TaskStatus.IN_PROGRESS


def test_list_tasks(db):
    """
    Testa a listagem de todas as tarefas no repositório.
    """
    repository = TaskRepository(db)

    task_1 = Task(title=faker.sentence(nb_words=3), description=faker.text(), status=TaskStatus.PENDING)
    task_2 = Task(title=faker.sentence(nb_words=3), description=faker.text(), status=TaskStatus.COMPLETED)
    db.add(task_1)
    db.add(task_2)
    db.commit()

    tasks = repository.list()

    assert len(tasks) >= 2
    assert any(task.title == task_1.title for task in tasks)
    assert any(task.title == task_2.title for task in tasks)


def test_update_task(db):
    """
    Testa a atualização de uma tarefa existente no repositório.
    """
    repository = TaskRepository(db)

    task = Task(
        title=faker.sentence(nb_words=3),
        description=faker.text(),
        status=TaskStatus.PENDING
    )
    created_task = repository.create(task)

    updated_title = faker.sentence(nb_words=3)
    updated_description = faker.text()
    created_task.title = updated_title
    created_task.description = updated_description
    created_task.status = TaskStatus.COMPLETED

    updated_task = repository.update(created_task.id, created_task)

    assert updated_task is not None
    assert updated_task.id == created_task.id
    assert updated_task.title == updated_title
    assert updated_task.description == updated_description
    assert updated_task.status == TaskStatus.COMPLETED


def test_delete_task(db):
    """
    Testa a exclusão de uma tarefa existente no repositório.
    """
    repository = TaskRepository(db)

    task = Task(
        title=faker.sentence(nb_words=3),
        description=faker.text(),
        status=TaskStatus.PENDING
    )
    created_task = repository.create(task)

    is_deleted = repository.delete(created_task.id)

    assert is_deleted is True
    assert repository.get(created_task.id) is None
