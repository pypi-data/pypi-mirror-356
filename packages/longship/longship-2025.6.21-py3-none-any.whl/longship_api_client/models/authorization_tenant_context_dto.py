from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="AuthorizationTenantContextDto")


@_attrs_define
class AuthorizationTenantContextDto:
    """
    Attributes:
        hubject_priority (Union[Unset, int]):
        hubject_enabled (Union[Unset, bool]):
        hubject_fast_approval (Union[Unset, bool]):
    """

    hubject_priority: Union[Unset, int] = UNSET
    hubject_enabled: Union[Unset, bool] = UNSET
    hubject_fast_approval: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        hubject_priority = self.hubject_priority

        hubject_enabled = self.hubject_enabled

        hubject_fast_approval = self.hubject_fast_approval

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if hubject_priority is not UNSET:
            field_dict["hubjectPriority"] = hubject_priority
        if hubject_enabled is not UNSET:
            field_dict["hubjectEnabled"] = hubject_enabled
        if hubject_fast_approval is not UNSET:
            field_dict["hubjectFastApproval"] = hubject_fast_approval

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        hubject_priority = d.pop("hubjectPriority", UNSET)

        hubject_enabled = d.pop("hubjectEnabled", UNSET)

        hubject_fast_approval = d.pop("hubjectFastApproval", UNSET)

        authorization_tenant_context_dto = cls(
            hubject_priority=hubject_priority,
            hubject_enabled=hubject_enabled,
            hubject_fast_approval=hubject_fast_approval,
        )

        authorization_tenant_context_dto.additional_properties = d
        return authorization_tenant_context_dto

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
