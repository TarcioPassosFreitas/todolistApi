import pytest
from fastapi.testclient import TestClient
from faker import Faker
from main import app

faker = Faker()


@pytest.fixture
def client():
    return TestClient(app)


def test_create_task(client):
    """
    Testa a criação de uma tarefa válida.
    """
    title = faker.sentence(nb_words=3)
    description = faker.text()
    response = client.post(
        "/tasks/",
        json={"title": title, "description": description, "status": "PENDING"}
    )
    assert response.status_code == 201, response.text

    task = response.json()
    assert task["title"] == title
    assert task["description"] == description
    assert task["status"] == "PENDING"


def test_create_task_invalid_data(client):
    """
    Testa a criação de uma tarefa com dados inválidos.
    """
    response = client.post(
        "/tasks/",
        json={"title": "", "description": "This task has no title"}
    )
    assert response.status_code == 422


def test_list_tasks(client):
    """
    Testa a listagem de todas as tarefas.
    """
    tasks = [
        {"title": faker.sentence(nb_words=3), "description": faker.text(), "status": "PENDING"},
        {"title": faker.sentence(nb_words=3), "description": faker.text(), "status": "IN_PROGRESS"},
    ]
    for task in tasks:
        client.post("/tasks/", json=task)

    response = client.get("/tasks/")
    assert response.status_code == 200, response.text

    response_tasks = response.json()
    assert len(response_tasks) >= len(tasks)
    assert response_tasks[-2]["status"] == "PENDING"
    assert response_tasks[-1]["status"] == "IN_PROGRESS"


def test_list_tasks_with_status_filter(client):
    """
    Testa a listagem de tarefas filtradas pelo status.
    """
    pending_task = {"title": faker.sentence(nb_words=3), "description": faker.text(), "status": "PENDING"}
    completed_task = {"title": faker.sentence(nb_words=3), "description": faker.text(), "status": "COMPLETED"}

    client.post("/tasks/", json=pending_task)
    client.post("/tasks/", json=completed_task)

    response = client.get("/tasks/?status=PENDING")
    assert response.status_code == 200, response.text
    tasks = response.json()
    assert len(tasks) >= 1
    for task in tasks:
        assert task["status"] == "PENDING"


def test_get_task(client):
    """
    Testa a busca de uma tarefa específica pelo ID.
    """
    title = faker.sentence(nb_words=3)
    description = faker.text()
    create_response = client.post(
        "/tasks/",
        json={"title": title, "description": description, "status": "PENDING"}
    )
    assert create_response.status_code == 201, create_response.text

    task_id = create_response.json().get("id")
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200, response.text
    task = response.json()
    assert task["id"] == task_id
    assert task["title"] == title
    assert task["description"] == description
    assert task["status"] == "PENDING"


def test_get_task_not_found(client):
    """
    Testa a busca de uma tarefa inexistente.
    """
    response = client.get("/tasks/99999")
    assert response.status_code == 404
