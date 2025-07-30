from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.chargepoint_connector_dto_format import ChargepointConnectorDtoFormat
from ..models.chargepoint_connector_dto_standard import ChargepointConnectorDtoStandard
from ..models.chargepoint_connector_dto_power_type import (
    ChargepointConnectorDtoPowerType,
)
from typing import Union
from ..models.chargepoint_connector_dto_operational_status import (
    ChargepointConnectorDtoOperationalStatus,
)


T = TypeVar("T", bound="ChargepointConnectorDto")


@_attrs_define
class ChargepointConnectorDto:
    """
    Attributes:
        id (Union[Unset, str]):
        operational_status (Union[Unset, ChargepointConnectorDtoOperationalStatus]):  Default:
            ChargepointConnectorDtoOperationalStatus.AVAILABLE.
        standard (Union[Unset, ChargepointConnectorDtoStandard]):  Default: ChargepointConnectorDtoStandard.CHADEMO.
        format_ (Union[Unset, ChargepointConnectorDtoFormat]):  Default: ChargepointConnectorDtoFormat.SOCKET.
        power_type (Union[Unset, ChargepointConnectorDtoPowerType]):  Default:
            ChargepointConnectorDtoPowerType.AC_1_PHASE.
        max_voltage (Union[Unset, int]):
        max_amperage (Union[Unset, int]):
        max_electric_power (Union[Unset, int]):
        tariff_id (Union[Unset, str]):
    """

    id: Union[Unset, str] = UNSET
    operational_status: Union[Unset, ChargepointConnectorDtoOperationalStatus] = (
        ChargepointConnectorDtoOperationalStatus.AVAILABLE
    )
    standard: Union[Unset, ChargepointConnectorDtoStandard] = (
        ChargepointConnectorDtoStandard.CHADEMO
    )
    format_: Union[Unset, ChargepointConnectorDtoFormat] = (
        ChargepointConnectorDtoFormat.SOCKET
    )
    power_type: Union[Unset, ChargepointConnectorDtoPowerType] = (
        ChargepointConnectorDtoPowerType.AC_1_PHASE
    )
    max_voltage: Union[Unset, int] = UNSET
    max_amperage: Union[Unset, int] = UNSET
    max_electric_power: Union[Unset, int] = UNSET
    tariff_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        operational_status: Union[Unset, str] = UNSET
        if not isinstance(self.operational_status, Unset):
            operational_status = self.operational_status.value

        standard: Union[Unset, str] = UNSET
        if not isinstance(self.standard, Unset):
            standard = self.standard.value

        format_: Union[Unset, str] = UNSET
        if not isinstance(self.format_, Unset):
            format_ = self.format_.value

        power_type: Union[Unset, str] = UNSET
        if not isinstance(self.power_type, Unset):
            power_type = self.power_type.value

        max_voltage = self.max_voltage

        max_amperage = self.max_amperage

        max_electric_power = self.max_electric_power

        tariff_id = self.tariff_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if operational_status is not UNSET:
            field_dict["operationalStatus"] = operational_status
        if standard is not UNSET:
            field_dict["standard"] = standard
        if format_ is not UNSET:
            field_dict["format"] = format_
        if power_type is not UNSET:
            field_dict["powerType"] = power_type
        if max_voltage is not UNSET:
            field_dict["maxVoltage"] = max_voltage
        if max_amperage is not UNSET:
            field_dict["maxAmperage"] = max_amperage
        if max_electric_power is not UNSET:
            field_dict["maxElectricPower"] = max_electric_power
        if tariff_id is not UNSET:
            field_dict["tariffId"] = tariff_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _operational_status = d.pop("operationalStatus", UNSET)
        operational_status: Union[Unset, ChargepointConnectorDtoOperationalStatus]
        if isinstance(_operational_status, Unset) or _operational_status is None:
            operational_status = UNSET
        else:
            operational_status = ChargepointConnectorDtoOperationalStatus(
                _operational_status
            )

        _standard = d.pop("standard", UNSET)
        standard: Union[Unset, ChargepointConnectorDtoStandard]
        if isinstance(_standard, Unset) or _standard is None:
            standard = UNSET
        else:
            standard = ChargepointConnectorDtoStandard(_standard)

        _format_ = d.pop("format", UNSET)
        format_: Union[Unset, ChargepointConnectorDtoFormat]
        if isinstance(_format_, Unset) or _format_ is None:
            format_ = UNSET
        else:
            format_ = ChargepointConnectorDtoFormat(_format_)

        _power_type = d.pop("powerType", UNSET)
        power_type: Union[Unset, ChargepointConnectorDtoPowerType]
        if isinstance(_power_type, Unset) or _power_type is None:
            power_type = UNSET
        else:
            power_type = ChargepointConnectorDtoPowerType(_power_type)

        max_voltage = d.pop("maxVoltage", UNSET)

        max_amperage = d.pop("maxAmperage", UNSET)

        max_electric_power = d.pop("maxElectricPower", UNSET)

        tariff_id = d.pop("tariffId", UNSET)

        chargepoint_connector_dto = cls(
            id=id,
            operational_status=operational_status,
            standard=standard,
            format_=format_,
            power_type=power_type,
            max_voltage=max_voltage,
            max_amperage=max_amperage,
            max_electric_power=max_electric_power,
            tariff_id=tariff_id,
        )

        chargepoint_connector_dto.additional_properties = d
        return chargepoint_connector_dto

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
