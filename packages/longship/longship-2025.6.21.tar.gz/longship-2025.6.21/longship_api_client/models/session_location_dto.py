from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.session_location_dto_power_type import SessionLocationDtoPowerType
from typing import Union

if TYPE_CHECKING:
    from ..models.session_geo_location_dto import SessionGeoLocationDto


T = TypeVar("T", bound="SessionLocationDto")


@_attrs_define
class SessionLocationDto:
    """
    Attributes:
        id (Union[Unset, str]):
        evse_id (Union[Unset, str]):
        power_type (Union[Unset, SessionLocationDtoPowerType]):  Default: SessionLocationDtoPowerType.AC_1_PHASE.
        country_code (Union[Unset, str]):
        party_id (Union[Unset, str]):
        name (Union[Unset, str]):
        house_number (Union[Unset, str]):
        street (Union[Unset, str]):
        city (Union[Unset, str]):
        postal_code (Union[Unset, str]):
        state (Union[Unset, str]):
        country (Union[Unset, str]):
        hotline_phonenumber (Union[Unset, str]):
        coordinates (Union[Unset, SessionGeoLocationDto]):
        time_zone (Union[Unset, str]):
        has_reimbursement (Union[Unset, bool]):
    """

    id: Union[Unset, str] = UNSET
    evse_id: Union[Unset, str] = UNSET
    power_type: Union[Unset, SessionLocationDtoPowerType] = (
        SessionLocationDtoPowerType.AC_1_PHASE
    )
    country_code: Union[Unset, str] = UNSET
    party_id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    house_number: Union[Unset, str] = UNSET
    street: Union[Unset, str] = UNSET
    city: Union[Unset, str] = UNSET
    postal_code: Union[Unset, str] = UNSET
    state: Union[Unset, str] = UNSET
    country: Union[Unset, str] = UNSET
    hotline_phonenumber: Union[Unset, str] = UNSET
    coordinates: Union[Unset, "SessionGeoLocationDto"] = UNSET
    time_zone: Union[Unset, str] = UNSET
    has_reimbursement: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        evse_id = self.evse_id

        power_type: Union[Unset, str] = UNSET
        if not isinstance(self.power_type, Unset):
            power_type = self.power_type.value

        country_code = self.country_code

        party_id = self.party_id

        name = self.name

        house_number = self.house_number

        street = self.street

        city = self.city

        postal_code = self.postal_code

        state = self.state

        country = self.country

        hotline_phonenumber = self.hotline_phonenumber

        coordinates: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.coordinates, Unset):
            coordinates = self.coordinates.to_dict()

        time_zone = self.time_zone

        has_reimbursement = self.has_reimbursement

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if evse_id is not UNSET:
            field_dict["evseId"] = evse_id
        if power_type is not UNSET:
            field_dict["powerType"] = power_type
        if country_code is not UNSET:
            field_dict["country_code"] = country_code
        if party_id is not UNSET:
            field_dict["party_id"] = party_id
        if name is not UNSET:
            field_dict["name"] = name
        if house_number is not UNSET:
            field_dict["houseNumber"] = house_number
        if street is not UNSET:
            field_dict["street"] = street
        if city is not UNSET:
            field_dict["city"] = city
        if postal_code is not UNSET:
            field_dict["postal_code"] = postal_code
        if state is not UNSET:
            field_dict["state"] = state
        if country is not UNSET:
            field_dict["country"] = country
        if hotline_phonenumber is not UNSET:
            field_dict["hotline_phonenumber"] = hotline_phonenumber
        if coordinates is not UNSET:
            field_dict["coordinates"] = coordinates
        if time_zone is not UNSET:
            field_dict["time_zone"] = time_zone
        if has_reimbursement is not UNSET:
            field_dict["hasReimbursement"] = has_reimbursement

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.session_geo_location_dto import SessionGeoLocationDto

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        evse_id = d.pop("evseId", UNSET)

        _power_type = d.pop("powerType", UNSET)
        power_type: Union[Unset, SessionLocationDtoPowerType]
        if isinstance(_power_type, Unset) or _power_type is None:
            power_type = UNSET
        else:
            power_type = SessionLocationDtoPowerType(_power_type)

        country_code = d.pop("country_code", UNSET)

        party_id = d.pop("party_id", UNSET)

        name = d.pop("name", UNSET)

        house_number = d.pop("houseNumber", UNSET)

        street = d.pop("street", UNSET)

        city = d.pop("city", UNSET)

        postal_code = d.pop("postal_code", UNSET)

        state = d.pop("state", UNSET)

        country = d.pop("country", UNSET)

        hotline_phonenumber = d.pop("hotline_phonenumber", UNSET)

        _coordinates = d.pop("coordinates", UNSET)
        coordinates: Union[Unset, SessionGeoLocationDto]
        if isinstance(_coordinates, Unset) or _coordinates is None:
            coordinates = UNSET
        else:
            coordinates = SessionGeoLocationDto.from_dict(_coordinates)

        time_zone = d.pop("time_zone", UNSET)

        has_reimbursement = d.pop("hasReimbursement", UNSET)

        session_location_dto = cls(
            id=id,
            evse_id=evse_id,
            power_type=power_type,
            country_code=country_code,
            party_id=party_id,
            name=name,
            house_number=house_number,
            street=street,
            city=city,
            postal_code=postal_code,
            state=state,
            country=country,
            hotline_phonenumber=hotline_phonenumber,
            coordinates=coordinates,
            time_zone=time_zone,
            has_reimbursement=has_reimbursement,
        )

        session_location_dto.additional_properties = d
        return session_location_dto

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
