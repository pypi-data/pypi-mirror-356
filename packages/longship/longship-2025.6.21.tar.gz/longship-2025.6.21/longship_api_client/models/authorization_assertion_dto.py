from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union
from ..models.authorization_assertion_dto_status import AuthorizationAssertionDtoStatus
from ..models.authorization_assertion_dto_auth_scenario_type import (
    AuthorizationAssertionDtoAuthScenarioType,
)


T = TypeVar("T", bound="AuthorizationAssertionDto")


@_attrs_define
class AuthorizationAssertionDto:
    """
    Attributes:
        auth_scenario_type (Union[Unset, AuthorizationAssertionDtoAuthScenarioType]):  Default:
            AuthorizationAssertionDtoAuthScenarioType.NONE.
        auth_result (Union[Unset, str]):
        status (Union[Unset, AuthorizationAssertionDtoStatus]):  Default: AuthorizationAssertionDtoStatus.PENDING.
    """

    auth_scenario_type: Union[Unset, AuthorizationAssertionDtoAuthScenarioType] = (
        AuthorizationAssertionDtoAuthScenarioType.NONE
    )
    auth_result: Union[Unset, str] = UNSET
    status: Union[Unset, AuthorizationAssertionDtoStatus] = (
        AuthorizationAssertionDtoStatus.PENDING
    )
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        auth_scenario_type: Union[Unset, str] = UNSET
        if not isinstance(self.auth_scenario_type, Unset):
            auth_scenario_type = self.auth_scenario_type.value

        auth_result = self.auth_result

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if auth_scenario_type is not UNSET:
            field_dict["authScenarioType"] = auth_scenario_type
        if auth_result is not UNSET:
            field_dict["authResult"] = auth_result
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _auth_scenario_type = d.pop("authScenarioType", UNSET)
        auth_scenario_type: Union[Unset, AuthorizationAssertionDtoAuthScenarioType]
        if isinstance(_auth_scenario_type, Unset) or _auth_scenario_type is None:
            auth_scenario_type = UNSET
        else:
            auth_scenario_type = AuthorizationAssertionDtoAuthScenarioType(
                _auth_scenario_type
            )

        auth_result = d.pop("authResult", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, AuthorizationAssertionDtoStatus]
        if isinstance(_status, Unset) or _status is None:
            status = UNSET
        else:
            status = AuthorizationAssertionDtoStatus(_status)

        authorization_assertion_dto = cls(
            auth_scenario_type=auth_scenario_type,
            auth_result=auth_result,
            status=status,
        )

        authorization_assertion_dto.additional_properties = d
        return authorization_assertion_dto

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
