from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from ..models.message_log_dto_ocpp_message_type import MessageLogDtoOcppMessageType
import datetime
from typing import Union
from ..models.message_log_dto_wamp_message_type import MessageLogDtoWampMessageType
from ..models.message_log_dto_direction import MessageLogDtoDirection


T = TypeVar("T", bound="MessageLogDto")


@_attrs_define
class MessageLogDto:
    """
    Attributes:
        id (Union[Unset, str]):
        charge_point_id (Union[Unset, str]):
        message_id (Union[Unset, str]):
        wamp_message_type (Union[Unset, MessageLogDtoWampMessageType]):  Default: MessageLogDtoWampMessageType.UNKNOWN.
        ocpp_message_type (Union[Unset, MessageLogDtoOcppMessageType]):  Default:
            MessageLogDtoOcppMessageType.AUTHORIZE.
        direction (Union[Unset, MessageLogDtoDirection]):  Default: MessageLogDtoDirection.UNKNOWN.
        tenant_id (Union[Unset, str]):
        payload (Union[Unset, str]):
        timestamp (Union[Unset, datetime.datetime]):
    """

    id: Union[Unset, str] = UNSET
    charge_point_id: Union[Unset, str] = UNSET
    message_id: Union[Unset, str] = UNSET
    wamp_message_type: Union[Unset, MessageLogDtoWampMessageType] = (
        MessageLogDtoWampMessageType.UNKNOWN
    )
    ocpp_message_type: Union[Unset, MessageLogDtoOcppMessageType] = (
        MessageLogDtoOcppMessageType.AUTHORIZE
    )
    direction: Union[Unset, MessageLogDtoDirection] = MessageLogDtoDirection.UNKNOWN
    tenant_id: Union[Unset, str] = UNSET
    payload: Union[Unset, str] = UNSET
    timestamp: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        charge_point_id = self.charge_point_id

        message_id = self.message_id

        wamp_message_type: Union[Unset, str] = UNSET
        if not isinstance(self.wamp_message_type, Unset):
            wamp_message_type = self.wamp_message_type.value

        ocpp_message_type: Union[Unset, str] = UNSET
        if not isinstance(self.ocpp_message_type, Unset):
            ocpp_message_type = self.ocpp_message_type.value

        direction: Union[Unset, str] = UNSET
        if not isinstance(self.direction, Unset):
            direction = self.direction.value

        tenant_id = self.tenant_id

        payload = self.payload

        timestamp: Union[Unset, str] = UNSET
        if not isinstance(self.timestamp, Unset):
            timestamp = self.timestamp.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if charge_point_id is not UNSET:
            field_dict["chargePointId"] = charge_point_id
        if message_id is not UNSET:
            field_dict["messageId"] = message_id
        if wamp_message_type is not UNSET:
            field_dict["wampMessageType"] = wamp_message_type
        if ocpp_message_type is not UNSET:
            field_dict["ocppMessageType"] = ocpp_message_type
        if direction is not UNSET:
            field_dict["direction"] = direction
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id
        if payload is not UNSET:
            field_dict["payload"] = payload
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        charge_point_id = d.pop("chargePointId", UNSET)

        message_id = d.pop("messageId", UNSET)

        _wamp_message_type = d.pop("wampMessageType", UNSET)
        wamp_message_type: Union[Unset, MessageLogDtoWampMessageType]
        if isinstance(_wamp_message_type, Unset) or _wamp_message_type is None:
            wamp_message_type = UNSET
        else:
            wamp_message_type = MessageLogDtoWampMessageType(_wamp_message_type)

        _ocpp_message_type = d.pop("ocppMessageType", UNSET)
        ocpp_message_type: Union[Unset, MessageLogDtoOcppMessageType]
        if isinstance(_ocpp_message_type, Unset) or _ocpp_message_type is None:
            ocpp_message_type = UNSET
        else:
            ocpp_message_type = MessageLogDtoOcppMessageType(_ocpp_message_type)

        _direction = d.pop("direction", UNSET)
        direction: Union[Unset, MessageLogDtoDirection]
        if isinstance(_direction, Unset) or _direction is None:
            direction = UNSET
        else:
            direction = MessageLogDtoDirection(_direction)

        tenant_id = d.pop("tenantId", UNSET)

        payload = d.pop("payload", UNSET)

        _timestamp = d.pop("timestamp", UNSET)
        timestamp: Union[Unset, datetime.datetime]
        if isinstance(_timestamp, Unset) or _timestamp is None:
            timestamp = UNSET
        else:
            timestamp = isoparse(_timestamp)

        message_log_dto = cls(
            id=id,
            charge_point_id=charge_point_id,
            message_id=message_id,
            wamp_message_type=wamp_message_type,
            ocpp_message_type=ocpp_message_type,
            direction=direction,
            tenant_id=tenant_id,
            payload=payload,
            timestamp=timestamp,
        )

        message_log_dto.additional_properties = d
        return message_log_dto

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
