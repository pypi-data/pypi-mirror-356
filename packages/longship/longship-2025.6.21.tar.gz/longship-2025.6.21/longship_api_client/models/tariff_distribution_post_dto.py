from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="TariffDistributionPostDto")


@_attrs_define
class TariffDistributionPostDto:
    """
    Attributes:
        name (Union[Unset, str]):
        ou_code (Union[Unset, str]):
        energy_compensation (Union[Unset, float]):
        fixed_tenant_k_wh_fee (Union[Unset, float]):
        percentage_fee_customer (Union[Unset, float]):
        percentage_fee_tenant (Union[Unset, float]):
    """

    name: Union[Unset, str] = UNSET
    ou_code: Union[Unset, str] = UNSET
    energy_compensation: Union[Unset, float] = UNSET
    fixed_tenant_k_wh_fee: Union[Unset, float] = UNSET
    percentage_fee_customer: Union[Unset, float] = UNSET
    percentage_fee_tenant: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        ou_code = self.ou_code

        energy_compensation = self.energy_compensation

        fixed_tenant_k_wh_fee = self.fixed_tenant_k_wh_fee

        percentage_fee_customer = self.percentage_fee_customer

        percentage_fee_tenant = self.percentage_fee_tenant

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if ou_code is not UNSET:
            field_dict["ouCode"] = ou_code
        if energy_compensation is not UNSET:
            field_dict["energyCompensation"] = energy_compensation
        if fixed_tenant_k_wh_fee is not UNSET:
            field_dict["fixedTenantKWhFee"] = fixed_tenant_k_wh_fee
        if percentage_fee_customer is not UNSET:
            field_dict["percentageFeeCustomer"] = percentage_fee_customer
        if percentage_fee_tenant is not UNSET:
            field_dict["percentageFeeTenant"] = percentage_fee_tenant

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        ou_code = d.pop("ouCode", UNSET)

        energy_compensation = d.pop("energyCompensation", UNSET)

        fixed_tenant_k_wh_fee = d.pop("fixedTenantKWhFee", UNSET)

        percentage_fee_customer = d.pop("percentageFeeCustomer", UNSET)

        percentage_fee_tenant = d.pop("percentageFeeTenant", UNSET)

        tariff_distribution_post_dto = cls(
            name=name,
            ou_code=ou_code,
            energy_compensation=energy_compensation,
            fixed_tenant_k_wh_fee=fixed_tenant_k_wh_fee,
            percentage_fee_customer=percentage_fee_customer,
            percentage_fee_tenant=percentage_fee_tenant,
        )

        tariff_distribution_post_dto.additional_properties = d
        return tariff_distribution_post_dto

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
