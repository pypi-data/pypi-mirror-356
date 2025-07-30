from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union
from ..models.started_by_token_dto_auth_method import StartedByTokenDtoAuthMethod
from ..models.started_by_token_dto_token_type import StartedByTokenDtoTokenType


T = TypeVar("T", bound="StartedByTokenDto")


@_attrs_define
class StartedByTokenDto:
    """
    Attributes:
        uid (Union[Unset, str]):
        auth_reference (Union[Unset, str]):
        token_type (Union[Unset, StartedByTokenDtoTokenType]):  Default: StartedByTokenDtoTokenType.AD_HOC_USER.
        contract_id (Union[Unset, str]):
        auth_method (Union[Unset, StartedByTokenDtoAuthMethod]):  Default: StartedByTokenDtoAuthMethod.AUTH_REQUEST.
        provider_country_code (Union[Unset, str]):
        provider_party_id (Union[Unset, str]):
        token_ou_id (Union[Unset, str]):
        token_ou_name (Union[Unset, str]):
        token_ou (Union[Unset, str]):
    """

    uid: Union[Unset, str] = UNSET
    auth_reference: Union[Unset, str] = UNSET
    token_type: Union[Unset, StartedByTokenDtoTokenType] = (
        StartedByTokenDtoTokenType.AD_HOC_USER
    )
    contract_id: Union[Unset, str] = UNSET
    auth_method: Union[Unset, StartedByTokenDtoAuthMethod] = (
        StartedByTokenDtoAuthMethod.AUTH_REQUEST
    )
    provider_country_code: Union[Unset, str] = UNSET
    provider_party_id: Union[Unset, str] = UNSET
    token_ou_id: Union[Unset, str] = UNSET
    token_ou_name: Union[Unset, str] = UNSET
    token_ou: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        uid = self.uid

        auth_reference = self.auth_reference

        token_type: Union[Unset, str] = UNSET
        if not isinstance(self.token_type, Unset):
            token_type = self.token_type.value

        contract_id = self.contract_id

        auth_method: Union[Unset, str] = UNSET
        if not isinstance(self.auth_method, Unset):
            auth_method = self.auth_method.value

        provider_country_code = self.provider_country_code

        provider_party_id = self.provider_party_id

        token_ou_id = self.token_ou_id

        token_ou_name = self.token_ou_name

        token_ou = self.token_ou

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uid is not UNSET:
            field_dict["uid"] = uid
        if auth_reference is not UNSET:
            field_dict["authReference"] = auth_reference
        if token_type is not UNSET:
            field_dict["tokenType"] = token_type
        if contract_id is not UNSET:
            field_dict["contractId"] = contract_id
        if auth_method is not UNSET:
            field_dict["authMethod"] = auth_method
        if provider_country_code is not UNSET:
            field_dict["providerCountryCode"] = provider_country_code
        if provider_party_id is not UNSET:
            field_dict["providerPartyId"] = provider_party_id
        if token_ou_id is not UNSET:
            field_dict["tokenOUId"] = token_ou_id
        if token_ou_name is not UNSET:
            field_dict["tokenOUName"] = token_ou_name
        if token_ou is not UNSET:
            field_dict["tokenOU"] = token_ou

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        uid = d.pop("uid", UNSET)

        auth_reference = d.pop("authReference", UNSET)

        _token_type = d.pop("tokenType", UNSET)
        token_type: Union[Unset, StartedByTokenDtoTokenType]
        if isinstance(_token_type, Unset) or _token_type is None:
            token_type = UNSET
        else:
            token_type = StartedByTokenDtoTokenType(_token_type)

        contract_id = d.pop("contractId", UNSET)

        _auth_method = d.pop("authMethod", UNSET)
        auth_method: Union[Unset, StartedByTokenDtoAuthMethod]
        if isinstance(_auth_method, Unset) or _auth_method is None:
            auth_method = UNSET
        else:
            auth_method = StartedByTokenDtoAuthMethod(_auth_method)

        provider_country_code = d.pop("providerCountryCode", UNSET)

        provider_party_id = d.pop("providerPartyId", UNSET)

        token_ou_id = d.pop("tokenOUId", UNSET)

        token_ou_name = d.pop("tokenOUName", UNSET)

        token_ou = d.pop("tokenOU", UNSET)

        started_by_token_dto = cls(
            uid=uid,
            auth_reference=auth_reference,
            token_type=token_type,
            contract_id=contract_id,
            auth_method=auth_method,
            provider_country_code=provider_country_code,
            provider_party_id=provider_party_id,
            token_ou_id=token_ou_id,
            token_ou_name=token_ou_name,
            token_ou=token_ou,
        )

        started_by_token_dto.additional_properties = d
        return started_by_token_dto

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
