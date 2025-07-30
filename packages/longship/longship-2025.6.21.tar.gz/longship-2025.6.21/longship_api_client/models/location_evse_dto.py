from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from ..models.location_evse_dto_parking_restrictions_item import (
    LocationEVSEDtoParkingRestrictionsItem,
)
from ..models.location_evse_dto_capabilities_item import LocationEVSEDtoCapabilitiesItem
import datetime
from typing import Union
from ..models.location_evse_dto_status import LocationEVSEDtoStatus

if TYPE_CHECKING:
    from ..models.display_text_dto import DisplayTextDto
    from ..models.image_dto import ImageDto
    from ..models.geo_location_dto import GeoLocationDto
    from ..models.status_schedule_dto import StatusScheduleDto
    from ..models.connector_dto import ConnectorDto


T = TypeVar("T", bound="LocationEVSEDto")


@_attrs_define
class LocationEVSEDto:
    """
    Attributes:
        id (Union[Unset, str]):
        chargepointid (Union[Unset, str]):
        latitude (Union[Unset, float]):
        longitude (Union[Unset, float]):
        uid (Union[Unset, str]):
        evse_id (Union[Unset, str]):
        status (Union[Unset, LocationEVSEDtoStatus]):  Default: LocationEVSEDtoStatus.AVAILABLE.
        status_schedule (Union[Unset, List['StatusScheduleDto']]):
        capabilities (Union[Unset, List[LocationEVSEDtoCapabilitiesItem]]):
        connectors (Union[Unset, List['ConnectorDto']]):
        floor_level (Union[Unset, str]):
        coordinates (Union[Unset, GeoLocationDto]):
        physical_reference (Union[Unset, str]):
        directions (Union[Unset, List['DisplayTextDto']]):
        parking_restrictions (Union[Unset, List[LocationEVSEDtoParkingRestrictionsItem]]):
        images (Union[Unset, List['ImageDto']]):
        last_updated (Union[Unset, datetime.datetime]):
    """

    id: Union[Unset, str] = UNSET
    chargepointid: Union[Unset, str] = UNSET
    latitude: Union[Unset, float] = UNSET
    longitude: Union[Unset, float] = UNSET
    uid: Union[Unset, str] = UNSET
    evse_id: Union[Unset, str] = UNSET
    status: Union[Unset, LocationEVSEDtoStatus] = LocationEVSEDtoStatus.AVAILABLE
    status_schedule: Union[Unset, List["StatusScheduleDto"]] = UNSET
    capabilities: Union[Unset, List[LocationEVSEDtoCapabilitiesItem]] = UNSET
    connectors: Union[Unset, List["ConnectorDto"]] = UNSET
    floor_level: Union[Unset, str] = UNSET
    coordinates: Union[Unset, "GeoLocationDto"] = UNSET
    physical_reference: Union[Unset, str] = UNSET
    directions: Union[Unset, List["DisplayTextDto"]] = UNSET
    parking_restrictions: Union[Unset, List[LocationEVSEDtoParkingRestrictionsItem]] = (
        UNSET
    )
    images: Union[Unset, List["ImageDto"]] = UNSET
    last_updated: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        chargepointid = self.chargepointid

        latitude = self.latitude

        longitude = self.longitude

        uid = self.uid

        evse_id = self.evse_id

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        status_schedule: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.status_schedule, Unset):
            status_schedule = []
            for status_schedule_item_data in self.status_schedule:
                status_schedule_item = status_schedule_item_data.to_dict()
                status_schedule.append(status_schedule_item)

        capabilities: Union[Unset, List[str]] = UNSET
        if not isinstance(self.capabilities, Unset):
            capabilities = []
            for capabilities_item_data in self.capabilities:
                capabilities_item = capabilities_item_data.value
                capabilities.append(capabilities_item)

        connectors: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.connectors, Unset):
            connectors = []
            for connectors_item_data in self.connectors:
                connectors_item = connectors_item_data.to_dict()
                connectors.append(connectors_item)

        floor_level = self.floor_level

        coordinates: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.coordinates, Unset):
            coordinates = self.coordinates.to_dict()

        physical_reference = self.physical_reference

        directions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.directions, Unset):
            directions = []
            for directions_item_data in self.directions:
                directions_item = directions_item_data.to_dict()
                directions.append(directions_item)

        parking_restrictions: Union[Unset, List[str]] = UNSET
        if not isinstance(self.parking_restrictions, Unset):
            parking_restrictions = []
            for parking_restrictions_item_data in self.parking_restrictions:
                parking_restrictions_item = parking_restrictions_item_data.value
                parking_restrictions.append(parking_restrictions_item)

        images: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.images, Unset):
            images = []
            for images_item_data in self.images:
                images_item = images_item_data.to_dict()
                images.append(images_item)

        last_updated: Union[Unset, str] = UNSET
        if not isinstance(self.last_updated, Unset):
            last_updated = self.last_updated.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if chargepointid is not UNSET:
            field_dict["chargepointid"] = chargepointid
        if latitude is not UNSET:
            field_dict["latitude"] = latitude
        if longitude is not UNSET:
            field_dict["longitude"] = longitude
        if uid is not UNSET:
            field_dict["uid"] = uid
        if evse_id is not UNSET:
            field_dict["evse_id"] = evse_id
        if status is not UNSET:
            field_dict["status"] = status
        if status_schedule is not UNSET:
            field_dict["status_schedule"] = status_schedule
        if capabilities is not UNSET:
            field_dict["capabilities"] = capabilities
        if connectors is not UNSET:
            field_dict["connectors"] = connectors
        if floor_level is not UNSET:
            field_dict["floor_level"] = floor_level
        if coordinates is not UNSET:
            field_dict["coordinates"] = coordinates
        if physical_reference is not UNSET:
            field_dict["physical_reference"] = physical_reference
        if directions is not UNSET:
            field_dict["directions"] = directions
        if parking_restrictions is not UNSET:
            field_dict["parking_restrictions"] = parking_restrictions
        if images is not UNSET:
            field_dict["images"] = images
        if last_updated is not UNSET:
            field_dict["last_updated"] = last_updated

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.display_text_dto import DisplayTextDto
        from ..models.image_dto import ImageDto
        from ..models.geo_location_dto import GeoLocationDto
        from ..models.status_schedule_dto import StatusScheduleDto
        from ..models.connector_dto import ConnectorDto

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        chargepointid = d.pop("chargepointid", UNSET)

        latitude = d.pop("latitude", UNSET)

        longitude = d.pop("longitude", UNSET)

        uid = d.pop("uid", UNSET)

        evse_id = d.pop("evse_id", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, LocationEVSEDtoStatus]
        if isinstance(_status, Unset) or _status is None:
            status = UNSET
        else:
            status = LocationEVSEDtoStatus(_status)

        status_schedule = []
        _status_schedule = d.pop("status_schedule", UNSET)
        for status_schedule_item_data in _status_schedule or []:
            status_schedule_item = StatusScheduleDto.from_dict(
                status_schedule_item_data
            )

            status_schedule.append(status_schedule_item)

        capabilities = []
        _capabilities = d.pop("capabilities", UNSET)
        for capabilities_item_data in _capabilities or []:
            capabilities_item = LocationEVSEDtoCapabilitiesItem(capabilities_item_data)

            capabilities.append(capabilities_item)

        connectors = []
        _connectors = d.pop("connectors", UNSET)
        for connectors_item_data in _connectors or []:
            connectors_item = ConnectorDto.from_dict(connectors_item_data)

            connectors.append(connectors_item)

        floor_level = d.pop("floor_level", UNSET)

        _coordinates = d.pop("coordinates", UNSET)
        coordinates: Union[Unset, GeoLocationDto]
        if isinstance(_coordinates, Unset) or _coordinates is None:
            coordinates = UNSET
        else:
            coordinates = GeoLocationDto.from_dict(_coordinates)

        physical_reference = d.pop("physical_reference", UNSET)

        directions = []
        _directions = d.pop("directions", UNSET)
        for directions_item_data in _directions or []:
            directions_item = DisplayTextDto.from_dict(directions_item_data)

            directions.append(directions_item)

        parking_restrictions = []
        _parking_restrictions = d.pop("parking_restrictions", UNSET)
        for parking_restrictions_item_data in _parking_restrictions or []:
            parking_restrictions_item = LocationEVSEDtoParkingRestrictionsItem(
                parking_restrictions_item_data
            )

            parking_restrictions.append(parking_restrictions_item)

        images = []
        _images = d.pop("images", UNSET)
        for images_item_data in _images or []:
            images_item = ImageDto.from_dict(images_item_data)

            images.append(images_item)

        _last_updated = d.pop("last_updated", UNSET)
        last_updated: Union[Unset, datetime.datetime]
        if isinstance(_last_updated, Unset) or _last_updated is None:
            last_updated = UNSET
        else:
            last_updated = isoparse(_last_updated)

        location_evse_dto = cls(
            id=id,
            chargepointid=chargepointid,
            latitude=latitude,
            longitude=longitude,
            uid=uid,
            evse_id=evse_id,
            status=status,
            status_schedule=status_schedule,
            capabilities=capabilities,
            connectors=connectors,
            floor_level=floor_level,
            coordinates=coordinates,
            physical_reference=physical_reference,
            directions=directions,
            parking_restrictions=parking_restrictions,
            images=images,
            last_updated=last_updated,
        )

        location_evse_dto.additional_properties = d
        return location_evse_dto

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
