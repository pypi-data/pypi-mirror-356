from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union
from ..models.private_emp_tariff_dto_power_type import PrivateEmpTariffDtoPowerType


T = TypeVar("T", bound="PrivateEmpTariffDto")


@_attrs_define
class PrivateEmpTariffDto:
    """
    Attributes:
        country_code (Union[Unset, str]):
        party_id (Union[Unset, str]):
        power_type (Union[Unset, PrivateEmpTariffDtoPowerType]):  Default: PrivateEmpTariffDtoPowerType.AC.
        use_public_tariff_when_kwh_is_cheaper (Union[Unset, bool]):
    """

    country_code: Union[Unset, str] = UNSET
    party_id: Union[Unset, str] = UNSET
    power_type: Union[Unset, PrivateEmpTariffDtoPowerType] = (
        PrivateEmpTariffDtoPowerType.AC
    )
    use_public_tariff_when_kwh_is_cheaper: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        country_code = self.country_code

        party_id = self.party_id

        power_type: Union[Unset, str] = UNSET
        if not isinstance(self.power_type, Unset):
            power_type = self.power_type.value

        use_public_tariff_when_kwh_is_cheaper = (
            self.use_public_tariff_when_kwh_is_cheaper
        )

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if country_code is not UNSET:
            field_dict["country_code"] = country_code
        if party_id is not UNSET:
            field_dict["party_id"] = party_id
        if power_type is not UNSET:
            field_dict["powerType"] = power_type
        if use_public_tariff_when_kwh_is_cheaper is not UNSET:
            field_dict["usePublicTariffWhenKwhIsCheaper"] = (
                use_public_tariff_when_kwh_is_cheaper
            )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        country_code = d.pop("country_code", UNSET)

        party_id = d.pop("party_id", UNSET)

        _power_type = d.pop("powerType", UNSET)
        power_type: Union[Unset, PrivateEmpTariffDtoPowerType]
        if isinstance(_power_type, Unset) or _power_type is None:
            power_type = UNSET
        else:
            power_type = PrivateEmpTariffDtoPowerType(_power_type)

        use_public_tariff_when_kwh_is_cheaper = d.pop(
            "usePublicTariffWhenKwhIsCheaper", UNSET
        )

        private_emp_tariff_dto = cls(
            country_code=country_code,
            party_id=party_id,
            power_type=power_type,
            use_public_tariff_when_kwh_is_cheaper=use_public_tariff_when_kwh_is_cheaper,
        )

        private_emp_tariff_dto.additional_properties = d
        return private_emp_tariff_dto

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
