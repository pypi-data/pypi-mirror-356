from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Union

if TYPE_CHECKING:
    from ..models.local_token_group_token_put_dto import LocalTokenGroupTokenPutDto


T = TypeVar("T", bound="LocalTokenGroupPutDto")


@_attrs_define
class LocalTokenGroupPutDto:
    """
    Attributes:
        oucode (Union[Unset, str]):
        token_group_name (Union[Unset, str]):
        target_ou_codes (Union[Unset, List[str]]):
        override_tariff_id (Union[Unset, str]):
        tokens (Union[Unset, List['LocalTokenGroupTokenPutDto']]):
        target_chargepoint_ids (Union[Unset, List[str]]):
    """

    oucode: Union[Unset, str] = UNSET
    token_group_name: Union[Unset, str] = UNSET
    target_ou_codes: Union[Unset, List[str]] = UNSET
    override_tariff_id: Union[Unset, str] = UNSET
    tokens: Union[Unset, List["LocalTokenGroupTokenPutDto"]] = UNSET
    target_chargepoint_ids: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        oucode = self.oucode

        token_group_name = self.token_group_name

        target_ou_codes: Union[Unset, List[str]] = UNSET
        if not isinstance(self.target_ou_codes, Unset):
            target_ou_codes = self.target_ou_codes

        override_tariff_id = self.override_tariff_id

        tokens: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.tokens, Unset):
            tokens = []
            for tokens_item_data in self.tokens:
                tokens_item = tokens_item_data.to_dict()
                tokens.append(tokens_item)

        target_chargepoint_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.target_chargepoint_ids, Unset):
            target_chargepoint_ids = self.target_chargepoint_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if oucode is not UNSET:
            field_dict["oucode"] = oucode
        if token_group_name is not UNSET:
            field_dict["tokenGroupName"] = token_group_name
        if target_ou_codes is not UNSET:
            field_dict["targetOUCodes"] = target_ou_codes
        if override_tariff_id is not UNSET:
            field_dict["overrideTariffId"] = override_tariff_id
        if tokens is not UNSET:
            field_dict["tokens"] = tokens
        if target_chargepoint_ids is not UNSET:
            field_dict["targetChargepointIds"] = target_chargepoint_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.local_token_group_token_put_dto import LocalTokenGroupTokenPutDto

        d = src_dict.copy()
        oucode = d.pop("oucode", UNSET)

        token_group_name = d.pop("tokenGroupName", UNSET)

        target_ou_codes = cast(List[str], d.pop("targetOUCodes", UNSET))

        override_tariff_id = d.pop("overrideTariffId", UNSET)

        tokens = []
        _tokens = d.pop("tokens", UNSET)
        for tokens_item_data in _tokens or []:
            tokens_item = LocalTokenGroupTokenPutDto.from_dict(tokens_item_data)

            tokens.append(tokens_item)

        target_chargepoint_ids = cast(List[str], d.pop("targetChargepointIds", UNSET))

        local_token_group_put_dto = cls(
            oucode=oucode,
            token_group_name=token_group_name,
            target_ou_codes=target_ou_codes,
            override_tariff_id=override_tariff_id,
            tokens=tokens,
            target_chargepoint_ids=target_chargepoint_ids,
        )

        local_token_group_put_dto.additional_properties = d
        return local_token_group_put_dto

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
