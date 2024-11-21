from enum import Enum


class TaskStatus(Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

    @staticmethod
    def from_value(value):
        if isinstance(value, int):
            mapping = {1: "PENDING", 2: "IN_PROGRESS", 3: "COMPLETED"}
            return TaskStatus(mapping[value])
        return TaskStatus(value)
