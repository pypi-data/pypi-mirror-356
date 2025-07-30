from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.string_segment import StringSegment


T = TypeVar("T", bound="EntityTagHeaderValue")


@_attrs_define
class EntityTagHeaderValue:
    """
    Attributes:
        tag (Union[Unset, StringSegment]):
        is_weak (Union[Unset, bool]):
    """

    tag: Union[Unset, "StringSegment"] = UNSET
    is_weak: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        tag: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.tag, Unset):
            tag = self.tag.to_dict()

        is_weak = self.is_weak

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if tag is not UNSET:
            field_dict["tag"] = tag
        if is_weak is not UNSET:
            field_dict["isWeak"] = is_weak

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.string_segment import StringSegment

        d = src_dict.copy()
        _tag = d.pop("tag", UNSET)
        tag: Union[Unset, StringSegment]
        if isinstance(_tag, Unset) or _tag is None:
            tag = UNSET
        else:
            tag = StringSegment.from_dict(_tag)

        is_weak = d.pop("isWeak", UNSET)

        entity_tag_header_value = cls(
            tag=tag,
            is_weak=is_weak,
        )

        entity_tag_header_value.additional_properties = d
        return entity_tag_header_value

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
