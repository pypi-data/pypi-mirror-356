from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.tariff_assertion_dto import TariffAssertionDto


T = TypeVar("T", bound="TariffInfoDto")


@_attrs_define
class TariffInfoDto:
    """
    Attributes:
        tariff_id (Union[Unset, str]):
        tariff_name (Union[Unset, str]):
        start_tariff (Union[Unset, float]):
        tariff_price (Union[Unset, float]):
        parking_tariff (Union[Unset, float]):
        parking_step_size_in_minutes (Union[Unset, int]):
        parking_grace_period_in_minutes (Union[Unset, int]):
        time_tariff (Union[Unset, float]):
        time_step_size_in_minutes (Union[Unset, int]):
        time_grace_period_in_minutes (Union[Unset, int]):
        assertions (Union[Unset, List['TariffAssertionDto']]):
    """

    tariff_id: Union[Unset, str] = UNSET
    tariff_name: Union[Unset, str] = UNSET
    start_tariff: Union[Unset, float] = UNSET
    tariff_price: Union[Unset, float] = UNSET
    parking_tariff: Union[Unset, float] = UNSET
    parking_step_size_in_minutes: Union[Unset, int] = UNSET
    parking_grace_period_in_minutes: Union[Unset, int] = UNSET
    time_tariff: Union[Unset, float] = UNSET
    time_step_size_in_minutes: Union[Unset, int] = UNSET
    time_grace_period_in_minutes: Union[Unset, int] = UNSET
    assertions: Union[Unset, List["TariffAssertionDto"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        tariff_id = self.tariff_id

        tariff_name = self.tariff_name

        start_tariff = self.start_tariff

        tariff_price = self.tariff_price

        parking_tariff = self.parking_tariff

        parking_step_size_in_minutes = self.parking_step_size_in_minutes

        parking_grace_period_in_minutes = self.parking_grace_period_in_minutes

        time_tariff = self.time_tariff

        time_step_size_in_minutes = self.time_step_size_in_minutes

        time_grace_period_in_minutes = self.time_grace_period_in_minutes

        assertions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.assertions, Unset):
            assertions = []
            for assertions_item_data in self.assertions:
                assertions_item = assertions_item_data.to_dict()
                assertions.append(assertions_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if tariff_id is not UNSET:
            field_dict["tariffId"] = tariff_id
        if tariff_name is not UNSET:
            field_dict["tariffName"] = tariff_name
        if start_tariff is not UNSET:
            field_dict["startTariff"] = start_tariff
        if tariff_price is not UNSET:
            field_dict["tariffPrice"] = tariff_price
        if parking_tariff is not UNSET:
            field_dict["parkingTariff"] = parking_tariff
        if parking_step_size_in_minutes is not UNSET:
            field_dict["parkingStepSizeInMinutes"] = parking_step_size_in_minutes
        if parking_grace_period_in_minutes is not UNSET:
            field_dict["parkingGracePeriodInMinutes"] = parking_grace_period_in_minutes
        if time_tariff is not UNSET:
            field_dict["timeTariff"] = time_tariff
        if time_step_size_in_minutes is not UNSET:
            field_dict["timeStepSizeInMinutes"] = time_step_size_in_minutes
        if time_grace_period_in_minutes is not UNSET:
            field_dict["timeGracePeriodInMinutes"] = time_grace_period_in_minutes
        if assertions is not UNSET:
            field_dict["assertions"] = assertions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.tariff_assertion_dto import TariffAssertionDto

        d = src_dict.copy()
        tariff_id = d.pop("tariffId", UNSET)

        tariff_name = d.pop("tariffName", UNSET)

        start_tariff = d.pop("startTariff", UNSET)

        tariff_price = d.pop("tariffPrice", UNSET)

        parking_tariff = d.pop("parkingTariff", UNSET)

        parking_step_size_in_minutes = d.pop("parkingStepSizeInMinutes", UNSET)

        parking_grace_period_in_minutes = d.pop("parkingGracePeriodInMinutes", UNSET)

        time_tariff = d.pop("timeTariff", UNSET)

        time_step_size_in_minutes = d.pop("timeStepSizeInMinutes", UNSET)

        time_grace_period_in_minutes = d.pop("timeGracePeriodInMinutes", UNSET)

        assertions = []
        _assertions = d.pop("assertions", UNSET)
        for assertions_item_data in _assertions or []:
            assertions_item = TariffAssertionDto.from_dict(assertions_item_data)

            assertions.append(assertions_item)

        tariff_info_dto = cls(
            tariff_id=tariff_id,
            tariff_name=tariff_name,
            start_tariff=start_tariff,
            tariff_price=tariff_price,
            parking_tariff=parking_tariff,
            parking_step_size_in_minutes=parking_step_size_in_minutes,
            parking_grace_period_in_minutes=parking_grace_period_in_minutes,
            time_tariff=time_tariff,
            time_step_size_in_minutes=time_step_size_in_minutes,
            time_grace_period_in_minutes=time_grace_period_in_minutes,
            assertions=assertions,
        )

        tariff_info_dto.additional_properties = d
        return tariff_info_dto

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
