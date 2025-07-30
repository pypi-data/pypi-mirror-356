from enum import Enum


class GetAllChargepointsOrderBy(str, Enum):
    MODEL = "model"
    NAME = "name"
    OUNAME = "ouname"
    SERIALNUMBER = "serialnumber"

    def __str__(self) -> str:
        return str(self.value)
