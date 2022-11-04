from enum import Enum


class PostCheckKind(Enum):
    NO_CHANGE = 0
    NEW = 1
    MODIFIED = 2
    DRAFT = 3
