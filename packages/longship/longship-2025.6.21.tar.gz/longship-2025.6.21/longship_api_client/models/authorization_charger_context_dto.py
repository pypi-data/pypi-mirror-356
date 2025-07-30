from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="AuthorizationChargerContextDto")


@_attrs_define
class AuthorizationChargerContextDto:
    """
    Attributes:
        allow_any_token (Union[Unset, bool]):
        is_roaming (Union[Unset, bool]):
        charge_point_ou_code (Union[Unset, str]):
        reimburse_uid (Union[Unset, str]):
        reimburse_ou (Union[Unset, str]):
        has_reimbursement (Union[Unset, bool]):
    """

    allow_any_token: Union[Unset, bool] = UNSET
    is_roaming: Union[Unset, bool] = UNSET
    charge_point_ou_code: Union[Unset, str] = UNSET
    reimburse_uid: Union[Unset, str] = UNSET
    reimburse_ou: Union[Unset, str] = UNSET
    has_reimbursement: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        allow_any_token = self.allow_any_token

        is_roaming = self.is_roaming

        charge_point_ou_code = self.charge_point_ou_code

        reimburse_uid = self.reimburse_uid

        reimburse_ou = self.reimburse_ou

        has_reimbursement = self.has_reimbursement

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if allow_any_token is not UNSET:
            field_dict["allowAnyToken"] = allow_any_token
        if is_roaming is not UNSET:
            field_dict["isRoaming"] = is_roaming
        if charge_point_ou_code is not UNSET:
            field_dict["chargePointOUCode"] = charge_point_ou_code
        if reimburse_uid is not UNSET:
            field_dict["reimburseUid"] = reimburse_uid
        if reimburse_ou is not UNSET:
            field_dict["reimburseOu"] = reimburse_ou
        if has_reimbursement is not UNSET:
            field_dict["hasReimbursement"] = has_reimbursement

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        allow_any_token = d.pop("allowAnyToken", UNSET)

        is_roaming = d.pop("isRoaming", UNSET)

        charge_point_ou_code = d.pop("chargePointOUCode", UNSET)

        reimburse_uid = d.pop("reimburseUid", UNSET)

        reimburse_ou = d.pop("reimburseOu", UNSET)

        has_reimbursement = d.pop("hasReimbursement", UNSET)

        authorization_charger_context_dto = cls(
            allow_any_token=allow_any_token,
            is_roaming=is_roaming,
            charge_point_ou_code=charge_point_ou_code,
            reimburse_uid=reimburse_uid,
            reimburse_ou=reimburse_ou,
            has_reimbursement=has_reimbursement,
        )

        authorization_charger_context_dto.additional_properties = d
        return authorization_charger_context_dto

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
