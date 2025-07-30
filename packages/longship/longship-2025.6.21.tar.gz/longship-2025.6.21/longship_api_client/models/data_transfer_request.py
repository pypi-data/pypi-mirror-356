from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="DataTransferRequest")


@_attrs_define
class DataTransferRequest:
    """
    Attributes:
        vendor_id (str):
        message_id (Union[Unset, str]):
        data (Union[Unset, str]):
    """

    vendor_id: str
    message_id: Union[Unset, str] = UNSET
    data: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        vendor_id = self.vendor_id

        message_id = self.message_id

        data = self.data

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "vendorId": vendor_id,
            }
        )
        if message_id is not UNSET:
            field_dict["messageId"] = message_id
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        vendor_id = d.pop("vendorId")

        message_id = d.pop("messageId", UNSET)

        data = d.pop("data", UNSET)

        data_transfer_request = cls(
            vendor_id=vendor_id,
            message_id=message_id,
            data=data,
        )

        data_transfer_request.additional_properties = d
        return data_transfer_request

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
