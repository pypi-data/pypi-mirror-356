from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.display_text_dto import DisplayTextDto


T = TypeVar("T", bound="AdditionalGeoLocationDto")


@_attrs_define
class AdditionalGeoLocationDto:
    """
    Attributes:
        latitude (Union[Unset, str]):
        longitude (Union[Unset, str]):
        name (Union[Unset, DisplayTextDto]):
    """

    latitude: Union[Unset, str] = UNSET
    longitude: Union[Unset, str] = UNSET
    name: Union[Unset, "DisplayTextDto"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        latitude = self.latitude

        longitude = self.longitude

        name: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.name, Unset):
            name = self.name.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if latitude is not UNSET:
            field_dict["latitude"] = latitude
        if longitude is not UNSET:
            field_dict["longitude"] = longitude
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.display_text_dto import DisplayTextDto

        d = src_dict.copy()
        latitude = d.pop("latitude", UNSET)

        longitude = d.pop("longitude", UNSET)

        _name = d.pop("name", UNSET)
        name: Union[Unset, DisplayTextDto]
        if isinstance(_name, Unset) or _name is None:
            name = UNSET
        else:
            name = DisplayTextDto.from_dict(_name)

        additional_geo_location_dto = cls(
            latitude=latitude,
            longitude=longitude,
            name=name,
        )

        additional_geo_location_dto.additional_properties = d
        return additional_geo_location_dto

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
