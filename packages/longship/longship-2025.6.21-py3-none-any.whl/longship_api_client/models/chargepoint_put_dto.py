from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="ChargepointPutDto")


@_attrs_define
class ChargepointPutDto:
    """
    Attributes:
        display_name (Union[Unset, str]):
        roaming_name (Union[Unset, str]):
        allow_any_token (Union[Unset, bool]):
        ou_code (Union[Unset, str]):
        tariff_id (Union[Unset, str]):
        sim_card_number (Union[Unset, str]):
        is_new (Union[Unset, bool]):
        max_capacity_in_kw (Union[Unset, float]):
    """

    display_name: Union[Unset, str] = UNSET
    roaming_name: Union[Unset, str] = UNSET
    allow_any_token: Union[Unset, bool] = UNSET
    ou_code: Union[Unset, str] = UNSET
    tariff_id: Union[Unset, str] = UNSET
    sim_card_number: Union[Unset, str] = UNSET
    is_new: Union[Unset, bool] = UNSET
    max_capacity_in_kw: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        display_name = self.display_name

        roaming_name = self.roaming_name

        allow_any_token = self.allow_any_token

        ou_code = self.ou_code

        tariff_id = self.tariff_id

        sim_card_number = self.sim_card_number

        is_new = self.is_new

        max_capacity_in_kw = self.max_capacity_in_kw

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if roaming_name is not UNSET:
            field_dict["roamingName"] = roaming_name
        if allow_any_token is not UNSET:
            field_dict["allowAnyToken"] = allow_any_token
        if ou_code is not UNSET:
            field_dict["ouCode"] = ou_code
        if tariff_id is not UNSET:
            field_dict["tariffId"] = tariff_id
        if sim_card_number is not UNSET:
            field_dict["simCardNumber"] = sim_card_number
        if is_new is not UNSET:
            field_dict["isNew"] = is_new
        if max_capacity_in_kw is not UNSET:
            field_dict["maxCapacityInKw"] = max_capacity_in_kw

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        display_name = d.pop("displayName", UNSET)

        roaming_name = d.pop("roamingName", UNSET)

        allow_any_token = d.pop("allowAnyToken", UNSET)

        ou_code = d.pop("ouCode", UNSET)

        tariff_id = d.pop("tariffId", UNSET)

        sim_card_number = d.pop("simCardNumber", UNSET)

        is_new = d.pop("isNew", UNSET)

        max_capacity_in_kw = d.pop("maxCapacityInKw", UNSET)

        chargepoint_put_dto = cls(
            display_name=display_name,
            roaming_name=roaming_name,
            allow_any_token=allow_any_token,
            ou_code=ou_code,
            tariff_id=tariff_id,
            sim_card_number=sim_card_number,
            is_new=is_new,
            max_capacity_in_kw=max_capacity_in_kw,
        )

        chargepoint_put_dto.additional_properties = d
        return chargepoint_put_dto

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
