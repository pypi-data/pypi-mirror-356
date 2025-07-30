from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
import datetime
from typing import Union
from ..models.tariff_restriction_day_of_week import TariffRestrictionDayOfWeek


T = TypeVar("T", bound="TariffRestriction")


@_attrs_define
class TariffRestriction:
    """
    Attributes:
        start_time (Union[Unset, str]):
        end_time (Union[Unset, str]):
        start_date (Union[Unset, datetime.datetime]):
        end_date (Union[Unset, datetime.datetime]):
        day_of_week (Union[Unset, TariffRestrictionDayOfWeek]):  Default: TariffRestrictionDayOfWeek.VALUE_0.
    """

    start_time: Union[Unset, str] = UNSET
    end_time: Union[Unset, str] = UNSET
    start_date: Union[Unset, datetime.datetime] = UNSET
    end_date: Union[Unset, datetime.datetime] = UNSET
    day_of_week: Union[Unset, TariffRestrictionDayOfWeek] = (
        TariffRestrictionDayOfWeek.VALUE_0
    )
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        start_time = self.start_time

        end_time = self.end_time

        start_date: Union[Unset, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat()

        end_date: Union[Unset, str] = UNSET
        if not isinstance(self.end_date, Unset):
            end_date = self.end_date.isoformat()

        day_of_week: Union[Unset, int] = UNSET
        if not isinstance(self.day_of_week, Unset):
            day_of_week = self.day_of_week.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if start_time is not UNSET:
            field_dict["startTime"] = start_time
        if end_time is not UNSET:
            field_dict["endTime"] = end_time
        if start_date is not UNSET:
            field_dict["startDate"] = start_date
        if end_date is not UNSET:
            field_dict["endDate"] = end_date
        if day_of_week is not UNSET:
            field_dict["dayOfWeek"] = day_of_week

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        start_time = d.pop("startTime", UNSET)

        end_time = d.pop("endTime", UNSET)

        _start_date = d.pop("startDate", UNSET)
        start_date: Union[Unset, datetime.datetime]
        if isinstance(_start_date, Unset) or _start_date is None:
            start_date = UNSET
        else:
            start_date = isoparse(_start_date)

        _end_date = d.pop("endDate", UNSET)
        end_date: Union[Unset, datetime.datetime]
        if isinstance(_end_date, Unset) or _end_date is None:
            end_date = UNSET
        else:
            end_date = isoparse(_end_date)

        _day_of_week = d.pop("dayOfWeek", UNSET)
        day_of_week: Union[Unset, TariffRestrictionDayOfWeek]
        if isinstance(_day_of_week, Unset) or _day_of_week is None:
            day_of_week = UNSET
        else:
            day_of_week = TariffRestrictionDayOfWeek(_day_of_week)

        tariff_restriction = cls(
            start_time=start_time,
            end_time=end_time,
            start_date=start_date,
            end_date=end_date,
            day_of_week=day_of_week,
        )

        tariff_restriction.additional_properties = d
        return tariff_restriction

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
