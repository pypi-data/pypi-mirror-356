from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="ReimbursementCustomerShareDto")


@_attrs_define
class ReimbursementCustomerShareDto:
    """
    Attributes:
        customer_share (Union[Unset, float]):
        energy_compensation (Union[Unset, float]):
        tenant_fee (Union[Unset, float]):
    """

    customer_share: Union[Unset, float] = UNSET
    energy_compensation: Union[Unset, float] = UNSET
    tenant_fee: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        customer_share = self.customer_share

        energy_compensation = self.energy_compensation

        tenant_fee = self.tenant_fee

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if customer_share is not UNSET:
            field_dict["customerShare"] = customer_share
        if energy_compensation is not UNSET:
            field_dict["energyCompensation"] = energy_compensation
        if tenant_fee is not UNSET:
            field_dict["tenantFee"] = tenant_fee

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        customer_share = d.pop("customerShare", UNSET)

        energy_compensation = d.pop("energyCompensation", UNSET)

        tenant_fee = d.pop("tenantFee", UNSET)

        reimbursement_customer_share_dto = cls(
            customer_share=customer_share,
            energy_compensation=energy_compensation,
            tenant_fee=tenant_fee,
        )

        reimbursement_customer_share_dto.additional_properties = d
        return reimbursement_customer_share_dto

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
