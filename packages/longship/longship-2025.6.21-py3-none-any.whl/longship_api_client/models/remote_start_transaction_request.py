from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.charging_profile import ChargingProfile


T = TypeVar("T", bound="RemoteStartTransactionRequest")


@_attrs_define
class RemoteStartTransactionRequest:
    """
    Attributes:
        id_tag (str):
        connector_id (Union[Unset, int]):
        charging_profile (Union[Unset, ChargingProfile]):
    """

    id_tag: str
    connector_id: Union[Unset, int] = UNSET
    charging_profile: Union[Unset, "ChargingProfile"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_tag = self.id_tag

        connector_id = self.connector_id

        charging_profile: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.charging_profile, Unset):
            charging_profile = self.charging_profile.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "idTag": id_tag,
            }
        )
        if connector_id is not UNSET:
            field_dict["connectorId"] = connector_id
        if charging_profile is not UNSET:
            field_dict["chargingProfile"] = charging_profile

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.charging_profile import ChargingProfile

        d = src_dict.copy()
        id_tag = d.pop("idTag")

        connector_id = d.pop("connectorId", UNSET)

        _charging_profile = d.pop("chargingProfile", UNSET)
        charging_profile: Union[Unset, ChargingProfile]
        if isinstance(_charging_profile, Unset) or _charging_profile is None:
            charging_profile = UNSET
        else:
            charging_profile = ChargingProfile.from_dict(_charging_profile)

        remote_start_transaction_request = cls(
            id_tag=id_tag,
            connector_id=connector_id,
            charging_profile=charging_profile,
        )

        remote_start_transaction_request.additional_properties = d
        return remote_start_transaction_request

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
