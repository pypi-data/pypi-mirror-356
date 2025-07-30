from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.tariff_dto_tariff_type import TariffDtoTariffType
from dateutil.parser import isoparse
import datetime
from typing import Union
from ..models.tariff_dto_usage_type import TariffDtoUsageType

if TYPE_CHECKING:
    from ..models.tariff_price_dto import TariffPriceDto
    from ..models.private_emp_tariff_dto import PrivateEmpTariffDto
    from ..models.tariff_restriction import TariffRestriction


T = TypeVar("T", bound="TariffDto")


@_attrs_define
class TariffDto:
    """
    Attributes:
        tenant_id (str):
        id (Union[Unset, str]):
        ocpi_id (Union[Unset, str]):
        hubject_id (Union[Unset, str]):
        name (Union[Unset, str]):
        start_tariff (Union[Unset, float]):
        price (Union[Unset, float]):
        price_incl_vat (Union[Unset, float]):
        currency (Union[Unset, str]):
        last_updated (Union[Unset, datetime.datetime]):
        usage_type (Union[Unset, TariffDtoUsageType]):  Default: TariffDtoUsageType.SELL.
        tariff_type (Union[Unset, TariffDtoTariffType]):  Default: TariffDtoTariffType.AD_HOC_PAYMENT.
        vat (Union[Unset, float]):
        is_vat_relevant (Union[Unset, bool]):
        country_code (Union[Unset, str]):
        party_id (Union[Unset, str]):
        location_id (Union[Unset, str]):
        is_private_emp_tariff (Union[Unset, bool]):
        private_emp_tariff (Union[Unset, PrivateEmpTariffDto]):
        parking_tariff (Union[Unset, float]):
        parking_step_size_in_minutes (Union[Unset, int]):
        parking_grace_period_in_minutes (Union[Unset, int]):
        parking_tariff_restrictions (Union[Unset, List['TariffRestriction']]):
        time_tariff (Union[Unset, float]):
        time_step_size_in_minutes (Union[Unset, int]):
        time_grace_period_in_minutes (Union[Unset, int]):
        price_history (Union[Unset, List['TariffPriceDto']]):
        external_reference (Union[Unset, str]):
        deleted (Union[Unset, datetime.datetime]):
    """

    tenant_id: str
    id: Union[Unset, str] = UNSET
    ocpi_id: Union[Unset, str] = UNSET
    hubject_id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    start_tariff: Union[Unset, float] = UNSET
    price: Union[Unset, float] = UNSET
    price_incl_vat: Union[Unset, float] = UNSET
    currency: Union[Unset, str] = UNSET
    last_updated: Union[Unset, datetime.datetime] = UNSET
    usage_type: Union[Unset, TariffDtoUsageType] = TariffDtoUsageType.SELL
    tariff_type: Union[Unset, TariffDtoTariffType] = TariffDtoTariffType.AD_HOC_PAYMENT
    vat: Union[Unset, float] = UNSET
    is_vat_relevant: Union[Unset, bool] = UNSET
    country_code: Union[Unset, str] = UNSET
    party_id: Union[Unset, str] = UNSET
    location_id: Union[Unset, str] = UNSET
    is_private_emp_tariff: Union[Unset, bool] = UNSET
    private_emp_tariff: Union[Unset, "PrivateEmpTariffDto"] = UNSET
    parking_tariff: Union[Unset, float] = UNSET
    parking_step_size_in_minutes: Union[Unset, int] = UNSET
    parking_grace_period_in_minutes: Union[Unset, int] = UNSET
    parking_tariff_restrictions: Union[Unset, List["TariffRestriction"]] = UNSET
    time_tariff: Union[Unset, float] = UNSET
    time_step_size_in_minutes: Union[Unset, int] = UNSET
    time_grace_period_in_minutes: Union[Unset, int] = UNSET
    price_history: Union[Unset, List["TariffPriceDto"]] = UNSET
    external_reference: Union[Unset, str] = UNSET
    deleted: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        tenant_id = self.tenant_id

        id = self.id

        ocpi_id = self.ocpi_id

        hubject_id = self.hubject_id

        name = self.name

        start_tariff = self.start_tariff

        price = self.price

        price_incl_vat = self.price_incl_vat

        currency = self.currency

        last_updated: Union[Unset, str] = UNSET
        if not isinstance(self.last_updated, Unset):
            last_updated = self.last_updated.isoformat()

        usage_type: Union[Unset, str] = UNSET
        if not isinstance(self.usage_type, Unset):
            usage_type = self.usage_type.value

        tariff_type: Union[Unset, str] = UNSET
        if not isinstance(self.tariff_type, Unset):
            tariff_type = self.tariff_type.value

        vat = self.vat

        is_vat_relevant = self.is_vat_relevant

        country_code = self.country_code

        party_id = self.party_id

        location_id = self.location_id

        is_private_emp_tariff = self.is_private_emp_tariff

        private_emp_tariff: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.private_emp_tariff, Unset):
            private_emp_tariff = self.private_emp_tariff.to_dict()

        parking_tariff = self.parking_tariff

        parking_step_size_in_minutes = self.parking_step_size_in_minutes

        parking_grace_period_in_minutes = self.parking_grace_period_in_minutes

        parking_tariff_restrictions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.parking_tariff_restrictions, Unset):
            parking_tariff_restrictions = []
            for (
                parking_tariff_restrictions_item_data
            ) in self.parking_tariff_restrictions:
                parking_tariff_restrictions_item = (
                    parking_tariff_restrictions_item_data.to_dict()
                )
                parking_tariff_restrictions.append(parking_tariff_restrictions_item)

        time_tariff = self.time_tariff

        time_step_size_in_minutes = self.time_step_size_in_minutes

        time_grace_period_in_minutes = self.time_grace_period_in_minutes

        price_history: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.price_history, Unset):
            price_history = []
            for price_history_item_data in self.price_history:
                price_history_item = price_history_item_data.to_dict()
                price_history.append(price_history_item)

        external_reference = self.external_reference

        deleted: Union[Unset, str] = UNSET
        if not isinstance(self.deleted, Unset):
            deleted = self.deleted.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tenantId": tenant_id,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if ocpi_id is not UNSET:
            field_dict["ocpiId"] = ocpi_id
        if hubject_id is not UNSET:
            field_dict["hubjectId"] = hubject_id
        if name is not UNSET:
            field_dict["name"] = name
        if start_tariff is not UNSET:
            field_dict["startTariff"] = start_tariff
        if price is not UNSET:
            field_dict["price"] = price
        if price_incl_vat is not UNSET:
            field_dict["priceInclVat"] = price_incl_vat
        if currency is not UNSET:
            field_dict["currency"] = currency
        if last_updated is not UNSET:
            field_dict["last_updated"] = last_updated
        if usage_type is not UNSET:
            field_dict["usageType"] = usage_type
        if tariff_type is not UNSET:
            field_dict["tariffType"] = tariff_type
        if vat is not UNSET:
            field_dict["vat"] = vat
        if is_vat_relevant is not UNSET:
            field_dict["isVatRelevant"] = is_vat_relevant
        if country_code is not UNSET:
            field_dict["country_code"] = country_code
        if party_id is not UNSET:
            field_dict["party_id"] = party_id
        if location_id is not UNSET:
            field_dict["locationId"] = location_id
        if is_private_emp_tariff is not UNSET:
            field_dict["isPrivateEmpTariff"] = is_private_emp_tariff
        if private_emp_tariff is not UNSET:
            field_dict["privateEmpTariff"] = private_emp_tariff
        if parking_tariff is not UNSET:
            field_dict["parkingTariff"] = parking_tariff
        if parking_step_size_in_minutes is not UNSET:
            field_dict["parkingStepSizeInMinutes"] = parking_step_size_in_minutes
        if parking_grace_period_in_minutes is not UNSET:
            field_dict["parkingGracePeriodInMinutes"] = parking_grace_period_in_minutes
        if parking_tariff_restrictions is not UNSET:
            field_dict["parkingTariffRestrictions"] = parking_tariff_restrictions
        if time_tariff is not UNSET:
            field_dict["timeTariff"] = time_tariff
        if time_step_size_in_minutes is not UNSET:
            field_dict["timeStepSizeInMinutes"] = time_step_size_in_minutes
        if time_grace_period_in_minutes is not UNSET:
            field_dict["timeGracePeriodInMinutes"] = time_grace_period_in_minutes
        if price_history is not UNSET:
            field_dict["priceHistory"] = price_history
        if external_reference is not UNSET:
            field_dict["externalReference"] = external_reference
        if deleted is not UNSET:
            field_dict["deleted"] = deleted

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.tariff_price_dto import TariffPriceDto
        from ..models.private_emp_tariff_dto import PrivateEmpTariffDto
        from ..models.tariff_restriction import TariffRestriction

        d = src_dict.copy()
        tenant_id = d.pop("tenantId")

        id = d.pop("id", UNSET)

        ocpi_id = d.pop("ocpiId", UNSET)

        hubject_id = d.pop("hubjectId", UNSET)

        name = d.pop("name", UNSET)

        start_tariff = d.pop("startTariff", UNSET)

        price = d.pop("price", UNSET)

        price_incl_vat = d.pop("priceInclVat", UNSET)

        currency = d.pop("currency", UNSET)

        _last_updated = d.pop("last_updated", UNSET)
        last_updated: Union[Unset, datetime.datetime]
        if isinstance(_last_updated, Unset) or _last_updated is None:
            last_updated = UNSET
        else:
            last_updated = isoparse(_last_updated)

        _usage_type = d.pop("usageType", UNSET)
        usage_type: Union[Unset, TariffDtoUsageType]
        if isinstance(_usage_type, Unset) or _usage_type is None:
            usage_type = UNSET
        else:
            usage_type = TariffDtoUsageType(_usage_type)

        _tariff_type = d.pop("tariffType", UNSET)
        tariff_type: Union[Unset, TariffDtoTariffType]
        if isinstance(_tariff_type, Unset) or _tariff_type is None:
            tariff_type = UNSET
        else:
            tariff_type = TariffDtoTariffType(_tariff_type)

        vat = d.pop("vat", UNSET)

        is_vat_relevant = d.pop("isVatRelevant", UNSET)

        country_code = d.pop("country_code", UNSET)

        party_id = d.pop("party_id", UNSET)

        location_id = d.pop("locationId", UNSET)

        is_private_emp_tariff = d.pop("isPrivateEmpTariff", UNSET)

        _private_emp_tariff = d.pop("privateEmpTariff", UNSET)
        private_emp_tariff: Union[Unset, PrivateEmpTariffDto]
        if isinstance(_private_emp_tariff, Unset) or _private_emp_tariff is None:
            private_emp_tariff = UNSET
        else:
            private_emp_tariff = PrivateEmpTariffDto.from_dict(_private_emp_tariff)

        parking_tariff = d.pop("parkingTariff", UNSET)

        parking_step_size_in_minutes = d.pop("parkingStepSizeInMinutes", UNSET)

        parking_grace_period_in_minutes = d.pop("parkingGracePeriodInMinutes", UNSET)

        parking_tariff_restrictions = []
        _parking_tariff_restrictions = d.pop("parkingTariffRestrictions", UNSET)
        for parking_tariff_restrictions_item_data in _parking_tariff_restrictions or []:
            parking_tariff_restrictions_item = TariffRestriction.from_dict(
                parking_tariff_restrictions_item_data
            )

            parking_tariff_restrictions.append(parking_tariff_restrictions_item)

        time_tariff = d.pop("timeTariff", UNSET)

        time_step_size_in_minutes = d.pop("timeStepSizeInMinutes", UNSET)

        time_grace_period_in_minutes = d.pop("timeGracePeriodInMinutes", UNSET)

        price_history = []
        _price_history = d.pop("priceHistory", UNSET)
        for price_history_item_data in _price_history or []:
            price_history_item = TariffPriceDto.from_dict(price_history_item_data)

            price_history.append(price_history_item)

        external_reference = d.pop("externalReference", UNSET)

        _deleted = d.pop("deleted", UNSET)
        deleted: Union[Unset, datetime.datetime]
        if isinstance(_deleted, Unset) or _deleted is None:
            deleted = UNSET
        else:
            deleted = isoparse(_deleted)

        tariff_dto = cls(
            tenant_id=tenant_id,
            id=id,
            ocpi_id=ocpi_id,
            hubject_id=hubject_id,
            name=name,
            start_tariff=start_tariff,
            price=price,
            price_incl_vat=price_incl_vat,
            currency=currency,
            last_updated=last_updated,
            usage_type=usage_type,
            tariff_type=tariff_type,
            vat=vat,
            is_vat_relevant=is_vat_relevant,
            country_code=country_code,
            party_id=party_id,
            location_id=location_id,
            is_private_emp_tariff=is_private_emp_tariff,
            private_emp_tariff=private_emp_tariff,
            parking_tariff=parking_tariff,
            parking_step_size_in_minutes=parking_step_size_in_minutes,
            parking_grace_period_in_minutes=parking_grace_period_in_minutes,
            parking_tariff_restrictions=parking_tariff_restrictions,
            time_tariff=time_tariff,
            time_step_size_in_minutes=time_step_size_in_minutes,
            time_grace_period_in_minutes=time_grace_period_in_minutes,
            price_history=price_history,
            external_reference=external_reference,
            deleted=deleted,
        )

        tariff_dto.additional_properties = d
        return tariff_dto

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
