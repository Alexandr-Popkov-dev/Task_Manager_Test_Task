from typing import Generator
import psycopg2
import pytest
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient
from app import models
from app.config import USER, PASSWORD, HOST
from app.tm_app import application, get_db

SQLALCHEMY_DATABASE_URL = f'postgresql://{USER}:{PASSWORD}@{HOST}/test'


@pytest.fixture(scope="session")
def connection():
    con = psycopg2.connect(dbname='postgres',
                           user=USER, host=HOST,
                           password=PASSWORD)

    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    cur.execute('DROP DATABASE IF EXISTS test')
    cur.execute("CREATE DATABASE test")

    # Создаем движок для тестовой базы
    test_engine = create_engine(SQLALCHEMY_DATABASE_URL)
    models.Base.metadata.create_all(bind=test_engine)
    return test_engine.connect()


@pytest.fixture(scope="session")
def db_session(connection):
    transaction = connection.begin()
    session_factory = sessionmaker(autocommit=False,
                                   autoflush=False,
                                   bind=connection)
    session = session_factory()
    yield session
    session.close()
    transaction.rollback()


@pytest.fixture(scope='module')
def client(db_session) -> Generator:
    def override_get_db():
        try:
            yield db_session
        finally:
            pass  # Не закрываем сессию здесь, так как это делается в фикстуре db_session

    application.dependency_overrides[get_db] = override_get_db
    with TestClient(application) as c:
        yield c
    application.dependency_overrides.clear()


@pytest.fixture()
def tasks_setup(db_session):
    # Создаем тестовую задачу
    db_task = models.Task(
        title='Test_Title',
        description='Test_Description',
        status=models.TaskStatus.PENDING.value
    )
    db_session.add(db_task)
    db_session.commit()
    return db_task.id  # Возвращаем ID созданной задачи


def test_get_tasks(client, tasks_setup):
    print('test_get_tasks')
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]['title'] == 'Test_Title'


def test_get_task_by_id(client, tasks_setup):
    print('test_get_task_by_id')
    # Получаем список задач, чтобы узнать ID созданной задачи
    response = client.get("/tasks")
    task_id = response.json()[0]['id']

    # Теперь получаем конкретную задачу по ID
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()['title'] == 'Test_Title'


def test_create_task(client):
    print('test_create_task')
    task_data = {
        "title": "New Task",
        "description": "New Description",
        "status": "Создано"
    }
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 200
    assert response.json()['title'] == 'New Task'


def test_update_task(client, tasks_setup):
    print('test_update_task')
    # Получаем список задач, чтобы узнать ID созданной задачи
    response = client.get("/tasks")
    task_id = response.json()[0]['id']

    # Обновляем задачу
    update_data = {
        "title": "Updated Title",
        "description": "Updated Description",
        "status": "В работе"
    }
    response = client.put(f"/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()['title'] == 'Updated Title'


def test_delete_task(client, tasks_setup):
    print('test_delete_task')
    # Получаем список задач, чтобы узнать ID созданной задачи
    response = client.get("/tasks")
    task_id = response.json()[0]['id']

    # Удаляем задачу
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()['message'] == 'Task deleted successfully'

    # Проверяем, что задача действительно удалена
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404
