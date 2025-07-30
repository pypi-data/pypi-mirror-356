from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="RegularHoursDto")


@_attrs_define
class RegularHoursDto:
    """
    Attributes:
        weekday (Union[Unset, int]):
        period_begin (Union[Unset, str]):
        period_end (Union[Unset, str]):
    """

    weekday: Union[Unset, int] = UNSET
    period_begin: Union[Unset, str] = UNSET
    period_end: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        weekday = self.weekday

        period_begin = self.period_begin

        period_end = self.period_end

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if weekday is not UNSET:
            field_dict["weekday"] = weekday
        if period_begin is not UNSET:
            field_dict["period_begin"] = period_begin
        if period_end is not UNSET:
            field_dict["period_end"] = period_end

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        weekday = d.pop("weekday", UNSET)

        period_begin = d.pop("period_begin", UNSET)

        period_end = d.pop("period_end", UNSET)

        regular_hours_dto = cls(
            weekday=weekday,
            period_begin=period_begin,
            period_end=period_end,
        )

        regular_hours_dto.additional_properties = d
        return regular_hours_dto

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
