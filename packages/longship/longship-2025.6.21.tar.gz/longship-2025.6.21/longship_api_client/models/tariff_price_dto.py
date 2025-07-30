from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from ..models.tariff_price_dto_approval_status import TariffPriceDtoApprovalStatus
import datetime
from typing import Union

if TYPE_CHECKING:
    from ..models.tariff_restriction import TariffRestriction


T = TypeVar("T", bound="TariffPriceDto")


@_attrs_define
class TariffPriceDto:
    """
    Attributes:
        created_timestamp (Union[Unset, datetime.datetime]):
        valid_from (Union[Unset, datetime.datetime]):
        start_tariff (Union[Unset, float]):
        price_per_kwh (Union[Unset, float]):
        price_per_kwh_incl_vat (Union[Unset, float]):
        is_vat_relevant (Union[Unset, bool]):
        parking_tariff (Union[Unset, float]):
        parking_step_size_in_minutes (Union[Unset, int]):
        parking_grace_period_in_minutes (Union[Unset, int]):
        parking_tariff_restrictions (Union[Unset, List['TariffRestriction']]):
        time_tariff (Union[Unset, float]):
        time_step_size_in_minutes (Union[Unset, int]):
        time_grace_period_in_minutes (Union[Unset, int]):
        approval_status (Union[Unset, TariffPriceDtoApprovalStatus]):  Default: TariffPriceDtoApprovalStatus.PENDING.
    """

    created_timestamp: Union[Unset, datetime.datetime] = UNSET
    valid_from: Union[Unset, datetime.datetime] = UNSET
    start_tariff: Union[Unset, float] = UNSET
    price_per_kwh: Union[Unset, float] = UNSET
    price_per_kwh_incl_vat: Union[Unset, float] = UNSET
    is_vat_relevant: Union[Unset, bool] = UNSET
    parking_tariff: Union[Unset, float] = UNSET
    parking_step_size_in_minutes: Union[Unset, int] = UNSET
    parking_grace_period_in_minutes: Union[Unset, int] = UNSET
    parking_tariff_restrictions: Union[Unset, List["TariffRestriction"]] = UNSET
    time_tariff: Union[Unset, float] = UNSET
    time_step_size_in_minutes: Union[Unset, int] = UNSET
    time_grace_period_in_minutes: Union[Unset, int] = UNSET
    approval_status: Union[Unset, TariffPriceDtoApprovalStatus] = (
        TariffPriceDtoApprovalStatus.PENDING
    )
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        created_timestamp: Union[Unset, str] = UNSET
        if not isinstance(self.created_timestamp, Unset):
            created_timestamp = self.created_timestamp.isoformat()

        valid_from: Union[Unset, str] = UNSET
        if not isinstance(self.valid_from, Unset):
            valid_from = self.valid_from.isoformat()

        start_tariff = self.start_tariff

        price_per_kwh = self.price_per_kwh

        price_per_kwh_incl_vat = self.price_per_kwh_incl_vat

        is_vat_relevant = self.is_vat_relevant

        parking_tariff = self.parking_tariff

        parking_step_size_in_minutes = self.parking_step_size_in_minutes

        parking_grace_period_in_minutes = self.parking_grace_period_in_minutes

        parking_tariff_restrictions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.parking_tariff_restrictions, Unset):
            parking_tariff_restrictions = []
            for (
                parking_tariff_restrictions_item_data
            ) in self.parking_tariff_restrictions:
                parking_tariff_restrictions_item = (
                    parking_tariff_restrictions_item_data.to_dict()
                )
                parking_tariff_restrictions.append(parking_tariff_restrictions_item)

        time_tariff = self.time_tariff

        time_step_size_in_minutes = self.time_step_size_in_minutes

        time_grace_period_in_minutes = self.time_grace_period_in_minutes

        approval_status: Union[Unset, str] = UNSET
        if not isinstance(self.approval_status, Unset):
            approval_status = self.approval_status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_timestamp is not UNSET:
            field_dict["createdTimestamp"] = created_timestamp
        if valid_from is not UNSET:
            field_dict["validFrom"] = valid_from
        if start_tariff is not UNSET:
            field_dict["startTariff"] = start_tariff
        if price_per_kwh is not UNSET:
            field_dict["pricePerKwh"] = price_per_kwh
        if price_per_kwh_incl_vat is not UNSET:
            field_dict["pricePerKwhInclVat"] = price_per_kwh_incl_vat
        if is_vat_relevant is not UNSET:
            field_dict["isVatRelevant"] = is_vat_relevant
        if parking_tariff is not UNSET:
            field_dict["parkingTariff"] = parking_tariff
        if parking_step_size_in_minutes is not UNSET:
            field_dict["parkingStepSizeInMinutes"] = parking_step_size_in_minutes
        if parking_grace_period_in_minutes is not UNSET:
            field_dict["parkingGracePeriodInMinutes"] = parking_grace_period_in_minutes
        if parking_tariff_restrictions is not UNSET:
            field_dict["parkingTariffRestrictions"] = parking_tariff_restrictions
        if time_tariff is not UNSET:
            field_dict["timeTariff"] = time_tariff
        if time_step_size_in_minutes is not UNSET:
            field_dict["timeStepSizeInMinutes"] = time_step_size_in_minutes
        if time_grace_period_in_minutes is not UNSET:
            field_dict["timeGracePeriodInMinutes"] = time_grace_period_in_minutes
        if approval_status is not UNSET:
            field_dict["approvalStatus"] = approval_status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.tariff_restriction import TariffRestriction

        d = src_dict.copy()
        _created_timestamp = d.pop("createdTimestamp", UNSET)
        created_timestamp: Union[Unset, datetime.datetime]
        if isinstance(_created_timestamp, Unset) or _created_timestamp is None:
            created_timestamp = UNSET
        else:
            created_timestamp = isoparse(_created_timestamp)

        _valid_from = d.pop("validFrom", UNSET)
        valid_from: Union[Unset, datetime.datetime]
        if isinstance(_valid_from, Unset) or _valid_from is None:
            valid_from = UNSET
        else:
            valid_from = isoparse(_valid_from)

        start_tariff = d.pop("startTariff", UNSET)

        price_per_kwh = d.pop("pricePerKwh", UNSET)

        price_per_kwh_incl_vat = d.pop("pricePerKwhInclVat", UNSET)

        is_vat_relevant = d.pop("isVatRelevant", UNSET)

        parking_tariff = d.pop("parkingTariff", UNSET)

        parking_step_size_in_minutes = d.pop("parkingStepSizeInMinutes", UNSET)

        parking_grace_period_in_minutes = d.pop("parkingGracePeriodInMinutes", UNSET)

        parking_tariff_restrictions = []
        _parking_tariff_restrictions = d.pop("parkingTariffRestrictions", UNSET)
        for parking_tariff_restrictions_item_data in _parking_tariff_restrictions or []:
            parking_tariff_restrictions_item = TariffRestriction.from_dict(
                parking_tariff_restrictions_item_data
            )

            parking_tariff_restrictions.append(parking_tariff_restrictions_item)

        time_tariff = d.pop("timeTariff", UNSET)

        time_step_size_in_minutes = d.pop("timeStepSizeInMinutes", UNSET)

        time_grace_period_in_minutes = d.pop("timeGracePeriodInMinutes", UNSET)

        _approval_status = d.pop("approvalStatus", UNSET)
        approval_status: Union[Unset, TariffPriceDtoApprovalStatus]
        if isinstance(_approval_status, Unset) or _approval_status is None:
            approval_status = UNSET
        else:
            approval_status = TariffPriceDtoApprovalStatus(_approval_status)

        tariff_price_dto = cls(
            created_timestamp=created_timestamp,
            valid_from=valid_from,
            start_tariff=start_tariff,
            price_per_kwh=price_per_kwh,
            price_per_kwh_incl_vat=price_per_kwh_incl_vat,
            is_vat_relevant=is_vat_relevant,
            parking_tariff=parking_tariff,
            parking_step_size_in_minutes=parking_step_size_in_minutes,
            parking_grace_period_in_minutes=parking_grace_period_in_minutes,
            parking_tariff_restrictions=parking_tariff_restrictions,
            time_tariff=time_tariff,
            time_step_size_in_minutes=time_step_size_in_minutes,
            time_grace_period_in_minutes=time_grace_period_in_minutes,
            approval_status=approval_status,
        )

        tariff_price_dto.additional_properties = d
        return tariff_price_dto

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
