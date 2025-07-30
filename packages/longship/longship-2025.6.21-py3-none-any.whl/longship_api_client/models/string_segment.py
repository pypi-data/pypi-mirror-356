from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="StringSegment")


@_attrs_define
class StringSegment:
    """
    Attributes:
        buffer (Union[Unset, str]):
        offset (Union[Unset, int]):
        length (Union[Unset, int]):
        value (Union[Unset, str]):
        has_value (Union[Unset, bool]):
    """

    buffer: Union[Unset, str] = UNSET
    offset: Union[Unset, int] = UNSET
    length: Union[Unset, int] = UNSET
    value: Union[Unset, str] = UNSET
    has_value: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        buffer = self.buffer

        offset = self.offset

        length = self.length

        value = self.value

        has_value = self.has_value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if buffer is not UNSET:
            field_dict["buffer"] = buffer
        if offset is not UNSET:
            field_dict["offset"] = offset
        if length is not UNSET:
            field_dict["length"] = length
        if value is not UNSET:
            field_dict["value"] = value
        if has_value is not UNSET:
            field_dict["hasValue"] = has_value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        buffer = d.pop("buffer", UNSET)

        offset = d.pop("offset", UNSET)

        length = d.pop("length", UNSET)

        value = d.pop("value", UNSET)

        has_value = d.pop("hasValue", UNSET)

        string_segment = cls(
            buffer=buffer,
            offset=offset,
            length=length,
            value=value,
            has_value=has_value,
        )

        string_segment.additional_properties = d
        return string_segment

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
