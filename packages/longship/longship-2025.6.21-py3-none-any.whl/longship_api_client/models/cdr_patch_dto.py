from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union
from ..models.cdr_patch_dto_approval_status import CdrPatchDtoApprovalStatus


T = TypeVar("T", bound="CdrPatchDto")


@_attrs_define
class CdrPatchDto:
    """
    Attributes:
        approval_status (Union[Unset, CdrPatchDtoApprovalStatus]):  Default: CdrPatchDtoApprovalStatus.APPROVED.
    """

    approval_status: Union[Unset, CdrPatchDtoApprovalStatus] = (
        CdrPatchDtoApprovalStatus.APPROVED
    )
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        approval_status: Union[Unset, str] = UNSET
        if not isinstance(self.approval_status, Unset):
            approval_status = self.approval_status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if approval_status is not UNSET:
            field_dict["approvalStatus"] = approval_status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _approval_status = d.pop("approvalStatus", UNSET)
        approval_status: Union[Unset, CdrPatchDtoApprovalStatus]
        if isinstance(_approval_status, Unset) or _approval_status is None:
            approval_status = UNSET
        else:
            approval_status = CdrPatchDtoApprovalStatus(_approval_status)

        cdr_patch_dto = cls(
            approval_status=approval_status,
        )

        cdr_patch_dto.additional_properties = d
        return cdr_patch_dto

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
