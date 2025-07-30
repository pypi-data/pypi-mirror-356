from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.reimburse_info_dto_type import ReimburseInfoDtoType
from typing import Union

if TYPE_CHECKING:
    from ..models.location_tariff_distribution_dto import LocationTariffDistributionDto
    from ..models.reimbursement_tariff_dto import ReimbursementTariffDto
    from ..models.reimbursement_bank_details_dto import ReimbursementBankDetailsDto


T = TypeVar("T", bound="ReimburseInfoDto")


@_attrs_define
class ReimburseInfoDto:
    """
    Attributes:
        type (Union[Unset, ReimburseInfoDtoType]):  Default: ReimburseInfoDtoType.ORGANIZATIONUNIT.
        has_guest_usage (Union[Unset, bool]):
        has_guest_charging_reimbursement_fee (Union[Unset, bool]):
        country_code (Union[Unset, str]):
        party_id (Union[Unset, str]):
        external_organization_unit_id (Union[Unset, str]):
        external_organization_unit_name (Union[Unset, str]):
        external_organization_unit_reference (Union[Unset, str]):
        external_organization_unit_code (Union[Unset, str]):
        charge_card_emaid (Union[Unset, str]):
        charge_card_uid (Union[Unset, str]):
        charge_card_issuer (Union[Unset, str]):
        tariffs (Union[Unset, List['ReimbursementTariffDto']]):
        bank_details (Union[Unset, List['ReimbursementBankDetailsDto']]):
        tariff_distribution_id (Union[Unset, str]):
        tariff_distribution_history (Union[Unset, List['LocationTariffDistributionDto']]):
        ou (Union[Unset, str]):
        ou_id (Union[Unset, str]):
        ou_name (Union[Unset, str]):
    """

    type: Union[Unset, ReimburseInfoDtoType] = ReimburseInfoDtoType.ORGANIZATIONUNIT
    has_guest_usage: Union[Unset, bool] = UNSET
    has_guest_charging_reimbursement_fee: Union[Unset, bool] = UNSET
    country_code: Union[Unset, str] = UNSET
    party_id: Union[Unset, str] = UNSET
    external_organization_unit_id: Union[Unset, str] = UNSET
    external_organization_unit_name: Union[Unset, str] = UNSET
    external_organization_unit_reference: Union[Unset, str] = UNSET
    external_organization_unit_code: Union[Unset, str] = UNSET
    charge_card_emaid: Union[Unset, str] = UNSET
    charge_card_uid: Union[Unset, str] = UNSET
    charge_card_issuer: Union[Unset, str] = UNSET
    tariffs: Union[Unset, List["ReimbursementTariffDto"]] = UNSET
    bank_details: Union[Unset, List["ReimbursementBankDetailsDto"]] = UNSET
    tariff_distribution_id: Union[Unset, str] = UNSET
    tariff_distribution_history: Union[Unset, List["LocationTariffDistributionDto"]] = (
        UNSET
    )
    ou: Union[Unset, str] = UNSET
    ou_id: Union[Unset, str] = UNSET
    ou_name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        has_guest_usage = self.has_guest_usage

        has_guest_charging_reimbursement_fee = self.has_guest_charging_reimbursement_fee

        country_code = self.country_code

        party_id = self.party_id

        external_organization_unit_id = self.external_organization_unit_id

        external_organization_unit_name = self.external_organization_unit_name

        external_organization_unit_reference = self.external_organization_unit_reference

        external_organization_unit_code = self.external_organization_unit_code

        charge_card_emaid = self.charge_card_emaid

        charge_card_uid = self.charge_card_uid

        charge_card_issuer = self.charge_card_issuer

        tariffs: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.tariffs, Unset):
            tariffs = []
            for tariffs_item_data in self.tariffs:
                tariffs_item = tariffs_item_data.to_dict()
                tariffs.append(tariffs_item)

        bank_details: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.bank_details, Unset):
            bank_details = []
            for bank_details_item_data in self.bank_details:
                bank_details_item = bank_details_item_data.to_dict()
                bank_details.append(bank_details_item)

        tariff_distribution_id = self.tariff_distribution_id

        tariff_distribution_history: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.tariff_distribution_history, Unset):
            tariff_distribution_history = []
            for (
                tariff_distribution_history_item_data
            ) in self.tariff_distribution_history:
                tariff_distribution_history_item = (
                    tariff_distribution_history_item_data.to_dict()
                )
                tariff_distribution_history.append(tariff_distribution_history_item)

        ou = self.ou

        ou_id = self.ou_id

        ou_name = self.ou_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if has_guest_usage is not UNSET:
            field_dict["hasGuestUsage"] = has_guest_usage
        if has_guest_charging_reimbursement_fee is not UNSET:
            field_dict["hasGuestChargingReimbursementFee"] = (
                has_guest_charging_reimbursement_fee
            )
        if country_code is not UNSET:
            field_dict["countryCode"] = country_code
        if party_id is not UNSET:
            field_dict["partyId"] = party_id
        if external_organization_unit_id is not UNSET:
            field_dict["externalOrganizationUnitId"] = external_organization_unit_id
        if external_organization_unit_name is not UNSET:
            field_dict["externalOrganizationUnitName"] = external_organization_unit_name
        if external_organization_unit_reference is not UNSET:
            field_dict["externalOrganizationUnitReference"] = (
                external_organization_unit_reference
            )
        if external_organization_unit_code is not UNSET:
            field_dict["externalOrganizationUnitCode"] = external_organization_unit_code
        if charge_card_emaid is not UNSET:
            field_dict["chargeCardEMAID"] = charge_card_emaid
        if charge_card_uid is not UNSET:
            field_dict["chargeCardUID"] = charge_card_uid
        if charge_card_issuer is not UNSET:
            field_dict["chargeCardIssuer"] = charge_card_issuer
        if tariffs is not UNSET:
            field_dict["tariffs"] = tariffs
        if bank_details is not UNSET:
            field_dict["bankDetails"] = bank_details
        if tariff_distribution_id is not UNSET:
            field_dict["tariffDistributionId"] = tariff_distribution_id
        if tariff_distribution_history is not UNSET:
            field_dict["tariffDistributionHistory"] = tariff_distribution_history
        if ou is not UNSET:
            field_dict["ou"] = ou
        if ou_id is not UNSET:
            field_dict["ouId"] = ou_id
        if ou_name is not UNSET:
            field_dict["ouName"] = ou_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.location_tariff_distribution_dto import (
            LocationTariffDistributionDto,
        )
        from ..models.reimbursement_tariff_dto import ReimbursementTariffDto
        from ..models.reimbursement_bank_details_dto import ReimbursementBankDetailsDto

        d = src_dict.copy()
        _type = d.pop("type", UNSET)
        type: Union[Unset, ReimburseInfoDtoType]
        if isinstance(_type, Unset) or _type is None:
            type = UNSET
        else:
            type = ReimburseInfoDtoType(_type)

        has_guest_usage = d.pop("hasGuestUsage", UNSET)

        has_guest_charging_reimbursement_fee = d.pop(
            "hasGuestChargingReimbursementFee", UNSET
        )

        country_code = d.pop("countryCode", UNSET)

        party_id = d.pop("partyId", UNSET)

        external_organization_unit_id = d.pop("externalOrganizationUnitId", UNSET)

        external_organization_unit_name = d.pop("externalOrganizationUnitName", UNSET)

        external_organization_unit_reference = d.pop(
            "externalOrganizationUnitReference", UNSET
        )

        external_organization_unit_code = d.pop("externalOrganizationUnitCode", UNSET)

        charge_card_emaid = d.pop("chargeCardEMAID", UNSET)

        charge_card_uid = d.pop("chargeCardUID", UNSET)

        charge_card_issuer = d.pop("chargeCardIssuer", UNSET)

        tariffs = []
        _tariffs = d.pop("tariffs", UNSET)
        for tariffs_item_data in _tariffs or []:
            tariffs_item = ReimbursementTariffDto.from_dict(tariffs_item_data)

            tariffs.append(tariffs_item)

        bank_details = []
        _bank_details = d.pop("bankDetails", UNSET)
        for bank_details_item_data in _bank_details or []:
            bank_details_item = ReimbursementBankDetailsDto.from_dict(
                bank_details_item_data
            )

            bank_details.append(bank_details_item)

        tariff_distribution_id = d.pop("tariffDistributionId", UNSET)

        tariff_distribution_history = []
        _tariff_distribution_history = d.pop("tariffDistributionHistory", UNSET)
        for tariff_distribution_history_item_data in _tariff_distribution_history or []:
            tariff_distribution_history_item = LocationTariffDistributionDto.from_dict(
                tariff_distribution_history_item_data
            )

            tariff_distribution_history.append(tariff_distribution_history_item)

        ou = d.pop("ou", UNSET)

        ou_id = d.pop("ouId", UNSET)

        ou_name = d.pop("ouName", UNSET)

        reimburse_info_dto = cls(
            type=type,
            has_guest_usage=has_guest_usage,
            has_guest_charging_reimbursement_fee=has_guest_charging_reimbursement_fee,
            country_code=country_code,
            party_id=party_id,
            external_organization_unit_id=external_organization_unit_id,
            external_organization_unit_name=external_organization_unit_name,
            external_organization_unit_reference=external_organization_unit_reference,
            external_organization_unit_code=external_organization_unit_code,
            charge_card_emaid=charge_card_emaid,
            charge_card_uid=charge_card_uid,
            charge_card_issuer=charge_card_issuer,
            tariffs=tariffs,
            bank_details=bank_details,
            tariff_distribution_id=tariff_distribution_id,
            tariff_distribution_history=tariff_distribution_history,
            ou=ou,
            ou_id=ou_id,
            ou_name=ou_name,
        )

        reimburse_info_dto.additional_properties = d
        return reimburse_info_dto

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
