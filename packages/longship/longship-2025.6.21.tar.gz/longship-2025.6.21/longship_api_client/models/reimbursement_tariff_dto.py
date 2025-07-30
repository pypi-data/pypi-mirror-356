from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
import datetime
from ..models.reimbursement_tariff_dto_status import ReimbursementTariffDtoStatus
from typing import Union

if TYPE_CHECKING:
    from ..models.reimbursement_price_dto import ReimbursementPriceDto


T = TypeVar("T", bound="ReimbursementTariffDto")


@_attrs_define
class ReimbursementTariffDto:
    """
    Attributes:
        id (Union[Unset, str]):
        date_created (Union[Unset, datetime.datetime]):
        valid_from (Union[Unset, datetime.datetime]):
        currency (Union[Unset, str]):
        price (Union[Unset, ReimbursementPriceDto]):
        status (Union[Unset, ReimbursementTariffDtoStatus]):  Default: ReimbursementTariffDtoStatus.PENDING.
    """

    id: Union[Unset, str] = UNSET
    date_created: Union[Unset, datetime.datetime] = UNSET
    valid_from: Union[Unset, datetime.datetime] = UNSET
    currency: Union[Unset, str] = UNSET
    price: Union[Unset, "ReimbursementPriceDto"] = UNSET
    status: Union[Unset, ReimbursementTariffDtoStatus] = (
        ReimbursementTariffDtoStatus.PENDING
    )
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        date_created: Union[Unset, str] = UNSET
        if not isinstance(self.date_created, Unset):
            date_created = self.date_created.isoformat()

        valid_from: Union[Unset, str] = UNSET
        if not isinstance(self.valid_from, Unset):
            valid_from = self.valid_from.isoformat()

        currency = self.currency

        price: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.price, Unset):
            price = self.price.to_dict()

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if date_created is not UNSET:
            field_dict["dateCreated"] = date_created
        if valid_from is not UNSET:
            field_dict["validFrom"] = valid_from
        if currency is not UNSET:
            field_dict["currency"] = currency
        if price is not UNSET:
            field_dict["price"] = price
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.reimbursement_price_dto import ReimbursementPriceDto

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _date_created = d.pop("dateCreated", UNSET)
        date_created: Union[Unset, datetime.datetime]
        if isinstance(_date_created, Unset) or _date_created is None:
            date_created = UNSET
        else:
            date_created = isoparse(_date_created)

        _valid_from = d.pop("validFrom", UNSET)
        valid_from: Union[Unset, datetime.datetime]
        if isinstance(_valid_from, Unset) or _valid_from is None:
            valid_from = UNSET
        else:
            valid_from = isoparse(_valid_from)

        currency = d.pop("currency", UNSET)

        _price = d.pop("price", UNSET)
        price: Union[Unset, ReimbursementPriceDto]
        if isinstance(_price, Unset) or _price is None:
            price = UNSET
        else:
            price = ReimbursementPriceDto.from_dict(_price)

        _status = d.pop("status", UNSET)
        status: Union[Unset, ReimbursementTariffDtoStatus]
        if isinstance(_status, Unset) or _status is None:
            status = UNSET
        else:
            status = ReimbursementTariffDtoStatus(_status)

        reimbursement_tariff_dto = cls(
            id=id,
            date_created=date_created,
            valid_from=valid_from,
            currency=currency,
            price=price,
            status=status,
        )

        reimbursement_tariff_dto.additional_properties = d
        return reimbursement_tariff_dto

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
