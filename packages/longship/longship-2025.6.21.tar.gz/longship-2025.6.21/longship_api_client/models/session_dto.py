from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.session_dto_approval_status import SessionDtoApprovalStatus
from dateutil.parser import isoparse
from ..models.session_dto_status import SessionDtoStatus
import datetime
from typing import Union
from ..models.session_dto_review_scenario_type import SessionDtoReviewScenarioType

if TYPE_CHECKING:
    from ..models.charging_meter_value_dto import ChargingMeterValueDto
    from ..models.session_location_dto import SessionLocationDto
    from ..models.price_info_dto import PriceInfoDto
    from ..models.tariff_info_dto import TariffInfoDto
    from ..models.session_thresholds_dto import SessionThresholdsDto
    from ..models.started_by_info_dto import StartedByInfoDto
    from ..models.charging_period_dto import ChargingPeriodDto


T = TypeVar("T", bound="SessionDto")


@_attrs_define
class SessionDto:
    """
    Attributes:
        id (Union[Unset, str]):
        tenant_id (Union[Unset, str]):
        charge_point_id (Union[Unset, str]):
        transaction_id (Union[Unset, int]):
        ocpp_transaction_id (Union[Unset, str]):
        connector_id (Union[Unset, int]):
        session_location (Union[Unset, SessionLocationDto]):
        id_tag (Union[Unset, str]):
        started_by_info (Union[Unset, StartedByInfoDto]):
        meter_start_in_wh (Union[Unset, int]):
        session_start (Union[Unset, datetime.datetime]):
        charging_periods (Union[Unset, List['ChargingPeriodDto']]):
        charging_meter_values (Union[Unset, List['ChargingMeterValueDto']]):
        meter_stop_in_wh (Union[Unset, int]):
        session_stop (Union[Unset, datetime.datetime]):
        status (Union[Unset, SessionDtoStatus]):  Default: SessionDtoStatus.ACTIVE.
        approval_status (Union[Unset, SessionDtoApprovalStatus]):  Default: SessionDtoApprovalStatus.VALUE_0.
        review_scenario_type (Union[Unset, SessionDtoReviewScenarioType]):  Default:
            SessionDtoReviewScenarioType.VALUE_0.
        total_energy_in_kwh (Union[Unset, float]):
        total_price (Union[Unset, float]):
        created (Union[Unset, datetime.datetime]):
        last_updated (Union[Unset, datetime.datetime]):
        ou (Union[Unset, str]):
        ou_id (Union[Unset, str]):
        ou_name (Union[Unset, str]):
        tariff_info (Union[Unset, TariffInfoDto]):
        price_info (Union[Unset, PriceInfoDto]):
        tariff_id (Union[Unset, str]):
        tariff_name (Union[Unset, str]):
        start_tariff (Union[Unset, float]):
        tariff_price (Union[Unset, float]):
        parking_tariff (Union[Unset, float]):
        thresholds (Union[Unset, SessionThresholdsDto]):
        parking_step_size (Union[Unset, int]):
        delay_in_minutes (Union[Unset, int]):
        parking_time_start (Union[Unset, datetime.datetime]):
    """

    id: Union[Unset, str] = UNSET
    tenant_id: Union[Unset, str] = UNSET
    charge_point_id: Union[Unset, str] = UNSET
    transaction_id: Union[Unset, int] = UNSET
    ocpp_transaction_id: Union[Unset, str] = UNSET
    connector_id: Union[Unset, int] = UNSET
    session_location: Union[Unset, "SessionLocationDto"] = UNSET
    id_tag: Union[Unset, str] = UNSET
    started_by_info: Union[Unset, "StartedByInfoDto"] = UNSET
    meter_start_in_wh: Union[Unset, int] = UNSET
    session_start: Union[Unset, datetime.datetime] = UNSET
    charging_periods: Union[Unset, List["ChargingPeriodDto"]] = UNSET
    charging_meter_values: Union[Unset, List["ChargingMeterValueDto"]] = UNSET
    meter_stop_in_wh: Union[Unset, int] = UNSET
    session_stop: Union[Unset, datetime.datetime] = UNSET
    status: Union[Unset, SessionDtoStatus] = SessionDtoStatus.ACTIVE
    approval_status: Union[Unset, SessionDtoApprovalStatus] = (
        SessionDtoApprovalStatus.VALUE_0
    )
    review_scenario_type: Union[Unset, SessionDtoReviewScenarioType] = (
        SessionDtoReviewScenarioType.VALUE_0
    )
    total_energy_in_kwh: Union[Unset, float] = UNSET
    total_price: Union[Unset, float] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    last_updated: Union[Unset, datetime.datetime] = UNSET
    ou: Union[Unset, str] = UNSET
    ou_id: Union[Unset, str] = UNSET
    ou_name: Union[Unset, str] = UNSET
    tariff_info: Union[Unset, "TariffInfoDto"] = UNSET
    price_info: Union[Unset, "PriceInfoDto"] = UNSET
    tariff_id: Union[Unset, str] = UNSET
    tariff_name: Union[Unset, str] = UNSET
    start_tariff: Union[Unset, float] = UNSET
    tariff_price: Union[Unset, float] = UNSET
    parking_tariff: Union[Unset, float] = UNSET
    thresholds: Union[Unset, "SessionThresholdsDto"] = UNSET
    parking_step_size: Union[Unset, int] = UNSET
    delay_in_minutes: Union[Unset, int] = UNSET
    parking_time_start: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        tenant_id = self.tenant_id

        charge_point_id = self.charge_point_id

        transaction_id = self.transaction_id

        ocpp_transaction_id = self.ocpp_transaction_id

        connector_id = self.connector_id

        session_location: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.session_location, Unset):
            session_location = self.session_location.to_dict()

        id_tag = self.id_tag

        started_by_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.started_by_info, Unset):
            started_by_info = self.started_by_info.to_dict()

        meter_start_in_wh = self.meter_start_in_wh

        session_start: Union[Unset, str] = UNSET
        if not isinstance(self.session_start, Unset):
            session_start = self.session_start.isoformat()

        charging_periods: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.charging_periods, Unset):
            charging_periods = []
            for charging_periods_item_data in self.charging_periods:
                charging_periods_item = charging_periods_item_data.to_dict()
                charging_periods.append(charging_periods_item)

        charging_meter_values: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.charging_meter_values, Unset):
            charging_meter_values = []
            for charging_meter_values_item_data in self.charging_meter_values:
                charging_meter_values_item = charging_meter_values_item_data.to_dict()
                charging_meter_values.append(charging_meter_values_item)

        meter_stop_in_wh = self.meter_stop_in_wh

        session_stop: Union[Unset, str] = UNSET
        if not isinstance(self.session_stop, Unset):
            session_stop = self.session_stop.isoformat()

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        approval_status: Union[Unset, int] = UNSET
        if not isinstance(self.approval_status, Unset):
            approval_status = self.approval_status.value

        review_scenario_type: Union[Unset, int] = UNSET
        if not isinstance(self.review_scenario_type, Unset):
            review_scenario_type = self.review_scenario_type.value

        total_energy_in_kwh = self.total_energy_in_kwh

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

        tariff_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.tariff_info, Unset):
            tariff_info = self.tariff_info.to_dict()

        price_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.price_info, Unset):
            price_info = self.price_info.to_dict()

        tariff_id = self.tariff_id

        tariff_name = self.tariff_name

        start_tariff = self.start_tariff

        tariff_price = self.tariff_price

        parking_tariff = self.parking_tariff

        thresholds: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.thresholds, Unset):
            thresholds = self.thresholds.to_dict()

        parking_step_size = self.parking_step_size

        delay_in_minutes = self.delay_in_minutes

        parking_time_start: Union[Unset, str] = UNSET
        if not isinstance(self.parking_time_start, Unset):
            parking_time_start = self.parking_time_start.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id
        if charge_point_id is not UNSET:
            field_dict["chargePointId"] = charge_point_id
        if transaction_id is not UNSET:
            field_dict["transactionId"] = transaction_id
        if ocpp_transaction_id is not UNSET:
            field_dict["ocppTransactionId"] = ocpp_transaction_id
        if connector_id is not UNSET:
            field_dict["connectorId"] = connector_id
        if session_location is not UNSET:
            field_dict["sessionLocation"] = session_location
        if id_tag is not UNSET:
            field_dict["idTag"] = id_tag
        if started_by_info is not UNSET:
            field_dict["startedByInfo"] = started_by_info
        if meter_start_in_wh is not UNSET:
            field_dict["meterStartInWh"] = meter_start_in_wh
        if session_start is not UNSET:
            field_dict["sessionStart"] = session_start
        if charging_periods is not UNSET:
            field_dict["chargingPeriods"] = charging_periods
        if charging_meter_values is not UNSET:
            field_dict["chargingMeterValues"] = charging_meter_values
        if meter_stop_in_wh is not UNSET:
            field_dict["meterStopInWh"] = meter_stop_in_wh
        if session_stop is not UNSET:
            field_dict["sessionStop"] = session_stop
        if status is not UNSET:
            field_dict["status"] = status
        if approval_status is not UNSET:
            field_dict["approvalStatus"] = approval_status
        if review_scenario_type is not UNSET:
            field_dict["reviewScenarioType"] = review_scenario_type
        if total_energy_in_kwh is not UNSET:
            field_dict["totalEnergyInKwh"] = total_energy_in_kwh
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
        if tariff_info is not UNSET:
            field_dict["tariffInfo"] = tariff_info
        if price_info is not UNSET:
            field_dict["priceInfo"] = price_info
        if tariff_id is not UNSET:
            field_dict["tariffId"] = tariff_id
        if tariff_name is not UNSET:
            field_dict["tariffName"] = tariff_name
        if start_tariff is not UNSET:
            field_dict["startTariff"] = start_tariff
        if tariff_price is not UNSET:
            field_dict["tariffPrice"] = tariff_price
        if parking_tariff is not UNSET:
            field_dict["parkingTariff"] = parking_tariff
        if thresholds is not UNSET:
            field_dict["thresholds"] = thresholds
        if parking_step_size is not UNSET:
            field_dict["parkingStepSize"] = parking_step_size
        if delay_in_minutes is not UNSET:
            field_dict["delayInMinutes"] = delay_in_minutes
        if parking_time_start is not UNSET:
            field_dict["parkingTimeStart"] = parking_time_start

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.charging_meter_value_dto import ChargingMeterValueDto
        from ..models.session_location_dto import SessionLocationDto
        from ..models.price_info_dto import PriceInfoDto
        from ..models.tariff_info_dto import TariffInfoDto
        from ..models.session_thresholds_dto import SessionThresholdsDto
        from ..models.started_by_info_dto import StartedByInfoDto
        from ..models.charging_period_dto import ChargingPeriodDto

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        tenant_id = d.pop("tenantId", UNSET)

        charge_point_id = d.pop("chargePointId", UNSET)

        transaction_id = d.pop("transactionId", UNSET)

        ocpp_transaction_id = d.pop("ocppTransactionId", UNSET)

        connector_id = d.pop("connectorId", UNSET)

        _session_location = d.pop("sessionLocation", UNSET)
        session_location: Union[Unset, SessionLocationDto]
        if isinstance(_session_location, Unset) or _session_location is None:
            session_location = UNSET
        else:
            session_location = SessionLocationDto.from_dict(_session_location)

        id_tag = d.pop("idTag", UNSET)

        _started_by_info = d.pop("startedByInfo", UNSET)
        started_by_info: Union[Unset, StartedByInfoDto]
        if isinstance(_started_by_info, Unset) or _started_by_info is None:
            started_by_info = UNSET
        else:
            started_by_info = StartedByInfoDto.from_dict(_started_by_info)

        meter_start_in_wh = d.pop("meterStartInWh", UNSET)

        _session_start = d.pop("sessionStart", UNSET)
        session_start: Union[Unset, datetime.datetime]
        if isinstance(_session_start, Unset) or _session_start is None:
            session_start = UNSET
        else:
            session_start = isoparse(_session_start)

        charging_periods = []
        _charging_periods = d.pop("chargingPeriods", UNSET)
        for charging_periods_item_data in _charging_periods or []:
            charging_periods_item = ChargingPeriodDto.from_dict(
                charging_periods_item_data
            )

            charging_periods.append(charging_periods_item)

        charging_meter_values = []
        _charging_meter_values = d.pop("chargingMeterValues", UNSET)
        for charging_meter_values_item_data in _charging_meter_values or []:
            charging_meter_values_item = ChargingMeterValueDto.from_dict(
                charging_meter_values_item_data
            )

            charging_meter_values.append(charging_meter_values_item)

        meter_stop_in_wh = d.pop("meterStopInWh", UNSET)

        _session_stop = d.pop("sessionStop", UNSET)
        session_stop: Union[Unset, datetime.datetime]
        if isinstance(_session_stop, Unset) or _session_stop is None:
            session_stop = UNSET
        else:
            session_stop = isoparse(_session_stop)

        _status = d.pop("status", UNSET)
        status: Union[Unset, SessionDtoStatus]
        if isinstance(_status, Unset) or _status is None:
            status = UNSET
        else:
            status = SessionDtoStatus(_status)

        _approval_status = d.pop("approvalStatus", UNSET)
        approval_status: Union[Unset, SessionDtoApprovalStatus]
        if isinstance(_approval_status, Unset) or _approval_status is None:
            approval_status = UNSET
        else:
            approval_status = SessionDtoApprovalStatus(_approval_status)

        _review_scenario_type = d.pop("reviewScenarioType", UNSET)
        review_scenario_type: Union[Unset, SessionDtoReviewScenarioType]
        if isinstance(_review_scenario_type, Unset) or _review_scenario_type is None:
            review_scenario_type = UNSET
        else:
            review_scenario_type = SessionDtoReviewScenarioType(_review_scenario_type)

        total_energy_in_kwh = d.pop("totalEnergyInKwh", UNSET)

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

        _tariff_info = d.pop("tariffInfo", UNSET)
        tariff_info: Union[Unset, TariffInfoDto]
        if isinstance(_tariff_info, Unset) or _tariff_info is None:
            tariff_info = UNSET
        else:
            tariff_info = TariffInfoDto.from_dict(_tariff_info)

        _price_info = d.pop("priceInfo", UNSET)
        price_info: Union[Unset, PriceInfoDto]
        if isinstance(_price_info, Unset) or _price_info is None:
            price_info = UNSET
        else:
            price_info = PriceInfoDto.from_dict(_price_info)

        tariff_id = d.pop("tariffId", UNSET)

        tariff_name = d.pop("tariffName", UNSET)

        start_tariff = d.pop("startTariff", UNSET)

        tariff_price = d.pop("tariffPrice", UNSET)

        parking_tariff = d.pop("parkingTariff", UNSET)

        _thresholds = d.pop("thresholds", UNSET)
        thresholds: Union[Unset, SessionThresholdsDto]
        if isinstance(_thresholds, Unset) or _thresholds is None:
            thresholds = UNSET
        else:
            thresholds = SessionThresholdsDto.from_dict(_thresholds)

        parking_step_size = d.pop("parkingStepSize", UNSET)

        delay_in_minutes = d.pop("delayInMinutes", UNSET)

        _parking_time_start = d.pop("parkingTimeStart", UNSET)
        parking_time_start: Union[Unset, datetime.datetime]
        if isinstance(_parking_time_start, Unset) or _parking_time_start is None:
            parking_time_start = UNSET
        else:
            parking_time_start = isoparse(_parking_time_start)

        session_dto = cls(
            id=id,
            tenant_id=tenant_id,
            charge_point_id=charge_point_id,
            transaction_id=transaction_id,
            ocpp_transaction_id=ocpp_transaction_id,
            connector_id=connector_id,
            session_location=session_location,
            id_tag=id_tag,
            started_by_info=started_by_info,
            meter_start_in_wh=meter_start_in_wh,
            session_start=session_start,
            charging_periods=charging_periods,
            charging_meter_values=charging_meter_values,
            meter_stop_in_wh=meter_stop_in_wh,
            session_stop=session_stop,
            status=status,
            approval_status=approval_status,
            review_scenario_type=review_scenario_type,
            total_energy_in_kwh=total_energy_in_kwh,
            total_price=total_price,
            created=created,
            last_updated=last_updated,
            ou=ou,
            ou_id=ou_id,
            ou_name=ou_name,
            tariff_info=tariff_info,
            price_info=price_info,
            tariff_id=tariff_id,
            tariff_name=tariff_name,
            start_tariff=start_tariff,
            tariff_price=tariff_price,
            parking_tariff=parking_tariff,
            thresholds=thresholds,
            parking_step_size=parking_step_size,
            delay_in_minutes=delay_in_minutes,
            parking_time_start=parking_time_start,
        )

        session_dto.additional_properties = d
        return session_dto

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
