from enum import Enum


class Action(str, Enum):
    update = "update"
    remove = "remove"
    add = "add"
