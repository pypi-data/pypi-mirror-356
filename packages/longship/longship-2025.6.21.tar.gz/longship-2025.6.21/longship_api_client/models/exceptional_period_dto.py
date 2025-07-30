from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
import datetime
from typing import Union


T = TypeVar("T", bound="ExceptionalPeriodDto")


@_attrs_define
class ExceptionalPeriodDto:
    """
    Attributes:
        period_begin (Union[Unset, datetime.datetime]):
        period_end (Union[Unset, datetime.datetime]):
    """

    period_begin: Union[Unset, datetime.datetime] = UNSET
    period_end: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        period_begin: Union[Unset, str] = UNSET
        if not isinstance(self.period_begin, Unset):
            period_begin = self.period_begin.isoformat()

        period_end: Union[Unset, str] = UNSET
        if not isinstance(self.period_end, Unset):
            period_end = self.period_end.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if period_begin is not UNSET:
            field_dict["period_begin"] = period_begin
        if period_end is not UNSET:
            field_dict["period_end"] = period_end

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _period_begin = d.pop("period_begin", UNSET)
        period_begin: Union[Unset, datetime.datetime]
        if isinstance(_period_begin, Unset) or _period_begin is None:
            period_begin = UNSET
        else:
            period_begin = isoparse(_period_begin)

        _period_end = d.pop("period_end", UNSET)
        period_end: Union[Unset, datetime.datetime]
        if isinstance(_period_end, Unset) or _period_end is None:
            period_end = UNSET
        else:
            period_end = isoparse(_period_end)

        exceptional_period_dto = cls(
            period_begin=period_begin,
            period_end=period_end,
        )

        exceptional_period_dto.additional_properties = d
        return exceptional_period_dto

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
