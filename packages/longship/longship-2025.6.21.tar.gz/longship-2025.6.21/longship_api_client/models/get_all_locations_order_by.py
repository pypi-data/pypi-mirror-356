from enum import Enum


class GetAllLocationsOrderBy(str, Enum):
    ADDRESS = "address"
    NAME = "name"
    OUNAME = "ouname"

    def __str__(self) -> str:
        return str(self.value)
