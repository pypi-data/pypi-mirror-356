from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union
from ..models.image_dto_category import ImageDtoCategory


T = TypeVar("T", bound="ImageDto")


@_attrs_define
class ImageDto:
    """
    Attributes:
        url (Union[Unset, str]):
        thumbnail (Union[Unset, str]):
        category (Union[Unset, ImageDtoCategory]):  Default: ImageDtoCategory.CHARGER.
        type (Union[Unset, str]):
        width (Union[Unset, int]):
        height (Union[Unset, int]):
    """

    url: Union[Unset, str] = UNSET
    thumbnail: Union[Unset, str] = UNSET
    category: Union[Unset, ImageDtoCategory] = ImageDtoCategory.CHARGER
    type: Union[Unset, str] = UNSET
    width: Union[Unset, int] = UNSET
    height: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        url = self.url

        thumbnail = self.thumbnail

        category: Union[Unset, str] = UNSET
        if not isinstance(self.category, Unset):
            category = self.category.value

        type = self.type

        width = self.width

        height = self.height

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if thumbnail is not UNSET:
            field_dict["thumbnail"] = thumbnail
        if category is not UNSET:
            field_dict["category"] = category
        if type is not UNSET:
            field_dict["type"] = type
        if width is not UNSET:
            field_dict["width"] = width
        if height is not UNSET:
            field_dict["height"] = height

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        if src_dict is None:
            return UNSET
        d = src_dict.copy()
        url = d.pop("url", UNSET)

        thumbnail = d.pop("thumbnail", UNSET)

        _category = d.pop("category", UNSET)
        category: Union[Unset, ImageDtoCategory]
        if isinstance(_category, Unset) or _category is None:
            category = UNSET
        else:
            category = ImageDtoCategory(_category)

        type = d.pop("type", UNSET)

        width = d.pop("width", UNSET)

        height = d.pop("height", UNSET)

        image_dto = cls(
            url=url,
            thumbnail=thumbnail,
            category=category,
            type=type,
            width=width,
            height=height,
        )

        image_dto.additional_properties = d
        return image_dto

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
