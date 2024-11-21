from configs.database import Engine
from repositories.models.base_model import EntityMeta
from repositories.models.task_model import Task


def init():
    EntityMeta.metadata.create_all(bind=Engine)
