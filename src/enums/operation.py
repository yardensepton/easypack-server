from enum import Enum


class Operation(str, Enum):
    update = "update"
    remove = "remove"
    add = "add"
