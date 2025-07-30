from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
import datetime
from ..models.connector_dto_format import ConnectorDtoFormat
from ..models.connector_dto_power_type import ConnectorDtoPowerType
from typing import Union
from ..models.connector_dto_standard import ConnectorDtoStandard


T = TypeVar("T", bound="ConnectorDto")


@_attrs_define
class ConnectorDto:
    """
    Attributes:
        id (Union[Unset, str]):
        standard (Union[Unset, ConnectorDtoStandard]):  Default: ConnectorDtoStandard.CHADEMO.
        format_ (Union[Unset, ConnectorDtoFormat]):  Default: ConnectorDtoFormat.SOCKET.
        power_type (Union[Unset, ConnectorDtoPowerType]):  Default: ConnectorDtoPowerType.AC_1_PHASE.
        max_voltage (Union[Unset, int]):
        max_amperage (Union[Unset, int]):
        max_electric_power (Union[Unset, int]):
        calc_max_electric_power (Union[Unset, bool]):
        last_updated (Union[Unset, datetime.datetime]):
    """

    id: Union[Unset, str] = UNSET
    standard: Union[Unset, ConnectorDtoStandard] = ConnectorDtoStandard.CHADEMO
    format_: Union[Unset, ConnectorDtoFormat] = ConnectorDtoFormat.SOCKET
    power_type: Union[Unset, ConnectorDtoPowerType] = ConnectorDtoPowerType.AC_1_PHASE
    max_voltage: Union[Unset, int] = UNSET
    max_amperage: Union[Unset, int] = UNSET
    max_electric_power: Union[Unset, int] = UNSET
    calc_max_electric_power: Union[Unset, bool] = UNSET
    last_updated: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

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

        calc_max_electric_power = self.calc_max_electric_power

        last_updated: Union[Unset, str] = UNSET
        if not isinstance(self.last_updated, Unset):
            last_updated = self.last_updated.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if standard is not UNSET:
            field_dict["standard"] = standard
        if format_ is not UNSET:
            field_dict["format"] = format_
        if power_type is not UNSET:
            field_dict["power_type"] = power_type
        if max_voltage is not UNSET:
            field_dict["max_voltage"] = max_voltage
        if max_amperage is not UNSET:
            field_dict["max_amperage"] = max_amperage
        if max_electric_power is not UNSET:
            field_dict["max_electric_power"] = max_electric_power
        if calc_max_electric_power is not UNSET:
            field_dict["calc_max_electric_power"] = calc_max_electric_power
        if last_updated is not UNSET:
            field_dict["last_updated"] = last_updated

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _standard = d.pop("standard", UNSET)
        standard: Union[Unset, ConnectorDtoStandard]
        if isinstance(_standard, Unset) or _standard is None:
            standard = UNSET
        else:
            standard = ConnectorDtoStandard(_standard)

        _format_ = d.pop("format", UNSET)
        format_: Union[Unset, ConnectorDtoFormat]
        if isinstance(_format_, Unset) or _format_ is None:
            format_ = UNSET
        else:
            format_ = ConnectorDtoFormat(_format_)

        _power_type = d.pop("power_type", UNSET)
        power_type: Union[Unset, ConnectorDtoPowerType]
        if isinstance(_power_type, Unset) or _power_type is None:
            power_type = UNSET
        else:
            power_type = ConnectorDtoPowerType(_power_type)

        max_voltage = d.pop("max_voltage", UNSET)

        max_amperage = d.pop("max_amperage", UNSET)

        max_electric_power = d.pop("max_electric_power", UNSET)

        calc_max_electric_power = d.pop("calc_max_electric_power", UNSET)

        _last_updated = d.pop("last_updated", UNSET)
        last_updated: Union[Unset, datetime.datetime]
        if isinstance(_last_updated, Unset) or _last_updated is None:
            last_updated = UNSET
        else:
            last_updated = isoparse(_last_updated)

        connector_dto = cls(
            id=id,
            standard=standard,
            format_=format_,
            power_type=power_type,
            max_voltage=max_voltage,
            max_amperage=max_amperage,
            max_electric_power=max_electric_power,
            calc_max_electric_power=calc_max_electric_power,
            last_updated=last_updated,
        )

        connector_dto.additional_properties = d
        return connector_dto

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
