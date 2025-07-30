from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.publish_token_type_dto_type import PublishTokenTypeDtoType
from typing import Union


T = TypeVar("T", bound="PublishTokenTypeDto")


@_attrs_define
class PublishTokenTypeDto:
    """
    Attributes:
        uid (Union[Unset, str]):
        type (Union[Unset, PublishTokenTypeDtoType]):  Default: PublishTokenTypeDtoType.RFID.
        visual_number (Union[Unset, str]):
        issuer (Union[Unset, str]):
        group_id (Union[Unset, str]):
    """

    uid: Union[Unset, str] = UNSET
    type: Union[Unset, PublishTokenTypeDtoType] = PublishTokenTypeDtoType.RFID
    visual_number: Union[Unset, str] = UNSET
    issuer: Union[Unset, str] = UNSET
    group_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        uid = self.uid

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        visual_number = self.visual_number

        issuer = self.issuer

        group_id = self.group_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uid is not UNSET:
            field_dict["uid"] = uid
        if type is not UNSET:
            field_dict["type"] = type
        if visual_number is not UNSET:
            field_dict["visual_number"] = visual_number
        if issuer is not UNSET:
            field_dict["issuer"] = issuer
        if group_id is not UNSET:
            field_dict["group_id"] = group_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        uid = d.pop("uid", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, PublishTokenTypeDtoType]
        if isinstance(_type, Unset) or _type is None:
            type = UNSET
        else:
            type = PublishTokenTypeDtoType(_type)

        visual_number = d.pop("visual_number", UNSET)

        issuer = d.pop("issuer", UNSET)

        group_id = d.pop("group_id", UNSET)

        publish_token_type_dto = cls(
            uid=uid,
            type=type,
            visual_number=visual_number,
            issuer=issuer,
            group_id=group_id,
        )

        publish_token_type_dto.additional_properties = d
        return publish_token_type_dto

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
