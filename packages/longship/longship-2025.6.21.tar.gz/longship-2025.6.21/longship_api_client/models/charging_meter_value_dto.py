from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from ..models.charging_meter_value_dto_measurand import ChargingMeterValueDtoMeasurand
import datetime
from ..models.charging_meter_value_dto_unit import ChargingMeterValueDtoUnit
from typing import Union


T = TypeVar("T", bound="ChargingMeterValueDto")


@_attrs_define
class ChargingMeterValueDto:
    """
    Attributes:
        timestamp (Union[Unset, datetime.datetime]):
        value (Union[Unset, str]):
        measurand (Union[Unset, ChargingMeterValueDtoMeasurand]):  Default:
            ChargingMeterValueDtoMeasurand.ENERGY_ACTIVE_EXPORT_REGISTER.
        unit (Union[Unset, ChargingMeterValueDtoUnit]):  Default: ChargingMeterValueDtoUnit.WH.
    """

    timestamp: Union[Unset, datetime.datetime] = UNSET
    value: Union[Unset, str] = UNSET
    measurand: Union[Unset, ChargingMeterValueDtoMeasurand] = (
        ChargingMeterValueDtoMeasurand.ENERGY_ACTIVE_EXPORT_REGISTER
    )
    unit: Union[Unset, ChargingMeterValueDtoUnit] = ChargingMeterValueDtoUnit.WH
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        timestamp: Union[Unset, str] = UNSET
        if not isinstance(self.timestamp, Unset):
            timestamp = self.timestamp.isoformat()

        value = self.value

        measurand: Union[Unset, str] = UNSET
        if not isinstance(self.measurand, Unset):
            measurand = self.measurand.value

        unit: Union[Unset, str] = UNSET
        if not isinstance(self.unit, Unset):
            unit = self.unit.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if value is not UNSET:
            field_dict["value"] = value
        if measurand is not UNSET:
            field_dict["measurand"] = measurand
        if unit is not UNSET:
            field_dict["unit"] = unit

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _timestamp = d.pop("timestamp", UNSET)
        timestamp: Union[Unset, datetime.datetime]
        if isinstance(_timestamp, Unset) or _timestamp is None:
            timestamp = UNSET
        else:
            timestamp = isoparse(_timestamp)

        value = d.pop("value", UNSET)

        _measurand = d.pop("measurand", UNSET)
        measurand: Union[Unset, ChargingMeterValueDtoMeasurand]
        if isinstance(_measurand, Unset) or _measurand is None:
            measurand = UNSET
        else:
            measurand = ChargingMeterValueDtoMeasurand(_measurand)

        _unit = d.pop("unit", UNSET)
        unit: Union[Unset, ChargingMeterValueDtoUnit]
        if isinstance(_unit, Unset) or _unit is None:
            unit = UNSET
        else:
            unit = ChargingMeterValueDtoUnit(_unit)

        charging_meter_value_dto = cls(
            timestamp=timestamp,
            value=value,
            measurand=measurand,
            unit=unit,
        )

        charging_meter_value_dto.additional_properties = d
        return charging_meter_value_dto

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
