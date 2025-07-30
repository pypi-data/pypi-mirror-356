from enum import Enum


class TariffAssertionDtoTariffType(str, Enum):
    DEFAULTTARIFF = "DefaultTariff"
    PRIVATETARIFF = "PrivateTariff"
    REIMBURSEMENTTARIFF = "ReimbursementTariff"
    SELLTARIFF = "SellTariff"

    def __str__(self) -> str:
        return str(self.value)
