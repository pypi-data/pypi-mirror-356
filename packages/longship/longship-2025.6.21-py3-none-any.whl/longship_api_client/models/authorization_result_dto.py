from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.authorization_result_dto_status import AuthorizationResultDtoStatus
from typing import Union
from ..models.authorization_result_dto_reason import AuthorizationResultDtoReason

if TYPE_CHECKING:
    from ..models.authorization_assertion_dto import AuthorizationAssertionDto


T = TypeVar("T", bound="AuthorizationResultDto")


@_attrs_define
class AuthorizationResultDto:
    """
    Attributes:
        assertion (Union[Unset, List['AuthorizationAssertionDto']]):
        status (Union[Unset, AuthorizationResultDtoStatus]):  Default: AuthorizationResultDtoStatus.ACCEPTED.
        reason (Union[Unset, AuthorizationResultDtoReason]):  Default: AuthorizationResultDtoReason.APPROVEDBYREMOTE.
        description (Union[Unset, str]):
    """

    assertion: Union[Unset, List["AuthorizationAssertionDto"]] = UNSET
    status: Union[Unset, AuthorizationResultDtoStatus] = (
        AuthorizationResultDtoStatus.ACCEPTED
    )
    reason: Union[Unset, AuthorizationResultDtoReason] = (
        AuthorizationResultDtoReason.APPROVEDBYREMOTE
    )
    description: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        assertion: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.assertion, Unset):
            assertion = []
            for assertion_item_data in self.assertion:
                assertion_item = assertion_item_data.to_dict()
                assertion.append(assertion_item)

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        reason: Union[Unset, str] = UNSET
        if not isinstance(self.reason, Unset):
            reason = self.reason.value

        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if assertion is not UNSET:
            field_dict["assertion"] = assertion
        if status is not UNSET:
            field_dict["status"] = status
        if reason is not UNSET:
            field_dict["reason"] = reason
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.authorization_assertion_dto import AuthorizationAssertionDto

        d = src_dict.copy()
        assertion = []
        _assertion = d.pop("assertion", UNSET)
        for assertion_item_data in _assertion or []:
            assertion_item = AuthorizationAssertionDto.from_dict(assertion_item_data)

            assertion.append(assertion_item)

        _status = d.pop("status", UNSET)
        status: Union[Unset, AuthorizationResultDtoStatus]
        if isinstance(_status, Unset) or _status is None:
            status = UNSET
        else:
            status = AuthorizationResultDtoStatus(_status)

        _reason = d.pop("reason", UNSET)
        reason: Union[Unset, AuthorizationResultDtoReason]
        if isinstance(_reason, Unset) or _reason is None:
            reason = UNSET
        else:
            reason = AuthorizationResultDtoReason(_reason)

        description = d.pop("description", UNSET)

        authorization_result_dto = cls(
            assertion=assertion,
            status=status,
            reason=reason,
            description=description,
        )

        authorization_result_dto.additional_properties = d
        return authorization_result_dto

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
