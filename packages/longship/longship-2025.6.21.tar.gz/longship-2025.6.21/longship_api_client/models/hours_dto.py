from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.regular_hours_dto import RegularHoursDto
    from ..models.exceptional_period_dto import ExceptionalPeriodDto


T = TypeVar("T", bound="HoursDto")


@_attrs_define
class HoursDto:
    """
    Attributes:
        twentyfourseven (Union[Unset, bool]):
        regular_hours (Union[Unset, List['RegularHoursDto']]):
        exceptional_openings (Union[Unset, List['ExceptionalPeriodDto']]):
        exceptional_closings (Union[Unset, List['ExceptionalPeriodDto']]):
    """

    twentyfourseven: Union[Unset, bool] = UNSET
    regular_hours: Union[Unset, List["RegularHoursDto"]] = UNSET
    exceptional_openings: Union[Unset, List["ExceptionalPeriodDto"]] = UNSET
    exceptional_closings: Union[Unset, List["ExceptionalPeriodDto"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        twentyfourseven = self.twentyfourseven

        regular_hours: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.regular_hours, Unset):
            regular_hours = []
            for regular_hours_item_data in self.regular_hours:
                regular_hours_item = regular_hours_item_data.to_dict()
                regular_hours.append(regular_hours_item)

        exceptional_openings: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.exceptional_openings, Unset):
            exceptional_openings = []
            for exceptional_openings_item_data in self.exceptional_openings:
                exceptional_openings_item = exceptional_openings_item_data.to_dict()
                exceptional_openings.append(exceptional_openings_item)

        exceptional_closings: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.exceptional_closings, Unset):
            exceptional_closings = []
            for exceptional_closings_item_data in self.exceptional_closings:
                exceptional_closings_item = exceptional_closings_item_data.to_dict()
                exceptional_closings.append(exceptional_closings_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if twentyfourseven is not UNSET:
            field_dict["twentyfourseven"] = twentyfourseven
        if regular_hours is not UNSET:
            field_dict["regular_hours"] = regular_hours
        if exceptional_openings is not UNSET:
            field_dict["exceptional_openings"] = exceptional_openings
        if exceptional_closings is not UNSET:
            field_dict["exceptional_closings"] = exceptional_closings

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.regular_hours_dto import RegularHoursDto
        from ..models.exceptional_period_dto import ExceptionalPeriodDto

        d = src_dict.copy()
        twentyfourseven = d.pop("twentyfourseven", UNSET)

        regular_hours = []
        _regular_hours = d.pop("regular_hours", UNSET)
        for regular_hours_item_data in _regular_hours or []:
            regular_hours_item = RegularHoursDto.from_dict(regular_hours_item_data)

            regular_hours.append(regular_hours_item)

        exceptional_openings = []
        _exceptional_openings = d.pop("exceptional_openings", UNSET)
        for exceptional_openings_item_data in _exceptional_openings or []:
            exceptional_openings_item = ExceptionalPeriodDto.from_dict(
                exceptional_openings_item_data
            )

            exceptional_openings.append(exceptional_openings_item)

        exceptional_closings = []
        _exceptional_closings = d.pop("exceptional_closings", UNSET)
        for exceptional_closings_item_data in _exceptional_closings or []:
            exceptional_closings_item = ExceptionalPeriodDto.from_dict(
                exceptional_closings_item_data
            )

            exceptional_closings.append(exceptional_closings_item)

        hours_dto = cls(
            twentyfourseven=twentyfourseven,
            regular_hours=regular_hours,
            exceptional_openings=exceptional_openings,
            exceptional_closings=exceptional_closings,
        )

        hours_dto.additional_properties = d
        return hours_dto

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
