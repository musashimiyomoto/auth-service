from enum import StrEnum, auto


class ActionEnum(StrEnum):
    CREATE = auto()
    READ = auto()
    UPDATE = auto()
    DELETE = auto()


class ResourceEnum(StrEnum):
    USER = auto()
    PERMISSION = auto()
