from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.cdr_dto_approval_status import CdrDtoApprovalStatus
from dateutil.parser import isoparse
from ..models.cdr_dto_financial_type import CdrDtoFinancialType
import datetime
from typing import Union

if TYPE_CHECKING:
    from ..models.cdr_location_dto import CdrLocationDto
    from ..models.cdr_started_by_info_dto import CdrStartedByInfoDto
    from ..models.charging_period_dto import ChargingPeriodDto
    from ..models.price_info_dto import PriceInfoDto


T = TypeVar("T", bound="CdrDto")


@_attrs_define
class CdrDto:
    """
    Attributes:
        id (Union[Unset, str]):
        tenant_id (Union[Unset, str]):
        charge_point_id (Union[Unset, str]):
        connector_id (Union[Unset, int]):
        cdr_location (Union[Unset, CdrLocationDto]):
        start_datetime (Union[Unset, datetime.datetime]):
        end_date_time (Union[Unset, datetime.datetime]):
        session_id (Union[Unset, str]):
        token (Union[Unset, str]):
        started_by_info (Union[Unset, CdrStartedByInfoDto]):
        total_energy_in_kwh (Union[Unset, float]):
        total_time_in_hours (Union[Unset, float]):
        charging_periods (Union[Unset, List['ChargingPeriodDto']]):
        total_price (Union[Unset, float]):
        created (Union[Unset, datetime.datetime]):
        last_updated (Union[Unset, datetime.datetime]):
        ou (Union[Unset, str]):
        ou_id (Union[Unset, str]):
        ou_name (Union[Unset, str]):
        tariff_id (Union[Unset, str]):
        tariff_name (Union[Unset, str]):
        start_tariff (Union[Unset, float]):
        tariff_price (Union[Unset, float]):
        charging_time_tariff (Union[Unset, float]):
        parking_time_tariff (Union[Unset, float]):
        price_info (Union[Unset, PriceInfoDto]):
        local_start_date_time (Union[Unset, datetime.datetime]):
        local_end_date_time (Union[Unset, datetime.datetime]):
        approval_status (Union[Unset, CdrDtoApprovalStatus]):  Default: CdrDtoApprovalStatus.APPROVED.
        financial_type (Union[Unset, CdrDtoFinancialType]):  Default: CdrDtoFinancialType.DEBIT.
        debit_cdr_id (Union[Unset, str]):
    """

    id: Union[Unset, str] = UNSET
    tenant_id: Union[Unset, str] = UNSET
    charge_point_id: Union[Unset, str] = UNSET
    connector_id: Union[Unset, int] = UNSET
    cdr_location: Union[Unset, "CdrLocationDto"] = UNSET
    start_datetime: Union[Unset, datetime.datetime] = UNSET
    end_date_time: Union[Unset, datetime.datetime] = UNSET
    session_id: Union[Unset, str] = UNSET
    token: Union[Unset, str] = UNSET
    started_by_info: Union[Unset, "CdrStartedByInfoDto"] = UNSET
    total_energy_in_kwh: Union[Unset, float] = UNSET
    total_time_in_hours: Union[Unset, float] = UNSET
    charging_periods: Union[Unset, List["ChargingPeriodDto"]] = UNSET
    total_price: Union[Unset, float] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    last_updated: Union[Unset, datetime.datetime] = UNSET
    ou: Union[Unset, str] = UNSET
    ou_id: Union[Unset, str] = UNSET
    ou_name: Union[Unset, str] = UNSET
    tariff_id: Union[Unset, str] = UNSET
    tariff_name: Union[Unset, str] = UNSET
    start_tariff: Union[Unset, float] = UNSET
    tariff_price: Union[Unset, float] = UNSET
    charging_time_tariff: Union[Unset, float] = UNSET
    parking_time_tariff: Union[Unset, float] = UNSET
    price_info: Union[Unset, "PriceInfoDto"] = UNSET
    local_start_date_time: Union[Unset, datetime.datetime] = UNSET
    local_end_date_time: Union[Unset, datetime.datetime] = UNSET
    approval_status: Union[Unset, CdrDtoApprovalStatus] = CdrDtoApprovalStatus.APPROVED
    financial_type: Union[Unset, CdrDtoFinancialType] = CdrDtoFinancialType.DEBIT
    debit_cdr_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        tenant_id = self.tenant_id

        charge_point_id = self.charge_point_id

        connector_id = self.connector_id

        cdr_location: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.cdr_location, Unset):
            cdr_location = self.cdr_location.to_dict()

        start_datetime: Union[Unset, str] = UNSET
        if not isinstance(self.start_datetime, Unset):
            start_datetime = self.start_datetime.isoformat()

        end_date_time: Union[Unset, str] = UNSET
        if not isinstance(self.end_date_time, Unset):
            end_date_time = self.end_date_time.isoformat()

        session_id = self.session_id

        token = self.token

        started_by_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.started_by_info, Unset):
            started_by_info = self.started_by_info.to_dict()

        total_energy_in_kwh = self.total_energy_in_kwh

        total_time_in_hours = self.total_time_in_hours

        charging_periods: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.charging_periods, Unset):
            charging_periods = []
            for charging_periods_item_data in self.charging_periods:
                charging_periods_item = charging_periods_item_data.to_dict()
                charging_periods.append(charging_periods_item)

        total_price = self.total_price

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        last_updated: Union[Unset, str] = UNSET
        if not isinstance(self.last_updated, Unset):
            last_updated = self.last_updated.isoformat()

        ou = self.ou

        ou_id = self.ou_id

        ou_name = self.ou_name

        tariff_id = self.tariff_id

        tariff_name = self.tariff_name

        start_tariff = self.start_tariff

        tariff_price = self.tariff_price

        charging_time_tariff = self.charging_time_tariff

        parking_time_tariff = self.parking_time_tariff

        price_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.price_info, Unset):
            price_info = self.price_info.to_dict()

        local_start_date_time: Union[Unset, str] = UNSET
        if not isinstance(self.local_start_date_time, Unset):
            local_start_date_time = self.local_start_date_time.isoformat()

        local_end_date_time: Union[Unset, str] = UNSET
        if not isinstance(self.local_end_date_time, Unset):
            local_end_date_time = self.local_end_date_time.isoformat()

        approval_status: Union[Unset, str] = UNSET
        if not isinstance(self.approval_status, Unset):
            approval_status = self.approval_status.value

        financial_type: Union[Unset, str] = UNSET
        if not isinstance(self.financial_type, Unset):
            financial_type = self.financial_type.value

        debit_cdr_id = self.debit_cdr_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id
        if charge_point_id is not UNSET:
            field_dict["chargePointId"] = charge_point_id
        if connector_id is not UNSET:
            field_dict["connectorId"] = connector_id
        if cdr_location is not UNSET:
            field_dict["cdrLocation"] = cdr_location
        if start_datetime is not UNSET:
            field_dict["startDatetime"] = start_datetime
        if end_date_time is not UNSET:
            field_dict["endDateTime"] = end_date_time
        if session_id is not UNSET:
            field_dict["sessionId"] = session_id
        if token is not UNSET:
            field_dict["token"] = token
        if started_by_info is not UNSET:
            field_dict["startedByInfo"] = started_by_info
        if total_energy_in_kwh is not UNSET:
            field_dict["totalEnergyInKwh"] = total_energy_in_kwh
        if total_time_in_hours is not UNSET:
            field_dict["totalTimeInHours"] = total_time_in_hours
        if charging_periods is not UNSET:
            field_dict["chargingPeriods"] = charging_periods
        if total_price is not UNSET:
            field_dict["totalPrice"] = total_price
        if created is not UNSET:
            field_dict["created"] = created
        if last_updated is not UNSET:
            field_dict["lastUpdated"] = last_updated
        if ou is not UNSET:
            field_dict["ou"] = ou
        if ou_id is not UNSET:
            field_dict["ouId"] = ou_id
        if ou_name is not UNSET:
            field_dict["ouName"] = ou_name
        if tariff_id is not UNSET:
            field_dict["tariffId"] = tariff_id
        if tariff_name is not UNSET:
            field_dict["tariffName"] = tariff_name
        if start_tariff is not UNSET:
            field_dict["startTariff"] = start_tariff
        if tariff_price is not UNSET:
            field_dict["tariffPrice"] = tariff_price
        if charging_time_tariff is not UNSET:
            field_dict["chargingTimeTariff"] = charging_time_tariff
        if parking_time_tariff is not UNSET:
            field_dict["parkingTimeTariff"] = parking_time_tariff
        if price_info is not UNSET:
            field_dict["priceInfo"] = price_info
        if local_start_date_time is not UNSET:
            field_dict["localStartDateTime"] = local_start_date_time
        if local_end_date_time is not UNSET:
            field_dict["localEndDateTime"] = local_end_date_time
        if approval_status is not UNSET:
            field_dict["approvalStatus"] = approval_status
        if financial_type is not UNSET:
            field_dict["financialType"] = financial_type
        if debit_cdr_id is not UNSET:
            field_dict["debitCdrId"] = debit_cdr_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.cdr_location_dto import CdrLocationDto
        from ..models.cdr_started_by_info_dto import CdrStartedByInfoDto
        from ..models.charging_period_dto import ChargingPeriodDto
        from ..models.price_info_dto import PriceInfoDto

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        tenant_id = d.pop("tenantId", UNSET)

        charge_point_id = d.pop("chargePointId", UNSET)

        connector_id = d.pop("connectorId", UNSET)

        _cdr_location = d.pop("cdrLocation", UNSET)
        cdr_location: Union[Unset, CdrLocationDto]
        if isinstance(_cdr_location, Unset) or _cdr_location is None:
            cdr_location = UNSET
        else:
            cdr_location = CdrLocationDto.from_dict(_cdr_location)

        _start_datetime = d.pop("startDatetime", UNSET)
        start_datetime: Union[Unset, datetime.datetime]
        if isinstance(_start_datetime, Unset) or _start_datetime is None:
            start_datetime = UNSET
        else:
            start_datetime = isoparse(_start_datetime)

        _end_date_time = d.pop("endDateTime", UNSET)
        end_date_time: Union[Unset, datetime.datetime]
        if isinstance(_end_date_time, Unset) or _end_date_time is None:
            end_date_time = UNSET
        else:
            end_date_time = isoparse(_end_date_time)

        session_id = d.pop("sessionId", UNSET)

        token = d.pop("token", UNSET)

        _started_by_info = d.pop("startedByInfo", UNSET)
        started_by_info: Union[Unset, CdrStartedByInfoDto]
        if isinstance(_started_by_info, Unset) or _started_by_info is None:
            started_by_info = UNSET
        else:
            started_by_info = CdrStartedByInfoDto.from_dict(_started_by_info)

        total_energy_in_kwh = d.pop("totalEnergyInKwh", UNSET)

        total_time_in_hours = d.pop("totalTimeInHours", UNSET)

        charging_periods = []
        _charging_periods = d.pop("chargingPeriods", UNSET)
        for charging_periods_item_data in _charging_periods or []:
            charging_periods_item = ChargingPeriodDto.from_dict(
                charging_periods_item_data
            )

            charging_periods.append(charging_periods_item)

        total_price = d.pop("totalPrice", UNSET)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset) or _created is None:
            created = UNSET
        else:
            created = isoparse(_created)

        _last_updated = d.pop("lastUpdated", UNSET)
        last_updated: Union[Unset, datetime.datetime]
        if isinstance(_last_updated, Unset) or _last_updated is None:
            last_updated = UNSET
        else:
            last_updated = isoparse(_last_updated)

        ou = d.pop("ou", UNSET)

        ou_id = d.pop("ouId", UNSET)

        ou_name = d.pop("ouName", UNSET)

        tariff_id = d.pop("tariffId", UNSET)

        tariff_name = d.pop("tariffName", UNSET)

        start_tariff = d.pop("startTariff", UNSET)

        tariff_price = d.pop("tariffPrice", UNSET)

        charging_time_tariff = d.pop("chargingTimeTariff", UNSET)

        parking_time_tariff = d.pop("parkingTimeTariff", UNSET)

        _price_info = d.pop("priceInfo", UNSET)
        price_info: Union[Unset, PriceInfoDto]
        if isinstance(_price_info, Unset) or _price_info is None:
            price_info = UNSET
        else:
            price_info = PriceInfoDto.from_dict(_price_info)

        _local_start_date_time = d.pop("localStartDateTime", UNSET)
        local_start_date_time: Union[Unset, datetime.datetime]
        if isinstance(_local_start_date_time, Unset) or _local_start_date_time is None:
            local_start_date_time = UNSET
        else:
            local_start_date_time = isoparse(_local_start_date_time)

        _local_end_date_time = d.pop("localEndDateTime", UNSET)
        local_end_date_time: Union[Unset, datetime.datetime]
        if isinstance(_local_end_date_time, Unset) or _local_end_date_time is None:
            local_end_date_time = UNSET
        else:
            local_end_date_time = isoparse(_local_end_date_time)

        _approval_status = d.pop("approvalStatus", UNSET)
        approval_status: Union[Unset, CdrDtoApprovalStatus]
        if isinstance(_approval_status, Unset) or _approval_status is None:
            approval_status = UNSET
        else:
            approval_status = CdrDtoApprovalStatus(_approval_status)

        _financial_type = d.pop("financialType", UNSET)
        financial_type: Union[Unset, CdrDtoFinancialType]
        if isinstance(_financial_type, Unset) or _financial_type is None:
            financial_type = UNSET
        else:
            financial_type = CdrDtoFinancialType(_financial_type)

        debit_cdr_id = d.pop("debitCdrId", UNSET)

        cdr_dto = cls(
            id=id,
            tenant_id=tenant_id,
            charge_point_id=charge_point_id,
            connector_id=connector_id,
            cdr_location=cdr_location,
            start_datetime=start_datetime,
            end_date_time=end_date_time,
            session_id=session_id,
            token=token,
            started_by_info=started_by_info,
            total_energy_in_kwh=total_energy_in_kwh,
            total_time_in_hours=total_time_in_hours,
            charging_periods=charging_periods,
            total_price=total_price,
            created=created,
            last_updated=last_updated,
            ou=ou,
            ou_id=ou_id,
            ou_name=ou_name,
            tariff_id=tariff_id,
            tariff_name=tariff_name,
            start_tariff=start_tariff,
            tariff_price=tariff_price,
            charging_time_tariff=charging_time_tariff,
            parking_time_tariff=parking_time_tariff,
            price_info=price_info,
            local_start_date_time=local_start_date_time,
            local_end_date_time=local_end_date_time,
            approval_status=approval_status,
            financial_type=financial_type,
            debit_cdr_id=debit_cdr_id,
        )

        cdr_dto.additional_properties = d
        return cdr_dto

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
