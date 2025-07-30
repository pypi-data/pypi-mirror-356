from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
import datetime
from typing import Union
from ..models.connector_operational_status_dto_operational_status import (
    ConnectorOperationalStatusDtoOperationalStatus,
)


T = TypeVar("T", bound="ConnectorOperationalStatusDto")


@_attrs_define
class ConnectorOperationalStatusDto:
    """
    Attributes:
        connector_number (Union[Unset, int]):
        operational_status (Union[Unset, ConnectorOperationalStatusDtoOperationalStatus]):  Default:
            ConnectorOperationalStatusDtoOperationalStatus.AVAILABLE.
        timestamp (Union[Unset, datetime.datetime]):
    """

    connector_number: Union[Unset, int] = UNSET
    operational_status: Union[Unset, ConnectorOperationalStatusDtoOperationalStatus] = (
        ConnectorOperationalStatusDtoOperationalStatus.AVAILABLE
    )
    timestamp: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        connector_number = self.connector_number

        operational_status: Union[Unset, str] = UNSET
        if not isinstance(self.operational_status, Unset):
            operational_status = self.operational_status.value

        timestamp: Union[Unset, str] = UNSET
        if not isinstance(self.timestamp, Unset):
            timestamp = self.timestamp.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if connector_number is not UNSET:
            field_dict["connectorNumber"] = connector_number
        if operational_status is not UNSET:
            field_dict["operationalStatus"] = operational_status
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        connector_number = d.pop("connectorNumber", UNSET)

        _operational_status = d.pop("operationalStatus", UNSET)
        operational_status: Union[Unset, ConnectorOperationalStatusDtoOperationalStatus]
        if isinstance(_operational_status, Unset) or _operational_status is None:
            operational_status = UNSET
        else:
            operational_status = ConnectorOperationalStatusDtoOperationalStatus(
                _operational_status
            )

        _timestamp = d.pop("timestamp", UNSET)
        timestamp: Union[Unset, datetime.datetime]
        if isinstance(_timestamp, Unset) or _timestamp is None:
            timestamp = UNSET
        else:
            timestamp = isoparse(_timestamp)

        connector_operational_status_dto = cls(
            connector_number=connector_number,
            operational_status=operational_status,
            timestamp=timestamp,
        )

        connector_operational_status_dto.additional_properties = d
        return connector_operational_status_dto

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
