from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
import datetime
from ..models.chargepoint_status_dto_connectivity_status import (
    ChargepointStatusDtoConnectivityStatus,
)
from typing import Union

if TYPE_CHECKING:
    from ..models.connector_operational_status_dto import ConnectorOperationalStatusDto


T = TypeVar("T", bound="ChargepointStatusDto")


@_attrs_define
class ChargepointStatusDto:
    """
    Attributes:
        id (Union[Unset, str]):
        display_name (Union[Unset, str]):
        tenant_id (Union[Unset, str]):
        ou (Union[Unset, str]):
        ou_id (Union[Unset, str]):
        ou_name (Union[Unset, str]):
        timestamp (Union[Unset, datetime.datetime]):
        connectivity_status (Union[Unset, ChargepointStatusDtoConnectivityStatus]):  Default:
            ChargepointStatusDtoConnectivityStatus.ONLINE.
        connectors (Union[Unset, List['ConnectorOperationalStatusDto']]):
        websocket_connected (Union[Unset, datetime.datetime]):
        websocket_disconnected (Union[Unset, datetime.datetime]):
    """

    id: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    tenant_id: Union[Unset, str] = UNSET
    ou: Union[Unset, str] = UNSET
    ou_id: Union[Unset, str] = UNSET
    ou_name: Union[Unset, str] = UNSET
    timestamp: Union[Unset, datetime.datetime] = UNSET
    connectivity_status: Union[Unset, ChargepointStatusDtoConnectivityStatus] = (
        ChargepointStatusDtoConnectivityStatus.ONLINE
    )
    connectors: Union[Unset, List["ConnectorOperationalStatusDto"]] = UNSET
    websocket_connected: Union[Unset, datetime.datetime] = UNSET
    websocket_disconnected: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        display_name = self.display_name

        tenant_id = self.tenant_id

        ou = self.ou

        ou_id = self.ou_id

        ou_name = self.ou_name

        timestamp: Union[Unset, str] = UNSET
        if not isinstance(self.timestamp, Unset):
            timestamp = self.timestamp.isoformat()

        connectivity_status: Union[Unset, str] = UNSET
        if not isinstance(self.connectivity_status, Unset):
            connectivity_status = self.connectivity_status.value

        connectors: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.connectors, Unset):
            connectors = []
            for connectors_item_data in self.connectors:
                connectors_item = connectors_item_data.to_dict()
                connectors.append(connectors_item)

        websocket_connected: Union[Unset, str] = UNSET
        if not isinstance(self.websocket_connected, Unset):
            websocket_connected = self.websocket_connected.isoformat()

        websocket_disconnected: Union[Unset, str] = UNSET
        if not isinstance(self.websocket_disconnected, Unset):
            websocket_disconnected = self.websocket_disconnected.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id
        if ou is not UNSET:
            field_dict["ou"] = ou
        if ou_id is not UNSET:
            field_dict["ouId"] = ou_id
        if ou_name is not UNSET:
            field_dict["ouName"] = ou_name
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if connectivity_status is not UNSET:
            field_dict["connectivityStatus"] = connectivity_status
        if connectors is not UNSET:
            field_dict["connectors"] = connectors
        if websocket_connected is not UNSET:
            field_dict["websocketConnected"] = websocket_connected
        if websocket_disconnected is not UNSET:
            field_dict["websocketDisconnected"] = websocket_disconnected

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.connector_operational_status_dto import (
            ConnectorOperationalStatusDto,
        )

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        display_name = d.pop("displayName", UNSET)

        tenant_id = d.pop("tenantId", UNSET)

        ou = d.pop("ou", UNSET)

        ou_id = d.pop("ouId", UNSET)

        ou_name = d.pop("ouName", UNSET)

        _timestamp = d.pop("timestamp", UNSET)
        timestamp: Union[Unset, datetime.datetime]
        if isinstance(_timestamp, Unset) or _timestamp is None:
            timestamp = UNSET
        else:
            timestamp = isoparse(_timestamp)

        _connectivity_status = d.pop("connectivityStatus", UNSET)
        connectivity_status: Union[Unset, ChargepointStatusDtoConnectivityStatus]
        if isinstance(_connectivity_status, Unset) or _connectivity_status is None:
            connectivity_status = UNSET
        else:
            connectivity_status = ChargepointStatusDtoConnectivityStatus(
                _connectivity_status
            )

        connectors = []
        _connectors = d.pop("connectors", UNSET)
        for connectors_item_data in _connectors or []:
            connectors_item = ConnectorOperationalStatusDto.from_dict(
                connectors_item_data
            )

            connectors.append(connectors_item)

        _websocket_connected = d.pop("websocketConnected", UNSET)
        websocket_connected: Union[Unset, datetime.datetime]
        if isinstance(_websocket_connected, Unset) or _websocket_connected is None:
            websocket_connected = UNSET
        else:
            websocket_connected = isoparse(_websocket_connected)

        _websocket_disconnected = d.pop("websocketDisconnected", UNSET)
        websocket_disconnected: Union[Unset, datetime.datetime]
        if isinstance(_websocket_disconnected, Unset) or _websocket_disconnected is None:
            websocket_disconnected = UNSET
        else:
            websocket_disconnected = isoparse(_websocket_disconnected)

        chargepoint_status_dto = cls(
            id=id,
            display_name=display_name,
            tenant_id=tenant_id,
            ou=ou,
            ou_id=ou_id,
            ou_name=ou_name,
            timestamp=timestamp,
            connectivity_status=connectivity_status,
            connectors=connectors,
            websocket_connected=websocket_connected,
            websocket_disconnected=websocket_disconnected,
        )

        chargepoint_status_dto.additional_properties = d
        return chargepoint_status_dto

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
