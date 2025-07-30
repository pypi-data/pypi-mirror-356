from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.authorization_charger_context_dto import (
        AuthorizationChargerContextDto,
    )
    from ..models.authorization_tenant_context_dto import AuthorizationTenantContextDto


T = TypeVar("T", bound="AuthorizationContextDetailsDto")


@_attrs_define
class AuthorizationContextDetailsDto:
    """
    Attributes:
        charger (Union[Unset, AuthorizationChargerContextDto]):
        tenant (Union[Unset, AuthorizationTenantContextDto]):
    """

    charger: Union[Unset, "AuthorizationChargerContextDto"] = UNSET
    tenant: Union[Unset, "AuthorizationTenantContextDto"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        charger: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.charger, Unset):
            charger = self.charger.to_dict()

        tenant: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.tenant, Unset):
            tenant = self.tenant.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if charger is not UNSET:
            field_dict["charger"] = charger
        if tenant is not UNSET:
            field_dict["tenant"] = tenant

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.authorization_charger_context_dto import (
            AuthorizationChargerContextDto,
        )
        from ..models.authorization_tenant_context_dto import (
            AuthorizationTenantContextDto,
        )

        d = src_dict.copy()
        _charger = d.pop("charger", UNSET)
        charger: Union[Unset, AuthorizationChargerContextDto]
        if isinstance(_charger, Unset) or _charger is None:
            charger = UNSET
        else:
            charger = AuthorizationChargerContextDto.from_dict(_charger)

        _tenant = d.pop("tenant", UNSET)
        tenant: Union[Unset, AuthorizationTenantContextDto]
        if isinstance(_tenant, Unset) or _tenant is None:
            tenant = UNSET
        else:
            tenant = AuthorizationTenantContextDto.from_dict(_tenant)

        authorization_context_details_dto = cls(
            charger=charger,
            tenant=tenant,
        )

        authorization_context_details_dto.additional_properties = d
        return authorization_context_details_dto

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
