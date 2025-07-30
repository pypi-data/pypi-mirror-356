from enum import Enum


class GetAllChargepointsAccesstype(str, Enum):
    GUEST = "guest"
    NEW = "new"
    PRIVATE = "private"
    PUBLIC = "public"

    def __str__(self) -> str:
        return str(self.value)
