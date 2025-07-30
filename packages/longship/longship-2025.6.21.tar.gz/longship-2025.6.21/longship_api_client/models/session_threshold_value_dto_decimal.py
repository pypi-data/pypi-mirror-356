from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.session_threshold_value_dto_decimal_threshold_hit_outcome import (
    SessionThresholdValueDtoDecimalThresholdHitOutcome,
)
from ..models.session_threshold_value_dto_decimal_status import (
    SessionThresholdValueDtoDecimalStatus,
)
from typing import Union


T = TypeVar("T", bound="SessionThresholdValueDtoDecimal")


@_attrs_define
class SessionThresholdValueDtoDecimal:
    """
    Attributes:
        threshold_value (Union[Unset, float]):
        threshold_hit_outcome (Union[Unset, SessionThresholdValueDtoDecimalThresholdHitOutcome]):  Default:
            SessionThresholdValueDtoDecimalThresholdHitOutcome.SUSPICIOUS.
        status (Union[Unset, SessionThresholdValueDtoDecimalStatus]):  Default:
            SessionThresholdValueDtoDecimalStatus.PENDING.
        result (Union[Unset, str]):
        is_enabled (Union[Unset, bool]):
    """

    threshold_value: Union[Unset, float] = UNSET
    threshold_hit_outcome: Union[
        Unset, SessionThresholdValueDtoDecimalThresholdHitOutcome
    ] = SessionThresholdValueDtoDecimalThresholdHitOutcome.SUSPICIOUS
    status: Union[Unset, SessionThresholdValueDtoDecimalStatus] = (
        SessionThresholdValueDtoDecimalStatus.PENDING
    )
    result: Union[Unset, str] = UNSET
    is_enabled: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        threshold_value = self.threshold_value

        threshold_hit_outcome: Union[Unset, str] = UNSET
        if not isinstance(self.threshold_hit_outcome, Unset):
            threshold_hit_outcome = self.threshold_hit_outcome.value

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        result = self.result

        is_enabled = self.is_enabled

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if threshold_value is not UNSET:
            field_dict["thresholdValue"] = threshold_value
        if threshold_hit_outcome is not UNSET:
            field_dict["thresholdHitOutcome"] = threshold_hit_outcome
        if status is not UNSET:
            field_dict["status"] = status
        if result is not UNSET:
            field_dict["result"] = result
        if is_enabled is not UNSET:
            field_dict["isEnabled"] = is_enabled

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        threshold_value = d.pop("thresholdValue", UNSET)

        _threshold_hit_outcome = d.pop("thresholdHitOutcome", UNSET)
        threshold_hit_outcome: Union[
            Unset, SessionThresholdValueDtoDecimalThresholdHitOutcome
        ]
        if isinstance(_threshold_hit_outcome, Unset) or _threshold_hit_outcome is None:
            threshold_hit_outcome = UNSET
        else:
            threshold_hit_outcome = SessionThresholdValueDtoDecimalThresholdHitOutcome(
                _threshold_hit_outcome
            )

        _status = d.pop("status", UNSET)
        status: Union[Unset, SessionThresholdValueDtoDecimalStatus]
        if isinstance(_status, Unset) or _status is None:
            status = UNSET
        else:
            status = SessionThresholdValueDtoDecimalStatus(_status)

        result = d.pop("result", UNSET)

        is_enabled = d.pop("isEnabled", UNSET)

        session_threshold_value_dto_decimal = cls(
            threshold_value=threshold_value,
            threshold_hit_outcome=threshold_hit_outcome,
            status=status,
            result=result,
            is_enabled=is_enabled,
        )

        session_threshold_value_dto_decimal.additional_properties = d
        return session_threshold_value_dto_decimal

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
