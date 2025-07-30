from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
import datetime
from typing import Union

if TYPE_CHECKING:
    from ..models.tariff_distribution_history_dto import TariffDistributionHistoryDto


T = TypeVar("T", bound="TariffDistributionGetDto")


@_attrs_define
class TariffDistributionGetDto:
    """
    Attributes:
        id (str):
        name (Union[Unset, str]):
        ou_code (Union[Unset, str]):
        energy_compensation (Union[Unset, float]):
        fixed_tenant_k_wh_fee (Union[Unset, float]):
        percentage_fee_customer (Union[Unset, float]):
        percentage_fee_tenant (Union[Unset, float]):
        price_history (Union[Unset, List['TariffDistributionHistoryDto']]):
        created (Union[Unset, datetime.datetime]):
        deleted (Union[Unset, datetime.datetime]):
        updated (Union[Unset, datetime.datetime]):
    """

    id: str
    name: Union[Unset, str] = UNSET
    ou_code: Union[Unset, str] = UNSET
    energy_compensation: Union[Unset, float] = UNSET
    fixed_tenant_k_wh_fee: Union[Unset, float] = UNSET
    percentage_fee_customer: Union[Unset, float] = UNSET
    percentage_fee_tenant: Union[Unset, float] = UNSET
    price_history: Union[Unset, List["TariffDistributionHistoryDto"]] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    deleted: Union[Unset, datetime.datetime] = UNSET
    updated: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        name = self.name

        ou_code = self.ou_code

        energy_compensation = self.energy_compensation

        fixed_tenant_k_wh_fee = self.fixed_tenant_k_wh_fee

        percentage_fee_customer = self.percentage_fee_customer

        percentage_fee_tenant = self.percentage_fee_tenant

        price_history: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.price_history, Unset):
            price_history = []
            for price_history_item_data in self.price_history:
                price_history_item = price_history_item_data.to_dict()
                price_history.append(price_history_item)

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        deleted: Union[Unset, str] = UNSET
        if not isinstance(self.deleted, Unset):
            deleted = self.deleted.isoformat()

        updated: Union[Unset, str] = UNSET
        if not isinstance(self.updated, Unset):
            updated = self.updated.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
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
        if price_history is not UNSET:
            field_dict["priceHistory"] = price_history
        if created is not UNSET:
            field_dict["created"] = created
        if deleted is not UNSET:
            field_dict["deleted"] = deleted
        if updated is not UNSET:
            field_dict["updated"] = updated

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.tariff_distribution_history_dto import (
            TariffDistributionHistoryDto,
        )

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name", UNSET)

        ou_code = d.pop("ouCode", UNSET)

        energy_compensation = d.pop("energyCompensation", UNSET)

        fixed_tenant_k_wh_fee = d.pop("fixedTenantKWhFee", UNSET)

        percentage_fee_customer = d.pop("percentageFeeCustomer", UNSET)

        percentage_fee_tenant = d.pop("percentageFeeTenant", UNSET)

        price_history = []
        _price_history = d.pop("priceHistory", UNSET)
        for price_history_item_data in _price_history or []:
            price_history_item = TariffDistributionHistoryDto.from_dict(
                price_history_item_data
            )

            price_history.append(price_history_item)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset) or _created is None:
            created = UNSET
        else:
            created = isoparse(_created)

        _deleted = d.pop("deleted", UNSET)
        deleted: Union[Unset, datetime.datetime]
        if isinstance(_deleted, Unset) or _deleted is None:
            deleted = UNSET
        else:
            deleted = isoparse(_deleted)

        _updated = d.pop("updated", UNSET)
        updated: Union[Unset, datetime.datetime]
        if isinstance(_updated, Unset) or _updated is None:
            updated = UNSET
        else:
            updated = isoparse(_updated)

        tariff_distribution_get_dto = cls(
            id=id,
            name=name,
            ou_code=ou_code,
            energy_compensation=energy_compensation,
            fixed_tenant_k_wh_fee=fixed_tenant_k_wh_fee,
            percentage_fee_customer=percentage_fee_customer,
            percentage_fee_tenant=percentage_fee_tenant,
            price_history=price_history,
            created=created,
            deleted=deleted,
            updated=updated,
        )

        tariff_distribution_get_dto.additional_properties = d
        return tariff_distribution_get_dto

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
