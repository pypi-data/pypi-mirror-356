"""Contains all the data models used in inputs/outputs"""

from .additional_geo_location_dto import AdditionalGeoLocationDto
from .authorization_assertion_dto import AuthorizationAssertionDto
from .authorization_assertion_dto_auth_scenario_type import (
    AuthorizationAssertionDtoAuthScenarioType,
)
from .authorization_assertion_dto_status import AuthorizationAssertionDtoStatus
from .authorization_charger_context_dto import AuthorizationChargerContextDto
from .authorization_context_details_dto import AuthorizationContextDetailsDto
from .authorization_data import AuthorizationData
from .authorization_result_dto import AuthorizationResultDto
from .authorization_result_dto_reason import AuthorizationResultDtoReason
from .authorization_result_dto_status import AuthorizationResultDtoStatus
from .authorization_tenant_context_dto import AuthorizationTenantContextDto
from .business_details_dto import BusinessDetailsDto
from .cancel_reservation_request import CancelReservationRequest
from .cdr_dto import CdrDto
from .cdr_dto_approval_status import CdrDtoApprovalStatus
from .cdr_dto_financial_type import CdrDtoFinancialType
from .cdr_geo_location_dto import CdrGeoLocationDto
from .cdr_location_dto import CdrLocationDto
from .cdr_location_dto_power_type import CdrLocationDtoPowerType
from .cdr_patch_dto import CdrPatchDto
from .cdr_patch_dto_approval_status import CdrPatchDtoApprovalStatus
from .cdr_started_by_info_dto import CdrStartedByInfoDto
from .cdr_started_by_info_dto_authorization_state import (
    CdrStartedByInfoDtoAuthorizationState,
)
from .cdr_started_by_info_dto_roaming_platform_type import (
    CdrStartedByInfoDtoRoamingPlatformType,
)
from .cdr_started_by_token_dto import CdrStartedByTokenDto
from .cdr_started_by_token_dto_auth_method import CdrStartedByTokenDtoAuthMethod
from .cdr_started_by_token_dto_token_type import CdrStartedByTokenDtoTokenType
from .change_availability_request import ChangeAvailabilityRequest
from .change_availability_request_type import ChangeAvailabilityRequestType
from .change_configuration_request import ChangeConfigurationRequest
from .charge_point_authorize_get_dto import ChargePointAuthorizeGetDto
from .charge_point_authorize_get_dto_authorization_request_type import (
    ChargePointAuthorizeGetDtoAuthorizationRequestType,
)
from .charge_point_authorize_post_dto import ChargePointAuthorizePostDto
from .chargepoint_configuration_items_dto import ChargepointConfigurationItemsDto
from .chargepoint_connector_dto import ChargepointConnectorDto
from .chargepoint_connector_dto_format import ChargepointConnectorDtoFormat
from .chargepoint_connector_dto_operational_status import (
    ChargepointConnectorDtoOperationalStatus,
)
from .chargepoint_connector_dto_power_type import ChargepointConnectorDtoPowerType
from .chargepoint_connector_dto_standard import ChargepointConnectorDtoStandard
from .chargepoint_dto import ChargepointDto
from .chargepoint_dto_connectivity_status import ChargepointDtoConnectivityStatus
from .chargepoint_evse_dto import ChargepointEVSEDto
from .chargepoint_put_dto import ChargepointPutDto
from .chargepoint_status_dto import ChargepointStatusDto
from .chargepoint_status_dto_connectivity_status import (
    ChargepointStatusDtoConnectivityStatus,
)
from .charging_meter_value_dto import ChargingMeterValueDto
from .charging_meter_value_dto_measurand import ChargingMeterValueDtoMeasurand
from .charging_meter_value_dto_unit import ChargingMeterValueDtoUnit
from .charging_period_dto import ChargingPeriodDto
from .charging_profile import ChargingProfile
from .charging_profile_charging_profile_kind import ChargingProfileChargingProfileKind
from .charging_profile_charging_profile_purpose import (
    ChargingProfileChargingProfilePurpose,
)
from .charging_profile_recurrency_kind import ChargingProfileRecurrencyKind
from .charging_schedule import ChargingSchedule
from .charging_schedule_charging_rate_unit import ChargingScheduleChargingRateUnit
from .charging_schedule_period import ChargingSchedulePeriod
from .clear_cache_request import ClearCacheRequest
from .clear_charging_profile_request import ClearChargingProfileRequest
from .clear_charging_profile_request_charging_profile_purpose import (
    ClearChargingProfileRequestChargingProfilePurpose,
)
from .connector_dto import ConnectorDto
from .connector_dto_format import ConnectorDtoFormat
from .connector_dto_power_type import ConnectorDtoPowerType
from .connector_dto_standard import ConnectorDtoStandard
from .connector_operational_status_dto import ConnectorOperationalStatusDto
from .connector_operational_status_dto_operational_status import (
    ConnectorOperationalStatusDtoOperationalStatus,
)
from .cs_charging_profiles import CsChargingProfiles
from .cs_charging_profiles_charging_profile_kind import (
    CsChargingProfilesChargingProfileKind,
)
from .cs_charging_profiles_charging_profile_purpose import (
    CsChargingProfilesChargingProfilePurpose,
)
from .cs_charging_profiles_recurrency_kind import CsChargingProfilesRecurrencyKind
from .data_transfer_request import DataTransferRequest
from .display_text_dto import DisplayTextDto
from .energy_mix_dto import EnergyMixDto
from .energy_source_dto import EnergySourceDto
from .energy_source_dto_source import EnergySourceDtoSource
from .entity_tag_header_value import EntityTagHeaderValue
from .environmental_impact_dto import EnvironmentalImpactDto
from .environmental_impact_dto_category import EnvironmentalImpactDtoCategory
from .exceptional_period_dto import ExceptionalPeriodDto
from .file_content_result import FileContentResult
from .geo_location_dto import GeoLocationDto
from .get_all_cdrs_order_by import GetAllCdrsOrderBy
from .get_all_chargepoints_accesstype import GetAllChargepointsAccesstype
from .get_all_chargepoints_chargerpowertype import GetAllChargepointsChargerpowertype
from .get_all_chargepoints_operationalstatus import GetAllChargepointsOperationalstatus
from .get_all_chargepoints_order_by import GetAllChargepointsOrderBy
from .get_all_locations_accesstype import GetAllLocationsAccesstype
from .get_all_locations_chargerpowertype import GetAllLocationsChargerpowertype
from .get_all_locations_order_by import GetAllLocationsOrderBy
from .get_all_reimbursementcdrs_order_by import GetAllReimbursementcdrsOrderBy
from .get_all_sessions_order_by import GetAllSessionsOrderBy
from .get_all_tariffdistributions_order_by import GetAllTariffdistributionsOrderBy
from .get_all_tariffs_order_by import GetAllTariffsOrderBy
from .get_all_webhooks_order_by import GetAllWebhooksOrderBy
from .get_composite_schedule_request import GetCompositeScheduleRequest
from .get_composite_schedule_request_charging_rate_unit import (
    GetCompositeScheduleRequestChargingRateUnit,
)
from .get_configuration_request import GetConfigurationRequest
from .get_diagnostics_request import GetDiagnosticsRequest
from .get_local_list_version_request import GetLocalListVersionRequest
from .hours_dto import HoursDto
from .id_tag_info import IdTagInfo
from .id_tag_info_status import IdTagInfoStatus
from .image_dto import ImageDto
from .image_dto_category import ImageDtoCategory
from .interchange_format_cdr import InterchangeFormatCdr
from .local_token_group_get_dto import LocalTokenGroupGetDto
from .local_token_group_post_dto import LocalTokenGroupPostDto
from .local_token_group_put_dto import LocalTokenGroupPutDto
from .local_token_group_token_get_dto import LocalTokenGroupTokenGetDto
from .local_token_group_token_post_dto import LocalTokenGroupTokenPostDto
from .local_token_group_token_put_dto import LocalTokenGroupTokenPutDto
from .location_charge_point_dto import LocationChargePointDto
from .location_dto import LocationDto
from .location_dto_facilities_item import LocationDtoFacilitiesItem
from .location_dto_parking_type import LocationDtoParkingType
from .location_evse_dto import LocationEVSEDto
from .location_evse_dto_capabilities_item import LocationEVSEDtoCapabilitiesItem
from .location_evse_dto_parking_restrictions_item import (
    LocationEVSEDtoParkingRestrictionsItem,
)
from .location_evse_dto_status import LocationEVSEDtoStatus
from .location_post_dto import LocationPostDto
from .location_post_dto_facilities_item import LocationPostDtoFacilitiesItem
from .location_post_dto_parking_type import LocationPostDtoParkingType
from .location_put_dto import LocationPutDto
from .location_put_dto_facilities_item import LocationPutDtoFacilitiesItem
from .location_put_dto_parking_type import LocationPutDtoParkingType
from .location_tariff_distribution_dto import LocationTariffDistributionDto
from .longship_error import LongshipError
from .longship_error_detail import LongshipErrorDetail
from .message_log_dto import MessageLogDto
from .message_log_dto_direction import MessageLogDtoDirection
from .message_log_dto_ocpp_message_type import MessageLogDtoOcppMessageType
from .message_log_dto_wamp_message_type import MessageLogDtoWampMessageType
from .organization_unit_financial_details_dto import OrganizationUnitFinancialDetailsDto
from .organization_unit_get_dto import OrganizationUnitGetDto
from .organization_unit_post_dto import OrganizationUnitPostDto
from .organization_unit_put_dto import OrganizationUnitPutDto
from .price_info_dto import PriceInfoDto
from .private_emp_tariff_dto import PrivateEmpTariffDto
from .private_emp_tariff_dto_power_type import PrivateEmpTariffDtoPowerType
from .publish_token_type_dto import PublishTokenTypeDto
from .publish_token_type_dto_type import PublishTokenTypeDtoType
from .regular_hours_dto import RegularHoursDto
from .reimburse_info_dto import ReimburseInfoDto
from .reimburse_info_dto_type import ReimburseInfoDtoType
from .reimburse_started_by_info_dto import ReimburseStartedByInfoDto
from .reimburse_started_by_info_dto_authorization_state import (
    ReimburseStartedByInfoDtoAuthorizationState,
)
from .reimburse_started_by_token_dto import ReimburseStartedByTokenDto
from .reimburse_started_by_token_dto_auth_method import (
    ReimburseStartedByTokenDtoAuthMethod,
)
from .reimburse_started_by_token_dto_token_type import (
    ReimburseStartedByTokenDtoTokenType,
)
from .reimbursement_bank_details_dto import ReimbursementBankDetailsDto
from .reimbursement_cdr_dto import ReimbursementCdrDto
from .reimbursement_cdr_geo_location_dto import ReimbursementCdrGeoLocationDto
from .reimbursement_cdr_location_dto import ReimbursementCdrLocationDto
from .reimbursement_cdr_location_dto_power_type import (
    ReimbursementCdrLocationDtoPowerType,
)
from .reimbursement_customer_share_dto import ReimbursementCustomerShareDto
from .reimbursement_price_dto import ReimbursementPriceDto
from .reimbursement_tariff_dto import ReimbursementTariffDto
from .reimbursement_tariff_dto_status import ReimbursementTariffDtoStatus
from .remote_start_transaction_request import RemoteStartTransactionRequest
from .remote_stop_transaction_request import RemoteStopTransactionRequest
from .reserve_now_request import ReserveNowRequest
from .reset_request import ResetRequest
from .reset_request_type import ResetRequestType
from .send_local_list_request import SendLocalListRequest
from .send_local_list_request_update_type import SendLocalListRequestUpdateType
from .session_dto import SessionDto
from .session_dto_approval_status import SessionDtoApprovalStatus
from .session_dto_review_scenario_type import SessionDtoReviewScenarioType
from .session_dto_status import SessionDtoStatus
from .session_geo_location_dto import SessionGeoLocationDto
from .session_location_dto import SessionLocationDto
from .session_location_dto_power_type import SessionLocationDtoPowerType
from .session_threshold_check_dto import SessionThresholdCheckDto
from .session_threshold_check_dto_status import SessionThresholdCheckDtoStatus
from .session_threshold_check_dto_threshold_hit_outcome import (
    SessionThresholdCheckDtoThresholdHitOutcome,
)
from .session_threshold_value_dto_decimal import SessionThresholdValueDtoDecimal
from .session_threshold_value_dto_decimal_status import (
    SessionThresholdValueDtoDecimalStatus,
)
from .session_threshold_value_dto_decimal_threshold_hit_outcome import (
    SessionThresholdValueDtoDecimalThresholdHitOutcome,
)
from .session_threshold_value_dto_int_32 import SessionThresholdValueDtoInt32
from .session_threshold_value_dto_int_32_status import (
    SessionThresholdValueDtoInt32Status,
)
from .session_threshold_value_dto_int_32_threshold_hit_outcome import (
    SessionThresholdValueDtoInt32ThresholdHitOutcome,
)
from .session_thresholds_dto import SessionThresholdsDto
from .session_thresholds_dto_thresholds_hit_item import (
    SessionThresholdsDtoThresholdsHitItem,
)
from .set_charging_profile_request import SetChargingProfileRequest
from .started_by_info_dto import StartedByInfoDto
from .started_by_info_dto_authorization_state import StartedByInfoDtoAuthorizationState
from .started_by_info_dto_roaming_platform_type import (
    StartedByInfoDtoRoamingPlatformType,
)
from .started_by_token_dto import StartedByTokenDto
from .started_by_token_dto_auth_method import StartedByTokenDtoAuthMethod
from .started_by_token_dto_token_type import StartedByTokenDtoTokenType
from .status_schedule_dto import StatusScheduleDto
from .status_schedule_dto_status import StatusScheduleDtoStatus
from .string_segment import StringSegment
from .tariff_assertion_dto import TariffAssertionDto
from .tariff_assertion_dto_tariff_type import TariffAssertionDtoTariffType
from .tariff_distribution_get_dto import TariffDistributionGetDto
from .tariff_distribution_history_dto import TariffDistributionHistoryDto
from .tariff_distribution_post_dto import TariffDistributionPostDto
from .tariff_distribution_put_dto import TariffDistributionPutDto
from .tariff_dto import TariffDto
from .tariff_dto_tariff_type import TariffDtoTariffType
from .tariff_dto_usage_type import TariffDtoUsageType
from .tariff_info_dto import TariffInfoDto
from .tariff_post_dto import TariffPostDto
from .tariff_post_dto_usage_type import TariffPostDtoUsageType
from .tariff_price_dto import TariffPriceDto
from .tariff_price_dto_approval_status import TariffPriceDtoApprovalStatus
from .tariff_put_dto import TariffPutDto
from .tariff_restriction import TariffRestriction
from .tariff_restriction_day_of_week import TariffRestrictionDayOfWeek
from .token_info_dto import TokenInfoDto
from .token_info_dto_token_type import TokenInfoDtoTokenType
from .trigger_message_request import TriggerMessageRequest
from .trigger_message_request_requested_message import (
    TriggerMessageRequestRequestedMessage,
)
from .unlock_connector_request import UnlockConnectorRequest
from .update_firmware_request import UpdateFirmwareRequest
from .webhook_get_dto import WebhookGetDto
from .webhook_get_dto_event_types_item import WebhookGetDtoEventTypesItem
from .webhook_header_dto import WebhookHeaderDto
from .webhook_post_dto import WebhookPostDto
from .webhook_post_dto_event_types_item import WebhookPostDtoEventTypesItem
from .webhook_put_dto import WebhookPutDto
from .webhook_put_dto_event_types_item import WebhookPutDtoEventTypesItem
from .webhook_summary_get_dto import WebhookSummaryGetDto
from .webhook_summary_get_dto_event_types_item import WebhookSummaryGetDtoEventTypesItem

__all__ = (
    "AdditionalGeoLocationDto",
    "AuthorizationAssertionDto",
    "AuthorizationAssertionDtoAuthScenarioType",
    "AuthorizationAssertionDtoStatus",
    "AuthorizationChargerContextDto",
    "AuthorizationContextDetailsDto",
    "AuthorizationData",
    "AuthorizationResultDto",
    "AuthorizationResultDtoReason",
    "AuthorizationResultDtoStatus",
    "AuthorizationTenantContextDto",
    "BusinessDetailsDto",
    "CancelReservationRequest",
    "CdrDto",
    "CdrDtoApprovalStatus",
    "CdrDtoFinancialType",
    "CdrGeoLocationDto",
    "CdrLocationDto",
    "CdrLocationDtoPowerType",
    "CdrPatchDto",
    "CdrPatchDtoApprovalStatus",
    "CdrStartedByInfoDto",
    "CdrStartedByInfoDtoAuthorizationState",
    "CdrStartedByInfoDtoRoamingPlatformType",
    "CdrStartedByTokenDto",
    "CdrStartedByTokenDtoAuthMethod",
    "CdrStartedByTokenDtoTokenType",
    "ChangeAvailabilityRequest",
    "ChangeAvailabilityRequestType",
    "ChangeConfigurationRequest",
    "ChargePointAuthorizeGetDto",
    "ChargePointAuthorizeGetDtoAuthorizationRequestType",
    "ChargePointAuthorizePostDto",
    "ChargepointConfigurationItemsDto",
    "ChargepointConnectorDto",
    "ChargepointConnectorDtoFormat",
    "ChargepointConnectorDtoOperationalStatus",
    "ChargepointConnectorDtoPowerType",
    "ChargepointConnectorDtoStandard",
    "ChargepointDto",
    "ChargepointDtoConnectivityStatus",
    "ChargepointEVSEDto",
    "ChargepointPutDto",
    "ChargepointStatusDto",
    "ChargepointStatusDtoConnectivityStatus",
    "ChargingMeterValueDto",
    "ChargingMeterValueDtoMeasurand",
    "ChargingMeterValueDtoUnit",
    "ChargingPeriodDto",
    "ChargingProfile",
    "ChargingProfileChargingProfileKind",
    "ChargingProfileChargingProfilePurpose",
    "ChargingProfileRecurrencyKind",
    "ChargingSchedule",
    "ChargingScheduleChargingRateUnit",
    "ChargingSchedulePeriod",
    "ClearCacheRequest",
    "ClearChargingProfileRequest",
    "ClearChargingProfileRequestChargingProfilePurpose",
    "ConnectorDto",
    "ConnectorDtoFormat",
    "ConnectorDtoPowerType",
    "ConnectorDtoStandard",
    "ConnectorOperationalStatusDto",
    "ConnectorOperationalStatusDtoOperationalStatus",
    "CsChargingProfiles",
    "CsChargingProfilesChargingProfileKind",
    "CsChargingProfilesChargingProfilePurpose",
    "CsChargingProfilesRecurrencyKind",
    "DataTransferRequest",
    "DisplayTextDto",
    "EnergyMixDto",
    "EnergySourceDto",
    "EnergySourceDtoSource",
    "EntityTagHeaderValue",
    "EnvironmentalImpactDto",
    "EnvironmentalImpactDtoCategory",
    "ExceptionalPeriodDto",
    "FileContentResult",
    "GeoLocationDto",
    "GetAllCdrsOrderBy",
    "GetAllChargepointsAccesstype",
    "GetAllChargepointsChargerpowertype",
    "GetAllChargepointsOperationalstatus",
    "GetAllChargepointsOrderBy",
    "GetAllLocationsAccesstype",
    "GetAllLocationsChargerpowertype",
    "GetAllLocationsOrderBy",
    "GetAllReimbursementcdrsOrderBy",
    "GetAllSessionsOrderBy",
    "GetAllTariffdistributionsOrderBy",
    "GetAllTariffsOrderBy",
    "GetAllWebhooksOrderBy",
    "GetCompositeScheduleRequest",
    "GetCompositeScheduleRequestChargingRateUnit",
    "GetConfigurationRequest",
    "GetDiagnosticsRequest",
    "GetLocalListVersionRequest",
    "HoursDto",
    "IdTagInfo",
    "IdTagInfoStatus",
    "ImageDto",
    "ImageDtoCategory",
    "InterchangeFormatCdr",
    "LocalTokenGroupGetDto",
    "LocalTokenGroupPostDto",
    "LocalTokenGroupPutDto",
    "LocalTokenGroupTokenGetDto",
    "LocalTokenGroupTokenPostDto",
    "LocalTokenGroupTokenPutDto",
    "LocationChargePointDto",
    "LocationDto",
    "LocationDtoFacilitiesItem",
    "LocationDtoParkingType",
    "LocationEVSEDto",
    "LocationEVSEDtoCapabilitiesItem",
    "LocationEVSEDtoParkingRestrictionsItem",
    "LocationEVSEDtoStatus",
    "LocationPostDto",
    "LocationPostDtoFacilitiesItem",
    "LocationPostDtoParkingType",
    "LocationPutDto",
    "LocationPutDtoFacilitiesItem",
    "LocationPutDtoParkingType",
    "LocationTariffDistributionDto",
    "LongshipError",
    "LongshipErrorDetail",
    "MessageLogDto",
    "MessageLogDtoDirection",
    "MessageLogDtoOcppMessageType",
    "MessageLogDtoWampMessageType",
    "OrganizationUnitFinancialDetailsDto",
    "OrganizationUnitGetDto",
    "OrganizationUnitPostDto",
    "OrganizationUnitPutDto",
    "PriceInfoDto",
    "PrivateEmpTariffDto",
    "PrivateEmpTariffDtoPowerType",
    "PublishTokenTypeDto",
    "PublishTokenTypeDtoType",
    "RegularHoursDto",
    "ReimburseInfoDto",
    "ReimburseInfoDtoType",
    "ReimbursementBankDetailsDto",
    "ReimbursementCdrDto",
    "ReimbursementCdrGeoLocationDto",
    "ReimbursementCdrLocationDto",
    "ReimbursementCdrLocationDtoPowerType",
    "ReimbursementCustomerShareDto",
    "ReimbursementPriceDto",
    "ReimbursementTariffDto",
    "ReimbursementTariffDtoStatus",
    "ReimburseStartedByInfoDto",
    "ReimburseStartedByInfoDtoAuthorizationState",
    "ReimburseStartedByTokenDto",
    "ReimburseStartedByTokenDtoAuthMethod",
    "ReimburseStartedByTokenDtoTokenType",
    "RemoteStartTransactionRequest",
    "RemoteStopTransactionRequest",
    "ReserveNowRequest",
    "ResetRequest",
    "ResetRequestType",
    "SendLocalListRequest",
    "SendLocalListRequestUpdateType",
    "SessionDto",
    "SessionDtoApprovalStatus",
    "SessionDtoReviewScenarioType",
    "SessionDtoStatus",
    "SessionGeoLocationDto",
    "SessionLocationDto",
    "SessionLocationDtoPowerType",
    "SessionThresholdCheckDto",
    "SessionThresholdCheckDtoStatus",
    "SessionThresholdCheckDtoThresholdHitOutcome",
    "SessionThresholdsDto",
    "SessionThresholdsDtoThresholdsHitItem",
    "SessionThresholdValueDtoDecimal",
    "SessionThresholdValueDtoDecimalStatus",
    "SessionThresholdValueDtoDecimalThresholdHitOutcome",
    "SessionThresholdValueDtoInt32",
    "SessionThresholdValueDtoInt32Status",
    "SessionThresholdValueDtoInt32ThresholdHitOutcome",
    "SetChargingProfileRequest",
    "StartedByInfoDto",
    "StartedByInfoDtoAuthorizationState",
    "StartedByInfoDtoRoamingPlatformType",
    "StartedByTokenDto",
    "StartedByTokenDtoAuthMethod",
    "StartedByTokenDtoTokenType",
    "StatusScheduleDto",
    "StatusScheduleDtoStatus",
    "StringSegment",
    "TariffAssertionDto",
    "TariffAssertionDtoTariffType",
    "TariffDistributionGetDto",
    "TariffDistributionHistoryDto",
    "TariffDistributionPostDto",
    "TariffDistributionPutDto",
    "TariffDto",
    "TariffDtoTariffType",
    "TariffDtoUsageType",
    "TariffInfoDto",
    "TariffPostDto",
    "TariffPostDtoUsageType",
    "TariffPriceDto",
    "TariffPriceDtoApprovalStatus",
    "TariffPutDto",
    "TariffRestriction",
    "TariffRestrictionDayOfWeek",
    "TokenInfoDto",
    "TokenInfoDtoTokenType",
    "TriggerMessageRequest",
    "TriggerMessageRequestRequestedMessage",
    "UnlockConnectorRequest",
    "UpdateFirmwareRequest",
    "WebhookGetDto",
    "WebhookGetDtoEventTypesItem",
    "WebhookHeaderDto",
    "WebhookPostDto",
    "WebhookPostDtoEventTypesItem",
    "WebhookPutDto",
    "WebhookPutDtoEventTypesItem",
    "WebhookSummaryGetDto",
    "WebhookSummaryGetDtoEventTypesItem",
)
