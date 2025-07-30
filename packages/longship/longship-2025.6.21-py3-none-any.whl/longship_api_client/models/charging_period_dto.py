from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
import datetime
from typing import Union


T = TypeVar("T", bound="ChargingPeriodDto")


@_attrs_define
class ChargingPeriodDto:
    """
    Attributes:
        timestamp (Union[Unset, datetime.datetime]):
        delta_kwh (Union[Unset, float]):
        absolute_kwh (Union[Unset, float]):
        price (Union[Unset, float]):
        parking_time_minutes (Union[Unset, float]):
    """

    timestamp: Union[Unset, datetime.datetime] = UNSET
    delta_kwh: Union[Unset, float] = UNSET
    absolute_kwh: Union[Unset, float] = UNSET
    price: Union[Unset, float] = UNSET
    parking_time_minutes: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        timestamp: Union[Unset, str] = UNSET
        if not isinstance(self.timestamp, Unset):
            timestamp = self.timestamp.isoformat()

        delta_kwh = self.delta_kwh

        absolute_kwh = self.absolute_kwh

        price = self.price

        parking_time_minutes = self.parking_time_minutes

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if delta_kwh is not UNSET:
            field_dict["deltaKwh"] = delta_kwh
        if absolute_kwh is not UNSET:
            field_dict["absoluteKwh"] = absolute_kwh
        if price is not UNSET:
            field_dict["price"] = price
        if parking_time_minutes is not UNSET:
            field_dict["parkingTimeMinutes"] = parking_time_minutes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _timestamp = d.pop("timestamp", UNSET)
        timestamp: Union[Unset, datetime.datetime]
        if isinstance(_timestamp, Unset) or _timestamp is None:
            timestamp = UNSET
        else:
            timestamp = isoparse(_timestamp)

        delta_kwh = d.pop("deltaKwh", UNSET)

        absolute_kwh = d.pop("absoluteKwh", UNSET)

        price = d.pop("price", UNSET)

        parking_time_minutes = d.pop("parkingTimeMinutes", UNSET)

        charging_period_dto = cls(
            timestamp=timestamp,
            delta_kwh=delta_kwh,
            absolute_kwh=absolute_kwh,
            price=price,
            parking_time_minutes=parking_time_minutes,
        )

        charging_period_dto.additional_properties = d
        return charging_period_dto

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
