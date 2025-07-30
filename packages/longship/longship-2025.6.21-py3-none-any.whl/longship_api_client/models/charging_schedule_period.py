from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="ChargingSchedulePeriod")


@_attrs_define
class ChargingSchedulePeriod:
    """
    Attributes:
        start_period (int):
        limit (float):
        number_phases (Union[Unset, int]):
    """

    start_period: int
    limit: float
    number_phases: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        start_period = self.start_period

        limit = self.limit

        number_phases = self.number_phases

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "startPeriod": start_period,
                "limit": limit,
            }
        )
        if number_phases is not UNSET:
            field_dict["numberPhases"] = number_phases

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        start_period = d.pop("startPeriod")

        limit = d.pop("limit")

        number_phases = d.pop("numberPhases", UNSET)

        charging_schedule_period = cls(
            start_period=start_period,
            limit=limit,
            number_phases=number_phases,
        )

        charging_schedule_period.additional_properties = d
        return charging_schedule_period

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
