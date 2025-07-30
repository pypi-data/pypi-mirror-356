from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.energy_source_dto import EnergySourceDto
    from ..models.environmental_impact_dto import EnvironmentalImpactDto


T = TypeVar("T", bound="EnergyMixDto")


@_attrs_define
class EnergyMixDto:
    """
    Attributes:
        is_green_energy (Union[Unset, bool]):
        energy_sources (Union[Unset, List['EnergySourceDto']]):
        environ_impact (Union[Unset, List['EnvironmentalImpactDto']]):
    """

    is_green_energy: Union[Unset, bool] = UNSET
    energy_sources: Union[Unset, List["EnergySourceDto"]] = UNSET
    environ_impact: Union[Unset, List["EnvironmentalImpactDto"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        is_green_energy = self.is_green_energy

        energy_sources: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.energy_sources, Unset):
            energy_sources = []
            for energy_sources_item_data in self.energy_sources:
                energy_sources_item = energy_sources_item_data.to_dict()
                energy_sources.append(energy_sources_item)

        environ_impact: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.environ_impact, Unset):
            environ_impact = []
            for environ_impact_item_data in self.environ_impact:
                environ_impact_item = environ_impact_item_data.to_dict()
                environ_impact.append(environ_impact_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if is_green_energy is not UNSET:
            field_dict["is_green_energy"] = is_green_energy
        if energy_sources is not UNSET:
            field_dict["energy_sources"] = energy_sources
        if environ_impact is not UNSET:
            field_dict["environ_impact"] = environ_impact

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.energy_source_dto import EnergySourceDto
        from ..models.environmental_impact_dto import EnvironmentalImpactDto

        d = src_dict.copy()
        is_green_energy = d.pop("is_green_energy", UNSET)

        energy_sources = []
        _energy_sources = d.pop("energy_sources", UNSET)
        for energy_sources_item_data in _energy_sources or []:
            energy_sources_item = EnergySourceDto.from_dict(energy_sources_item_data)

            energy_sources.append(energy_sources_item)

        environ_impact = []
        _environ_impact = d.pop("environ_impact", UNSET)
        for environ_impact_item_data in _environ_impact or []:
            environ_impact_item = EnvironmentalImpactDto.from_dict(
                environ_impact_item_data
            )

            environ_impact.append(environ_impact_item)

        energy_mix_dto = cls(
            is_green_energy=is_green_energy,
            energy_sources=energy_sources,
            environ_impact=environ_impact,
        )

        energy_mix_dto.additional_properties = d
        return energy_mix_dto

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
