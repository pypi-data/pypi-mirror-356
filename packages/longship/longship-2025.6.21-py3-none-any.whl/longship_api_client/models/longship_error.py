from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.longship_error_detail import LongshipErrorDetail


T = TypeVar("T", bound="LongshipError")


@_attrs_define
class LongshipError:
    """
    Attributes:
        code (Union[Unset, str]): The error code.
        error_details (Union[Unset, LongshipErrorDetail]): More details about the error.
    """

    code: Union[Unset, str] = UNSET
    error_details: Union[Unset, "LongshipErrorDetail"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        code = self.code

        error_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.error_details, Unset):
            error_details = self.error_details.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if code is not UNSET:
            field_dict["code"] = code
        if error_details is not UNSET:
            field_dict["errorDetails"] = error_details

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.longship_error_detail import LongshipErrorDetail

        d = src_dict.copy()
        code = d.pop("code", UNSET)

        _error_details = d.pop("errorDetails", UNSET)
        error_details: Union[Unset, LongshipErrorDetail]
        if isinstance(_error_details, Unset) or _error_details is None:
            error_details = UNSET
        else:
            error_details = LongshipErrorDetail.from_dict(_error_details)

        longship_error = cls(
            code=code,
            error_details=error_details,
        )

        longship_error.additional_properties = d
        return longship_error

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
