import os
import sys
import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Adiciona o diretório raiz ao PYTHONPATH
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Carrega variáveis de ambiente do .env
dotenv_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path)

from main import app  # Importa o app após corrigir o caminho
from repositories.models import EntityMeta
from configs.database import get_db_connection

# Configuração do banco de dados SQLite em memória para testes
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def setup_database():
    """
    Configura o banco de dados para testes (criação e destruição de tabelas).
    """
    EntityMeta.metadata.create_all(bind=engine)
    yield
    EntityMeta.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db(setup_database):
    """
    Gera uma nova sessão do banco para cada teste.
    """
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function", autouse=True)
def clear_database(db):
    """
    Limpa os dados do banco antes de cada teste.
    """
    for table in reversed(EntityMeta.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()


@pytest.fixture(scope="function")
def api_client(db):
    """
    Substitui a dependência do banco pela sessão de teste.
    """
    app.dependency_overrides[get_db_connection] = lambda: db
    return TestClient(app)
