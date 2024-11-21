from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from configs.environment import get_environment_variables

env = get_environment_variables()


def postgres_db_url():
    return f"{env.DATABASE_DIALECT}://{env.DATABASE_USERNAME}:{env.DATABASE_PASSWORD}@{env.DATABASE_HOSTNAME}:{env.DATABASE_PORT}/{env.DATABASE_NAME}"


def sqlite_db_url():
    return f"{env.DATABASE_DIALECT}:///{env.DATABASE_NAME}"


DATABASE_URL = sqlite_db_url()

if env.DATABASE_DIALECT == "postgresql":
    DATABASE_URL = postgres_db_url()

# Create Database Engine
Engine = create_engine(
    DATABASE_URL, echo=env.DEBUG_MODE, future=True
)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=Engine
)


def get_db_connection():
    db = scoped_session(SessionLocal)
    try:
        yield db
    finally:
        db.close()
