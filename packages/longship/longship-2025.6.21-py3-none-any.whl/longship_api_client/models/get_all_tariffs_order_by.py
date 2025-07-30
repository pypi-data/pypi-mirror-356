from enum import Enum


class GetAllTariffsOrderBy(str, Enum):
    KWH_PRICE = "kwH_PRICE"
    NAME = "name"
    START_PRICE = "starT_PRICE"

    def __str__(self) -> str:
        return str(self.value)
