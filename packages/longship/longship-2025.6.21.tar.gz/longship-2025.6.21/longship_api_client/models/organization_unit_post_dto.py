from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.organization_unit_financial_details_dto import (
        OrganizationUnitFinancialDetailsDto,
    )


T = TypeVar("T", bound="OrganizationUnitPostDto")


@_attrs_define
class OrganizationUnitPostDto:
    """
    Attributes:
        parent_id (str): The id of parent ou.
        name (Union[Unset, str]): The name of the ou.
        external_reference (Union[Unset, str]): This property can be used to link this OU to another system.
        grid_owner_reference (Union[Unset, str]): This property can be used to link this OU to a grid owner.
        tenant_reference (Union[Unset, str]): This property can be used to link this OU to a tenant.
        customer_reference (Union[Unset, str]): This property can be used to link this OU to a customer.
        address (Union[Unset, str]):
        state (Union[Unset, str]):
        country (Union[Unset, str]):
        city (Union[Unset, str]):
        house_number (Union[Unset, str]):
        postal_code (Union[Unset, str]):
        hotline_phone_number (Union[Unset, str]):
        company_email (Union[Unset, str]):
        primary_contactperson (Union[Unset, str]):
        primary_contactperson_email (Union[Unset, str]):
        msp_ou_id (Union[Unset, str]): The ou id used for the "Msp Integration" feature.
        msp_ou_name (Union[Unset, str]): The ou name used for the "Msp Integration" feature.
        msp_ou_code (Union[Unset, str]): The ou code used for the "Msp Integration" feature.
        msp_external_id (Union[Unset, str]): The externalId from the "Msp Integration" feature.
        financial_details (Union[Unset, OrganizationUnitFinancialDetailsDto]):
    """

    parent_id: str
    name: Union[Unset, str] = UNSET
    external_reference: Union[Unset, str] = UNSET
    grid_owner_reference: Union[Unset, str] = UNSET
    tenant_reference: Union[Unset, str] = UNSET
    customer_reference: Union[Unset, str] = UNSET
    address: Union[Unset, str] = UNSET
    state: Union[Unset, str] = UNSET
    country: Union[Unset, str] = UNSET
    city: Union[Unset, str] = UNSET
    house_number: Union[Unset, str] = UNSET
    postal_code: Union[Unset, str] = UNSET
    hotline_phone_number: Union[Unset, str] = UNSET
    company_email: Union[Unset, str] = UNSET
    primary_contactperson: Union[Unset, str] = UNSET
    primary_contactperson_email: Union[Unset, str] = UNSET
    msp_ou_id: Union[Unset, str] = UNSET
    msp_ou_name: Union[Unset, str] = UNSET
    msp_ou_code: Union[Unset, str] = UNSET
    msp_external_id: Union[Unset, str] = UNSET
    financial_details: Union[Unset, "OrganizationUnitFinancialDetailsDto"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        parent_id = self.parent_id

        name = self.name

        external_reference = self.external_reference

        grid_owner_reference = self.grid_owner_reference

        tenant_reference = self.tenant_reference

        customer_reference = self.customer_reference

        address = self.address

        state = self.state

        country = self.country

        city = self.city

        house_number = self.house_number

        postal_code = self.postal_code

        hotline_phone_number = self.hotline_phone_number

        company_email = self.company_email

        primary_contactperson = self.primary_contactperson

        primary_contactperson_email = self.primary_contactperson_email

        msp_ou_id = self.msp_ou_id

        msp_ou_name = self.msp_ou_name

        msp_ou_code = self.msp_ou_code

        msp_external_id = self.msp_external_id

        financial_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.financial_details, Unset):
            financial_details = self.financial_details.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "parentId": parent_id,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if external_reference is not UNSET:
            field_dict["externalReference"] = external_reference
        if grid_owner_reference is not UNSET:
            field_dict["gridOwnerReference"] = grid_owner_reference
        if tenant_reference is not UNSET:
            field_dict["tenantReference"] = tenant_reference
        if customer_reference is not UNSET:
            field_dict["customerReference"] = customer_reference
        if address is not UNSET:
            field_dict["address"] = address
        if state is not UNSET:
            field_dict["state"] = state
        if country is not UNSET:
            field_dict["country"] = country
        if city is not UNSET:
            field_dict["city"] = city
        if house_number is not UNSET:
            field_dict["houseNumber"] = house_number
        if postal_code is not UNSET:
            field_dict["postalCode"] = postal_code
        if hotline_phone_number is not UNSET:
            field_dict["hotlinePhoneNumber"] = hotline_phone_number
        if company_email is not UNSET:
            field_dict["companyEmail"] = company_email
        if primary_contactperson is not UNSET:
            field_dict["primaryContactperson"] = primary_contactperson
        if primary_contactperson_email is not UNSET:
            field_dict["primaryContactpersonEmail"] = primary_contactperson_email
        if msp_ou_id is not UNSET:
            field_dict["mspOuId"] = msp_ou_id
        if msp_ou_name is not UNSET:
            field_dict["mspOuName"] = msp_ou_name
        if msp_ou_code is not UNSET:
            field_dict["mspOuCode"] = msp_ou_code
        if msp_external_id is not UNSET:
            field_dict["mspExternalId"] = msp_external_id
        if financial_details is not UNSET:
            field_dict["financialDetails"] = financial_details

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.organization_unit_financial_details_dto import (
            OrganizationUnitFinancialDetailsDto,
        )

        d = src_dict.copy()
        parent_id = d.pop("parentId")

        name = d.pop("name", UNSET)

        external_reference = d.pop("externalReference", UNSET)

        grid_owner_reference = d.pop("gridOwnerReference", UNSET)

        tenant_reference = d.pop("tenantReference", UNSET)

        customer_reference = d.pop("customerReference", UNSET)

        address = d.pop("address", UNSET)

        state = d.pop("state", UNSET)

        country = d.pop("country", UNSET)

        city = d.pop("city", UNSET)

        house_number = d.pop("houseNumber", UNSET)

        postal_code = d.pop("postalCode", UNSET)

        hotline_phone_number = d.pop("hotlinePhoneNumber", UNSET)

        company_email = d.pop("companyEmail", UNSET)

        primary_contactperson = d.pop("primaryContactperson", UNSET)

        primary_contactperson_email = d.pop("primaryContactpersonEmail", UNSET)

        msp_ou_id = d.pop("mspOuId", UNSET)

        msp_ou_name = d.pop("mspOuName", UNSET)

        msp_ou_code = d.pop("mspOuCode", UNSET)

        msp_external_id = d.pop("mspExternalId", UNSET)

        _financial_details = d.pop("financialDetails", UNSET)
        financial_details: Union[Unset, OrganizationUnitFinancialDetailsDto]
        if isinstance(_financial_details, Unset) or _financial_details is None:
            financial_details = UNSET
        else:
            financial_details = OrganizationUnitFinancialDetailsDto.from_dict(
                _financial_details
            )

        organization_unit_post_dto = cls(
            parent_id=parent_id,
            name=name,
            external_reference=external_reference,
            grid_owner_reference=grid_owner_reference,
            tenant_reference=tenant_reference,
            customer_reference=customer_reference,
            address=address,
            state=state,
            country=country,
            city=city,
            house_number=house_number,
            postal_code=postal_code,
            hotline_phone_number=hotline_phone_number,
            company_email=company_email,
            primary_contactperson=primary_contactperson,
            primary_contactperson_email=primary_contactperson_email,
            msp_ou_id=msp_ou_id,
            msp_ou_name=msp_ou_name,
            msp_ou_code=msp_ou_code,
            msp_external_id=msp_external_id,
            financial_details=financial_details,
        )

        organization_unit_post_dto.additional_properties = d
        return organization_unit_post_dto

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
