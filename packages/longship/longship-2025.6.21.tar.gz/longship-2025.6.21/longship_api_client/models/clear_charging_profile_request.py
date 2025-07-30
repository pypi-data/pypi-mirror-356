from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union
from ..models.clear_charging_profile_request_charging_profile_purpose import (
    ClearChargingProfileRequestChargingProfilePurpose,
)


T = TypeVar("T", bound="ClearChargingProfileRequest")


@_attrs_define
class ClearChargingProfileRequest:
    """
    Attributes:
        id (Union[Unset, int]):
        connector_id (Union[Unset, int]):
        charging_profile_purpose (Union[Unset, ClearChargingProfileRequestChargingProfilePurpose]):  Default:
            ClearChargingProfileRequestChargingProfilePurpose.CHARGEPOINTMAXPROFILE.
        stack_level (Union[Unset, int]):
    """

    id: Union[Unset, int] = UNSET
    connector_id: Union[Unset, int] = UNSET
    charging_profile_purpose: Union[
        Unset, ClearChargingProfileRequestChargingProfilePurpose
    ] = ClearChargingProfileRequestChargingProfilePurpose.CHARGEPOINTMAXPROFILE
    stack_level: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        connector_id = self.connector_id

        charging_profile_purpose: Union[Unset, str] = UNSET
        if not isinstance(self.charging_profile_purpose, Unset):
            charging_profile_purpose = self.charging_profile_purpose.value

        stack_level = self.stack_level

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if connector_id is not UNSET:
            field_dict["connectorId"] = connector_id
        if charging_profile_purpose is not UNSET:
            field_dict["chargingProfilePurpose"] = charging_profile_purpose
        if stack_level is not UNSET:
            field_dict["stackLevel"] = stack_level

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        connector_id = d.pop("connectorId", UNSET)

        _charging_profile_purpose = d.pop("chargingProfilePurpose", UNSET)
        charging_profile_purpose: Union[
            Unset, ClearChargingProfileRequestChargingProfilePurpose
        ]
        if isinstance(_charging_profile_purpose, Unset) or _charging_profile_purpose is None:
            charging_profile_purpose = UNSET
        else:
            charging_profile_purpose = (
                ClearChargingProfileRequestChargingProfilePurpose(
                    _charging_profile_purpose
                )
            )

        stack_level = d.pop("stackLevel", UNSET)

        clear_charging_profile_request = cls(
            id=id,
            connector_id=connector_id,
            charging_profile_purpose=charging_profile_purpose,
            stack_level=stack_level,
        )

        clear_charging_profile_request.additional_properties = d
        return clear_charging_profile_request

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
