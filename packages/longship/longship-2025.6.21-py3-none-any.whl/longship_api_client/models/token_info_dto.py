from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union
from ..models.token_info_dto_token_type import TokenInfoDtoTokenType


T = TypeVar("T", bound="TokenInfoDto")


@_attrs_define
class TokenInfoDto:
    """
    Attributes:
        id_tag (Union[Unset, str]):
        contract_id (Union[Unset, str]):
        token_type (Union[Unset, TokenInfoDtoTokenType]):  Default: TokenInfoDtoTokenType.ADHOCUSER.
    """

    id_tag: Union[Unset, str] = UNSET
    contract_id: Union[Unset, str] = UNSET
    token_type: Union[Unset, TokenInfoDtoTokenType] = TokenInfoDtoTokenType.ADHOCUSER
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_tag = self.id_tag

        contract_id = self.contract_id

        token_type: Union[Unset, str] = UNSET
        if not isinstance(self.token_type, Unset):
            token_type = self.token_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id_tag is not UNSET:
            field_dict["idTag"] = id_tag
        if contract_id is not UNSET:
            field_dict["contractId"] = contract_id
        if token_type is not UNSET:
            field_dict["tokenType"] = token_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_tag = d.pop("idTag", UNSET)

        contract_id = d.pop("contractId", UNSET)

        _token_type = d.pop("tokenType", UNSET)
        token_type: Union[Unset, TokenInfoDtoTokenType]
        if isinstance(_token_type, Unset) or _token_type is None:
            token_type = UNSET
        else:
            token_type = TokenInfoDtoTokenType(_token_type)

        token_info_dto = cls(
            id_tag=id_tag,
            contract_id=contract_id,
            token_type=token_type,
        )

        token_info_dto.additional_properties = d
        return token_info_dto

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
