from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
import datetime
from typing import Union


T = TypeVar("T", bound="ChargepointConfigurationItemsDto")


@_attrs_define
class ChargepointConfigurationItemsDto:
    """
    Attributes:
        id (Union[Unset, str]):
        read_only (Union[Unset, bool]):
        value (Union[Unset, str]):
        created (Union[Unset, datetime.datetime]):
        modified (Union[Unset, datetime.datetime]):
        deleted (Union[Unset, datetime.datetime]):
    """

    id: Union[Unset, str] = UNSET
    read_only: Union[Unset, bool] = UNSET
    value: Union[Unset, str] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    modified: Union[Unset, datetime.datetime] = UNSET
    deleted: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        read_only = self.read_only

        value = self.value

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        modified: Union[Unset, str] = UNSET
        if not isinstance(self.modified, Unset):
            modified = self.modified.isoformat()

        deleted: Union[Unset, str] = UNSET
        if not isinstance(self.deleted, Unset):
            deleted = self.deleted.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if read_only is not UNSET:
            field_dict["readOnly"] = read_only
        if value is not UNSET:
            field_dict["value"] = value
        if created is not UNSET:
            field_dict["created"] = created
        if modified is not UNSET:
            field_dict["modified"] = modified
        if deleted is not UNSET:
            field_dict["deleted"] = deleted

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        read_only = d.pop("readOnly", UNSET)

        value = d.pop("value", UNSET)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset) or _created is None:
            created = UNSET
        else:
            created = isoparse(_created)

        _modified = d.pop("modified", UNSET)
        modified: Union[Unset, datetime.datetime]
        if isinstance(_modified, Unset) or _modified is None:
            modified = UNSET
        else:
            modified = isoparse(_modified)

        _deleted = d.pop("deleted", UNSET)
        deleted: Union[Unset, datetime.datetime]
        if isinstance(_deleted, Unset) or _deleted is None:
            deleted = UNSET
        else:
            deleted = isoparse(_deleted)

        chargepoint_configuration_items_dto = cls(
            id=id,
            read_only=read_only,
            value=value,
            created=created,
            modified=modified,
            deleted=deleted,
        )

        chargepoint_configuration_items_dto.additional_properties = d
        return chargepoint_configuration_items_dto

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
