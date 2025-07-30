from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from ..models.location_dto_facilities_item import LocationDtoFacilitiesItem
import datetime
from ..models.location_dto_parking_type import LocationDtoParkingType
from typing import Union

if TYPE_CHECKING:
    from ..models.display_text_dto import DisplayTextDto
    from ..models.reimburse_info_dto import ReimburseInfoDto
    from ..models.publish_token_type_dto import PublishTokenTypeDto
    from ..models.image_dto import ImageDto
    from ..models.hours_dto import HoursDto
    from ..models.energy_mix_dto import EnergyMixDto
    from ..models.geo_location_dto import GeoLocationDto
    from ..models.business_details_dto import BusinessDetailsDto
    from ..models.location_evse_dto import LocationEVSEDto
    from ..models.additional_geo_location_dto import AdditionalGeoLocationDto


T = TypeVar("T", bound="LocationDto")


@_attrs_define
class LocationDto:
    """
    Attributes:
        id (str):
        country_code (str):
        party_id (str):
        publish (bool):
        street (str):
        city (str):
        country (str):
        coordinates (GeoLocationDto):
        time_zone (str):
        last_updated (datetime.datetime):
        publish_allowed_to (Union[Unset, List['PublishTokenTypeDto']]):
        name (Union[Unset, str]):
        house_number (Union[Unset, str]):
        postal_code (Union[Unset, str]):
        state (Union[Unset, str]):
        hotline_phonenumber (Union[Unset, str]):
        related_locations (Union[Unset, List['AdditionalGeoLocationDto']]):
        parking_type (Union[Unset, LocationDtoParkingType]):  Default: LocationDtoParkingType.ALONG_MOTORWAY.
        evses (Union[Unset, List['LocationEVSEDto']]):
        directions (Union[Unset, List['DisplayTextDto']]):
        operator (Union[Unset, BusinessDetailsDto]):
        suboperator (Union[Unset, BusinessDetailsDto]):
        owner (Union[Unset, BusinessDetailsDto]):
        facilities (Union[Unset, List[LocationDtoFacilitiesItem]]):
        opening_times (Union[Unset, HoursDto]):
        charging_when_closed (Union[Unset, bool]):
        images (Union[Unset, List['ImageDto']]):
        energy_mix (Union[Unset, EnergyMixDto]):
        deleted_on (Union[Unset, datetime.datetime]):
        has_reimbursement (Union[Unset, bool]):
        reimburse_info (Union[Unset, ReimburseInfoDto]):
        operator_id (Union[Unset, str]):
        ou (Union[Unset, str]):
        ou_id (Union[Unset, str]):
        ou_name (Union[Unset, str]):
        external_reference_1 (Union[Unset, str]):
        external_reference_2 (Union[Unset, str]):
        external_reference_3 (Union[Unset, str]):
    """

    id: str
    country_code: str
    party_id: str
    publish: bool
    street: str
    city: str
    country: str
    coordinates: "GeoLocationDto"
    time_zone: str
    last_updated: datetime.datetime
    publish_allowed_to: Union[Unset, List["PublishTokenTypeDto"]] = UNSET
    name: Union[Unset, str] = UNSET
    house_number: Union[Unset, str] = UNSET
    postal_code: Union[Unset, str] = UNSET
    state: Union[Unset, str] = UNSET
    hotline_phonenumber: Union[Unset, str] = UNSET
    related_locations: Union[Unset, List["AdditionalGeoLocationDto"]] = UNSET
    parking_type: Union[Unset, LocationDtoParkingType] = (
        LocationDtoParkingType.ALONG_MOTORWAY
    )
    evses: Union[Unset, List["LocationEVSEDto"]] = UNSET
    directions: Union[Unset, List["DisplayTextDto"]] = UNSET
    operator: Union[Unset, "BusinessDetailsDto"] = UNSET
    suboperator: Union[Unset, "BusinessDetailsDto"] = UNSET
    owner: Union[Unset, "BusinessDetailsDto"] = UNSET
    facilities: Union[Unset, List[LocationDtoFacilitiesItem]] = UNSET
    opening_times: Union[Unset, "HoursDto"] = UNSET
    charging_when_closed: Union[Unset, bool] = UNSET
    images: Union[Unset, List["ImageDto"]] = UNSET
    energy_mix: Union[Unset, "EnergyMixDto"] = UNSET
    deleted_on: Union[Unset, datetime.datetime] = UNSET
    has_reimbursement: Union[Unset, bool] = UNSET
    reimburse_info: Union[Unset, "ReimburseInfoDto"] = UNSET
    operator_id: Union[Unset, str] = UNSET
    ou: Union[Unset, str] = UNSET
    ou_id: Union[Unset, str] = UNSET
    ou_name: Union[Unset, str] = UNSET
    external_reference_1: Union[Unset, str] = UNSET
    external_reference_2: Union[Unset, str] = UNSET
    external_reference_3: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        country_code = self.country_code

        party_id = self.party_id

        publish = self.publish

        street = self.street

        city = self.city

        country = self.country

        coordinates = self.coordinates.to_dict()

        time_zone = self.time_zone

        last_updated = self.last_updated.isoformat()

        publish_allowed_to: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.publish_allowed_to, Unset):
            publish_allowed_to = []
            for publish_allowed_to_item_data in self.publish_allowed_to:
                publish_allowed_to_item = publish_allowed_to_item_data.to_dict()
                publish_allowed_to.append(publish_allowed_to_item)

        name = self.name

        house_number = self.house_number

        postal_code = self.postal_code

        state = self.state

        hotline_phonenumber = self.hotline_phonenumber

        related_locations: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.related_locations, Unset):
            related_locations = []
            for related_locations_item_data in self.related_locations:
                related_locations_item = related_locations_item_data.to_dict()
                related_locations.append(related_locations_item)

        parking_type: Union[Unset, str] = UNSET
        if not isinstance(self.parking_type, Unset):
            parking_type = self.parking_type.value

        evses: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.evses, Unset):
            evses = []
            for evses_item_data in self.evses:
                evses_item = evses_item_data.to_dict()
                evses.append(evses_item)

        directions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.directions, Unset):
            directions = []
            for directions_item_data in self.directions:
                directions_item = directions_item_data.to_dict()
                directions.append(directions_item)

        operator: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.operator, Unset):
            operator = self.operator.to_dict()

        suboperator: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.suboperator, Unset):
            suboperator = self.suboperator.to_dict()

        owner: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.owner, Unset):
            owner = self.owner.to_dict()

        facilities: Union[Unset, List[str]] = UNSET
        if not isinstance(self.facilities, Unset):
            facilities = []
            for facilities_item_data in self.facilities:
                facilities_item = facilities_item_data.value
                facilities.append(facilities_item)

        opening_times: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.opening_times, Unset):
            opening_times = self.opening_times.to_dict()

        charging_when_closed = self.charging_when_closed

        images: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.images, Unset):
            images = []
            for images_item_data in self.images:
                images_item = images_item_data.to_dict()
                images.append(images_item)

        energy_mix: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.energy_mix, Unset):
            energy_mix = self.energy_mix.to_dict()

        deleted_on: Union[Unset, str] = UNSET
        if not isinstance(self.deleted_on, Unset):
            deleted_on = self.deleted_on.isoformat()

        has_reimbursement = self.has_reimbursement

        reimburse_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.reimburse_info, Unset):
            reimburse_info = self.reimburse_info.to_dict()

        operator_id = self.operator_id

        ou = self.ou

        ou_id = self.ou_id

        ou_name = self.ou_name

        external_reference_1 = self.external_reference_1

        external_reference_2 = self.external_reference_2

        external_reference_3 = self.external_reference_3

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "country_code": country_code,
                "party_id": party_id,
                "publish": publish,
                "street": street,
                "city": city,
                "country": country,
                "coordinates": coordinates,
                "time_zone": time_zone,
                "last_updated": last_updated,
            }
        )
        if publish_allowed_to is not UNSET:
            field_dict["publish_allowed_to"] = publish_allowed_to
        if name is not UNSET:
            field_dict["name"] = name
        if house_number is not UNSET:
            field_dict["houseNumber"] = house_number
        if postal_code is not UNSET:
            field_dict["postal_code"] = postal_code
        if state is not UNSET:
            field_dict["state"] = state
        if hotline_phonenumber is not UNSET:
            field_dict["hotline_phonenumber"] = hotline_phonenumber
        if related_locations is not UNSET:
            field_dict["related_locations"] = related_locations
        if parking_type is not UNSET:
            field_dict["parking_type"] = parking_type
        if evses is not UNSET:
            field_dict["evses"] = evses
        if directions is not UNSET:
            field_dict["directions"] = directions
        if operator is not UNSET:
            field_dict["operator"] = operator
        if suboperator is not UNSET:
            field_dict["suboperator"] = suboperator
        if owner is not UNSET:
            field_dict["owner"] = owner
        if facilities is not UNSET:
            field_dict["facilities"] = facilities
        if opening_times is not UNSET:
            field_dict["opening_times"] = opening_times
        if charging_when_closed is not UNSET:
            field_dict["charging_when_closed"] = charging_when_closed
        if images is not UNSET:
            field_dict["images"] = images
        if energy_mix is not UNSET:
            field_dict["energy_mix"] = energy_mix
        if deleted_on is not UNSET:
            field_dict["deletedOn"] = deleted_on
        if has_reimbursement is not UNSET:
            field_dict["hasReimbursement"] = has_reimbursement
        if reimburse_info is not UNSET:
            field_dict["reimburseInfo"] = reimburse_info
        if operator_id is not UNSET:
            field_dict["operatorId"] = operator_id
        if ou is not UNSET:
            field_dict["ou"] = ou
        if ou_id is not UNSET:
            field_dict["ouId"] = ou_id
        if ou_name is not UNSET:
            field_dict["ouName"] = ou_name
        if external_reference_1 is not UNSET:
            field_dict["externalReference1"] = external_reference_1
        if external_reference_2 is not UNSET:
            field_dict["externalReference2"] = external_reference_2
        if external_reference_3 is not UNSET:
            field_dict["externalReference3"] = external_reference_3

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.display_text_dto import DisplayTextDto
        from ..models.reimburse_info_dto import ReimburseInfoDto
        from ..models.publish_token_type_dto import PublishTokenTypeDto
        from ..models.image_dto import ImageDto
        from ..models.hours_dto import HoursDto
        from ..models.energy_mix_dto import EnergyMixDto
        from ..models.geo_location_dto import GeoLocationDto
        from ..models.business_details_dto import BusinessDetailsDto
        from ..models.location_evse_dto import LocationEVSEDto
        from ..models.additional_geo_location_dto import AdditionalGeoLocationDto

        d = src_dict.copy()
        id = d.pop("id")

        country_code = d.pop("country_code")

        party_id = d.pop("party_id")

        publish = d.pop("publish")

        street = d.pop("street")

        city = d.pop("city")

        country = d.pop("country")

        coordinates = GeoLocationDto.from_dict(d.pop("coordinates"))

        time_zone = d.pop("time_zone")

        last_updated = isoparse(d.pop("last_updated"))

        publish_allowed_to = []
        _publish_allowed_to = d.pop("publish_allowed_to", UNSET)
        for publish_allowed_to_item_data in _publish_allowed_to or []:
            publish_allowed_to_item = PublishTokenTypeDto.from_dict(
                publish_allowed_to_item_data
            )

            publish_allowed_to.append(publish_allowed_to_item)

        name = d.pop("name", UNSET)

        house_number = d.pop("houseNumber", UNSET)

        postal_code = d.pop("postal_code", UNSET)

        state = d.pop("state", UNSET)

        hotline_phonenumber = d.pop("hotline_phonenumber", UNSET)

        related_locations = []
        _related_locations = d.pop("related_locations", UNSET)
        for related_locations_item_data in _related_locations or []:
            related_locations_item = AdditionalGeoLocationDto.from_dict(
                related_locations_item_data
            )

            related_locations.append(related_locations_item)

        _parking_type = d.pop("parking_type", UNSET)
        parking_type: Union[Unset, LocationDtoParkingType]
        if isinstance(_parking_type, Unset) or _parking_type is None:
            parking_type = UNSET
        else:
            parking_type = LocationDtoParkingType(_parking_type)

        evses = []
        _evses = d.pop("evses", UNSET)
        for evses_item_data in _evses or []:
            evses_item = LocationEVSEDto.from_dict(evses_item_data)

            evses.append(evses_item)

        directions = []
        _directions = d.pop("directions", UNSET)
        for directions_item_data in _directions or []:
            directions_item = DisplayTextDto.from_dict(directions_item_data)

            directions.append(directions_item)

        _operator = d.pop("operator", UNSET)
        operator: Union[Unset, BusinessDetailsDto]
        if isinstance(_operator, Unset) or _operator is None:
            operator = UNSET
        else:
            operator = BusinessDetailsDto.from_dict(_operator)

        _suboperator = d.pop("suboperator", UNSET)
        suboperator: Union[Unset, BusinessDetailsDto]
        if isinstance(_suboperator, Unset) or _suboperator is None:
            suboperator = UNSET
        else:
            suboperator = BusinessDetailsDto.from_dict(_suboperator)

        _owner = d.pop("owner", UNSET)
        owner: Union[Unset, BusinessDetailsDto]
        if isinstance(_owner, Unset) or _owner is None:
            owner = UNSET
        else:
            owner = BusinessDetailsDto.from_dict(_owner)

        facilities = []
        _facilities = d.pop("facilities", UNSET)
        for facilities_item_data in _facilities or []:
            facilities_item = LocationDtoFacilitiesItem(facilities_item_data)

            facilities.append(facilities_item)

        _opening_times = d.pop("opening_times", UNSET)
        opening_times: Union[Unset, HoursDto]
        if isinstance(_opening_times, Unset) or _opening_times is None:
            opening_times = UNSET
        else:
            opening_times = HoursDto.from_dict(_opening_times)

        charging_when_closed = d.pop("charging_when_closed", UNSET)

        images = []
        _images = d.pop("images", UNSET)
        for images_item_data in _images or []:
            images_item = ImageDto.from_dict(images_item_data)

            images.append(images_item)

        _energy_mix = d.pop("energy_mix", UNSET)
        energy_mix: Union[Unset, EnergyMixDto]
        if isinstance(_energy_mix, Unset) or _energy_mix is None:
            energy_mix = UNSET
        else:
            energy_mix = EnergyMixDto.from_dict(_energy_mix)

        _deleted_on = d.pop("deletedOn", UNSET)
        deleted_on: Union[Unset, datetime.datetime]
        if isinstance(_deleted_on, Unset) or _deleted_on is None:
            deleted_on = UNSET
        else:
            deleted_on = isoparse(_deleted_on)

        has_reimbursement = d.pop("hasReimbursement", UNSET)

        _reimburse_info = d.pop("reimburseInfo", UNSET)
        reimburse_info: Union[Unset, ReimburseInfoDto]
        if isinstance(_reimburse_info, Unset) or _reimburse_info is None:
            reimburse_info = UNSET
        else:
            reimburse_info = ReimburseInfoDto.from_dict(_reimburse_info)

        operator_id = d.pop("operatorId", UNSET)

        ou = d.pop("ou", UNSET)

        ou_id = d.pop("ouId", UNSET)

        ou_name = d.pop("ouName", UNSET)

        external_reference_1 = d.pop("externalReference1", UNSET)

        external_reference_2 = d.pop("externalReference2", UNSET)

        external_reference_3 = d.pop("externalReference3", UNSET)

        location_dto = cls(
            id=id,
            country_code=country_code,
            party_id=party_id,
            publish=publish,
            street=street,
            city=city,
            country=country,
            coordinates=coordinates,
            time_zone=time_zone,
            last_updated=last_updated,
            publish_allowed_to=publish_allowed_to,
            name=name,
            house_number=house_number,
            postal_code=postal_code,
            state=state,
            hotline_phonenumber=hotline_phonenumber,
            related_locations=related_locations,
            parking_type=parking_type,
            evses=evses,
            directions=directions,
            operator=operator,
            suboperator=suboperator,
            owner=owner,
            facilities=facilities,
            opening_times=opening_times,
            charging_when_closed=charging_when_closed,
            images=images,
            energy_mix=energy_mix,
            deleted_on=deleted_on,
            has_reimbursement=has_reimbursement,
            reimburse_info=reimburse_info,
            operator_id=operator_id,
            ou=ou,
            ou_id=ou_id,
            ou_name=ou_name,
            external_reference_1=external_reference_1,
            external_reference_2=external_reference_2,
            external_reference_3=external_reference_3,
        )

        location_dto.additional_properties = d
        return location_dto

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
