from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.trigger_message_request_requested_message import (
    TriggerMessageRequestRequestedMessage,
)
from typing import Union


T = TypeVar("T", bound="TriggerMessageRequest")


@_attrs_define
class TriggerMessageRequest:
    """
    Attributes:
        requested_message (TriggerMessageRequestRequestedMessage):  Default:
            TriggerMessageRequestRequestedMessage.BOOTNOTIFICATION.
        connector_id (Union[Unset, int]):
    """

    requested_message: TriggerMessageRequestRequestedMessage = (
        TriggerMessageRequestRequestedMessage.BOOTNOTIFICATION
    )
    connector_id: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        requested_message = self.requested_message.value

        connector_id = self.connector_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "requestedMessage": requested_message,
            }
        )
        if connector_id is not UNSET:
            field_dict["connectorId"] = connector_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        requested_message = TriggerMessageRequestRequestedMessage(
            d.pop("requestedMessage")
        )

        connector_id = d.pop("connectorId", UNSET)

        trigger_message_request = cls(
            requested_message=requested_message,
            connector_id=connector_id,
        )

        trigger_message_request.additional_properties = d
        return trigger_message_request

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
