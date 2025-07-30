from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="ChargePointAuthorizePostDto")


@_attrs_define
class ChargePointAuthorizePostDto:
    """
    Attributes:
        contract_id (Union[Unset, str]):
        id_tag (Union[Unset, str]):
    """

    contract_id: Union[Unset, str] = UNSET
    id_tag: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        contract_id = self.contract_id

        id_tag = self.id_tag

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if contract_id is not UNSET:
            field_dict["contractId"] = contract_id
        if id_tag is not UNSET:
            field_dict["idTag"] = id_tag

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        contract_id = d.pop("contractId", UNSET)

        id_tag = d.pop("idTag", UNSET)

        charge_point_authorize_post_dto = cls(
            contract_id=contract_id,
            id_tag=id_tag,
        )

        charge_point_authorize_post_dto.additional_properties = d
        return charge_point_authorize_post_dto

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
