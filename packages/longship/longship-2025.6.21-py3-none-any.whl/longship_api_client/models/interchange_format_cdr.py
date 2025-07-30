from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
import datetime
from typing import Union


T = TypeVar("T", bound="InterchangeFormatCdr")


@_attrs_define
class InterchangeFormatCdr:
    """
    Attributes:
        cdr_id (Union[Unset, str]):
        start_date_time (Union[Unset, datetime.datetime]):
        end_date_time (Union[Unset, datetime.datetime]):
        duration (Union[Unset, str]):
        volume (Union[Unset, float]):
        charge_point_address (Union[Unset, str]):
        charge_point_zip (Union[Unset, str]):
        charge_point_city (Union[Unset, str]):
        charge_point_country (Union[Unset, str]):
        charge_point_type (Union[Unset, str]):
        product_type (Union[Unset, str]):
        tariff_type (Union[Unset, str]):
        authentication_id (Union[Unset, str]):
        contract_id (Union[Unset, str]):
        meter_id (Union[Unset, str]):
        obis_code (Union[Unset, str]):
        charge_point_id (Union[Unset, str]):
        service_provider_id (Union[Unset, str]):
        infra_provider_id (Union[Unset, str]):
        calculated_cost (Union[Unset, float]):
    """

    cdr_id: Union[Unset, str] = UNSET
    start_date_time: Union[Unset, datetime.datetime] = UNSET
    end_date_time: Union[Unset, datetime.datetime] = UNSET
    duration: Union[Unset, str] = UNSET
    volume: Union[Unset, float] = UNSET
    charge_point_address: Union[Unset, str] = UNSET
    charge_point_zip: Union[Unset, str] = UNSET
    charge_point_city: Union[Unset, str] = UNSET
    charge_point_country: Union[Unset, str] = UNSET
    charge_point_type: Union[Unset, str] = UNSET
    product_type: Union[Unset, str] = UNSET
    tariff_type: Union[Unset, str] = UNSET
    authentication_id: Union[Unset, str] = UNSET
    contract_id: Union[Unset, str] = UNSET
    meter_id: Union[Unset, str] = UNSET
    obis_code: Union[Unset, str] = UNSET
    charge_point_id: Union[Unset, str] = UNSET
    service_provider_id: Union[Unset, str] = UNSET
    infra_provider_id: Union[Unset, str] = UNSET
    calculated_cost: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        cdr_id = self.cdr_id

        start_date_time: Union[Unset, str] = UNSET
        if not isinstance(self.start_date_time, Unset):
            start_date_time = self.start_date_time.isoformat()

        end_date_time: Union[Unset, str] = UNSET
        if not isinstance(self.end_date_time, Unset):
            end_date_time = self.end_date_time.isoformat()

        duration = self.duration

        volume = self.volume

        charge_point_address = self.charge_point_address

        charge_point_zip = self.charge_point_zip

        charge_point_city = self.charge_point_city

        charge_point_country = self.charge_point_country

        charge_point_type = self.charge_point_type

        product_type = self.product_type

        tariff_type = self.tariff_type

        authentication_id = self.authentication_id

        contract_id = self.contract_id

        meter_id = self.meter_id

        obis_code = self.obis_code

        charge_point_id = self.charge_point_id

        service_provider_id = self.service_provider_id

        infra_provider_id = self.infra_provider_id

        calculated_cost = self.calculated_cost

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cdr_id is not UNSET:
            field_dict["cdrId"] = cdr_id
        if start_date_time is not UNSET:
            field_dict["startDateTime"] = start_date_time
        if end_date_time is not UNSET:
            field_dict["endDateTime"] = end_date_time
        if duration is not UNSET:
            field_dict["duration"] = duration
        if volume is not UNSET:
            field_dict["volume"] = volume
        if charge_point_address is not UNSET:
            field_dict["chargePointAddress"] = charge_point_address
        if charge_point_zip is not UNSET:
            field_dict["chargePointZip"] = charge_point_zip
        if charge_point_city is not UNSET:
            field_dict["chargePointCity"] = charge_point_city
        if charge_point_country is not UNSET:
            field_dict["chargePointCountry"] = charge_point_country
        if charge_point_type is not UNSET:
            field_dict["chargePointType"] = charge_point_type
        if product_type is not UNSET:
            field_dict["productType"] = product_type
        if tariff_type is not UNSET:
            field_dict["tariffType"] = tariff_type
        if authentication_id is not UNSET:
            field_dict["authenticationId"] = authentication_id
        if contract_id is not UNSET:
            field_dict["contractId"] = contract_id
        if meter_id is not UNSET:
            field_dict["meterId"] = meter_id
        if obis_code is not UNSET:
            field_dict["obisCode"] = obis_code
        if charge_point_id is not UNSET:
            field_dict["chargePointId"] = charge_point_id
        if service_provider_id is not UNSET:
            field_dict["serviceProviderId"] = service_provider_id
        if infra_provider_id is not UNSET:
            field_dict["infraProviderId"] = infra_provider_id
        if calculated_cost is not UNSET:
            field_dict["calculatedCost"] = calculated_cost

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        cdr_id = d.pop("cdrId", UNSET)

        _start_date_time = d.pop("startDateTime", UNSET)
        start_date_time: Union[Unset, datetime.datetime]
        if isinstance(_start_date_time, Unset) or _start_date_time is None:
            start_date_time = UNSET
        else:
            start_date_time = isoparse(_start_date_time)

        _end_date_time = d.pop("endDateTime", UNSET)
        end_date_time: Union[Unset, datetime.datetime]
        if isinstance(_end_date_time, Unset) or _end_date_time is None:
            end_date_time = UNSET
        else:
            end_date_time = isoparse(_end_date_time)

        duration = d.pop("duration", UNSET)

        volume = d.pop("volume", UNSET)

        charge_point_address = d.pop("chargePointAddress", UNSET)

        charge_point_zip = d.pop("chargePointZip", UNSET)

        charge_point_city = d.pop("chargePointCity", UNSET)

        charge_point_country = d.pop("chargePointCountry", UNSET)

        charge_point_type = d.pop("chargePointType", UNSET)

        product_type = d.pop("productType", UNSET)

        tariff_type = d.pop("tariffType", UNSET)

        authentication_id = d.pop("authenticationId", UNSET)

        contract_id = d.pop("contractId", UNSET)

        meter_id = d.pop("meterId", UNSET)

        obis_code = d.pop("obisCode", UNSET)

        charge_point_id = d.pop("chargePointId", UNSET)

        service_provider_id = d.pop("serviceProviderId", UNSET)

        infra_provider_id = d.pop("infraProviderId", UNSET)

        calculated_cost = d.pop("calculatedCost", UNSET)

        interchange_format_cdr = cls(
            cdr_id=cdr_id,
            start_date_time=start_date_time,
            end_date_time=end_date_time,
            duration=duration,
            volume=volume,
            charge_point_address=charge_point_address,
            charge_point_zip=charge_point_zip,
            charge_point_city=charge_point_city,
            charge_point_country=charge_point_country,
            charge_point_type=charge_point_type,
            product_type=product_type,
            tariff_type=tariff_type,
            authentication_id=authentication_id,
            contract_id=contract_id,
            meter_id=meter_id,
            obis_code=obis_code,
            charge_point_id=charge_point_id,
            service_provider_id=service_provider_id,
            infra_provider_id=infra_provider_id,
            calculated_cost=calculated_cost,
        )

        interchange_format_cdr.additional_properties = d
        return interchange_format_cdr

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
