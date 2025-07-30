from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
import datetime
from typing import Union


T = TypeVar("T", bound="UpdateFirmwareRequest")


@_attrs_define
class UpdateFirmwareRequest:
    """
    Attributes:
        location (str):
        retrieve_date (datetime.datetime):
        retries (Union[Unset, int]):
        retry_interval (Union[Unset, int]):
    """

    location: str
    retrieve_date: datetime.datetime
    retries: Union[Unset, int] = UNSET
    retry_interval: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        location = self.location

        retrieve_date = self.retrieve_date.isoformat()

        retries = self.retries

        retry_interval = self.retry_interval

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "location": location,
                "retrieveDate": retrieve_date,
            }
        )
        if retries is not UNSET:
            field_dict["retries"] = retries
        if retry_interval is not UNSET:
            field_dict["retryInterval"] = retry_interval

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        location = d.pop("location")

        retrieve_date = isoparse(d.pop("retrieveDate"))

        retries = d.pop("retries", UNSET)

        retry_interval = d.pop("retryInterval", UNSET)

        update_firmware_request = cls(
            location=location,
            retrieve_date=retrieve_date,
            retries=retries,
            retry_interval=retry_interval,
        )

        update_firmware_request.additional_properties = d
        return update_firmware_request

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
