from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.session_dto import SessionDto
from ...types import Unset
import datetime
from ...models.longship_error import LongshipError
from ...models.get_all_sessions_order_by import GetAllSessionsOrderBy


def _get_kwargs(
    *,
    skip: Union[Unset, int] = UNSET,
    take: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
    connector_number: Union[Unset, int] = UNSET,
    chargepoint_id: Union[Unset, str] = UNSET,
    running_only: Union[Unset, bool] = UNSET,
    completed_only: Union[Unset, bool] = UNSET,
    suspicious_only: Union[Unset, bool] = UNSET,
    rejected_only: Union[Unset, bool] = UNSET,
    local_only: Union[Unset, bool] = UNSET,
    unauthorized_only: Union[Unset, bool] = UNSET,
    roamingconnectionid: Union[Unset, str] = UNSET,
    organizationunitcode: Union[Unset, str] = UNSET,
    tariff_id: Union[Unset, str] = UNSET,
    pricegreaterthen: Union[Unset, float] = UNSET,
    pricelessthen: Union[Unset, float] = UNSET,
    kwhgreaterthen: Union[Unset, float] = UNSET,
    kwhlessthen: Union[Unset, float] = UNSET,
    contractid: Union[Unset, str] = UNSET,
    providerid: Union[Unset, str] = UNSET,
    authorizationreferenceid: Union[Unset, str] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    order_by: Union[Unset, GetAllSessionsOrderBy] = GetAllSessionsOrderBy.START,
    descending: Union[Unset, bool] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["skip"] = skip

    params["take"] = take

    params["search"] = search

    params["connectorNumber"] = connector_number

    params["chargepointId"] = chargepoint_id

    params["runningOnly"] = running_only

    params["completedOnly"] = completed_only

    params["suspiciousOnly"] = suspicious_only

    params["rejectedOnly"] = rejected_only

    params["localOnly"] = local_only

    params["unauthorizedOnly"] = unauthorized_only

    params["roamingconnectionid"] = roamingconnectionid

    params["organizationunitcode"] = organizationunitcode

    params["tariffId"] = tariff_id

    params["pricegreaterthen"] = pricegreaterthen

    params["pricelessthen"] = pricelessthen

    params["kwhgreaterthen"] = kwhgreaterthen

    params["kwhlessthen"] = kwhlessthen

    params["contractid"] = contractid

    params["providerid"] = providerid

    params["authorizationreferenceid"] = authorizationreferenceid

    json_from_: Union[Unset, str] = UNSET
    if not isinstance(from_, Unset):
        json_from_ = from_.isoformat()
    params["from"] = json_from_

    json_to: Union[Unset, str] = UNSET
    if not isinstance(to, Unset):
        json_to = to.isoformat()
    params["to"] = json_to

    json_order_by: Union[Unset, str] = UNSET
    if not isinstance(order_by, Unset):
        json_order_by = order_by.value

    params["orderBy"] = json_order_by

    params["descending"] = descending

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/v1/sessions",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[List["SessionDto"], LongshipError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for componentsschemassession_dto_array_item_data in _response_200:
            componentsschemassession_dto_array_item = SessionDto.from_dict(
                componentsschemassession_dto_array_item_data
            )

            response_200.append(componentsschemassession_dto_array_item)

        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = LongshipError.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = LongshipError.from_dict(response.json())

        return response_500
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = LongshipError.from_dict(response.json())

        return response_403
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[List["SessionDto"], LongshipError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    skip: Union[Unset, int] = UNSET,
    take: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
    connector_number: Union[Unset, int] = UNSET,
    chargepoint_id: Union[Unset, str] = UNSET,
    running_only: Union[Unset, bool] = UNSET,
    completed_only: Union[Unset, bool] = UNSET,
    suspicious_only: Union[Unset, bool] = UNSET,
    rejected_only: Union[Unset, bool] = UNSET,
    local_only: Union[Unset, bool] = UNSET,
    unauthorized_only: Union[Unset, bool] = UNSET,
    roamingconnectionid: Union[Unset, str] = UNSET,
    organizationunitcode: Union[Unset, str] = UNSET,
    tariff_id: Union[Unset, str] = UNSET,
    pricegreaterthen: Union[Unset, float] = UNSET,
    pricelessthen: Union[Unset, float] = UNSET,
    kwhgreaterthen: Union[Unset, float] = UNSET,
    kwhlessthen: Union[Unset, float] = UNSET,
    contractid: Union[Unset, str] = UNSET,
    providerid: Union[Unset, str] = UNSET,
    authorizationreferenceid: Union[Unset, str] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    order_by: Union[Unset, GetAllSessionsOrderBy] = GetAllSessionsOrderBy.START,
    descending: Union[Unset, bool] = UNSET,
) -> Response[Union[List["SessionDto"], LongshipError]]:
    """Get a list of sessions.

     Get a paged list of sessions, taken the filters into account.

    Args:
        skip (Union[Unset, int]):
        take (Union[Unset, int]):
        search (Union[Unset, str]):
        connector_number (Union[Unset, int]):
        chargepoint_id (Union[Unset, str]):
        running_only (Union[Unset, bool]):
        completed_only (Union[Unset, bool]):
        suspicious_only (Union[Unset, bool]):
        rejected_only (Union[Unset, bool]):
        local_only (Union[Unset, bool]):
        unauthorized_only (Union[Unset, bool]):
        roamingconnectionid (Union[Unset, str]):
        organizationunitcode (Union[Unset, str]):
        tariff_id (Union[Unset, str]):
        pricegreaterthen (Union[Unset, float]):
        pricelessthen (Union[Unset, float]):
        kwhgreaterthen (Union[Unset, float]):
        kwhlessthen (Union[Unset, float]):
        contractid (Union[Unset, str]):
        providerid (Union[Unset, str]):
        authorizationreferenceid (Union[Unset, str]):
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):
        order_by (Union[Unset, GetAllSessionsOrderBy]):  Default: GetAllSessionsOrderBy.START.
        descending (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[List['SessionDto'], LongshipError]]
    """

    kwargs = _get_kwargs(
        skip=skip,
        take=take,
        search=search,
        connector_number=connector_number,
        chargepoint_id=chargepoint_id,
        running_only=running_only,
        completed_only=completed_only,
        suspicious_only=suspicious_only,
        rejected_only=rejected_only,
        local_only=local_only,
        unauthorized_only=unauthorized_only,
        roamingconnectionid=roamingconnectionid,
        organizationunitcode=organizationunitcode,
        tariff_id=tariff_id,
        pricegreaterthen=pricegreaterthen,
        pricelessthen=pricelessthen,
        kwhgreaterthen=kwhgreaterthen,
        kwhlessthen=kwhlessthen,
        contractid=contractid,
        providerid=providerid,
        authorizationreferenceid=authorizationreferenceid,
        from_=from_,
        to=to,
        order_by=order_by,
        descending=descending,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    skip: Union[Unset, int] = UNSET,
    take: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
    connector_number: Union[Unset, int] = UNSET,
    chargepoint_id: Union[Unset, str] = UNSET,
    running_only: Union[Unset, bool] = UNSET,
    completed_only: Union[Unset, bool] = UNSET,
    suspicious_only: Union[Unset, bool] = UNSET,
    rejected_only: Union[Unset, bool] = UNSET,
    local_only: Union[Unset, bool] = UNSET,
    unauthorized_only: Union[Unset, bool] = UNSET,
    roamingconnectionid: Union[Unset, str] = UNSET,
    organizationunitcode: Union[Unset, str] = UNSET,
    tariff_id: Union[Unset, str] = UNSET,
    pricegreaterthen: Union[Unset, float] = UNSET,
    pricelessthen: Union[Unset, float] = UNSET,
    kwhgreaterthen: Union[Unset, float] = UNSET,
    kwhlessthen: Union[Unset, float] = UNSET,
    contractid: Union[Unset, str] = UNSET,
    providerid: Union[Unset, str] = UNSET,
    authorizationreferenceid: Union[Unset, str] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    order_by: Union[Unset, GetAllSessionsOrderBy] = GetAllSessionsOrderBy.START,
    descending: Union[Unset, bool] = UNSET,
) -> Optional[Union[List["SessionDto"], LongshipError]]:
    """Get a list of sessions.

     Get a paged list of sessions, taken the filters into account.

    Args:
        skip (Union[Unset, int]):
        take (Union[Unset, int]):
        search (Union[Unset, str]):
        connector_number (Union[Unset, int]):
        chargepoint_id (Union[Unset, str]):
        running_only (Union[Unset, bool]):
        completed_only (Union[Unset, bool]):
        suspicious_only (Union[Unset, bool]):
        rejected_only (Union[Unset, bool]):
        local_only (Union[Unset, bool]):
        unauthorized_only (Union[Unset, bool]):
        roamingconnectionid (Union[Unset, str]):
        organizationunitcode (Union[Unset, str]):
        tariff_id (Union[Unset, str]):
        pricegreaterthen (Union[Unset, float]):
        pricelessthen (Union[Unset, float]):
        kwhgreaterthen (Union[Unset, float]):
        kwhlessthen (Union[Unset, float]):
        contractid (Union[Unset, str]):
        providerid (Union[Unset, str]):
        authorizationreferenceid (Union[Unset, str]):
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):
        order_by (Union[Unset, GetAllSessionsOrderBy]):  Default: GetAllSessionsOrderBy.START.
        descending (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[List['SessionDto'], LongshipError]
    """

    return sync_detailed(
        client=client,
        skip=skip,
        take=take,
        search=search,
        connector_number=connector_number,
        chargepoint_id=chargepoint_id,
        running_only=running_only,
        completed_only=completed_only,
        suspicious_only=suspicious_only,
        rejected_only=rejected_only,
        local_only=local_only,
        unauthorized_only=unauthorized_only,
        roamingconnectionid=roamingconnectionid,
        organizationunitcode=organizationunitcode,
        tariff_id=tariff_id,
        pricegreaterthen=pricegreaterthen,
        pricelessthen=pricelessthen,
        kwhgreaterthen=kwhgreaterthen,
        kwhlessthen=kwhlessthen,
        contractid=contractid,
        providerid=providerid,
        authorizationreferenceid=authorizationreferenceid,
        from_=from_,
        to=to,
        order_by=order_by,
        descending=descending,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    skip: Union[Unset, int] = UNSET,
    take: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
    connector_number: Union[Unset, int] = UNSET,
    chargepoint_id: Union[Unset, str] = UNSET,
    running_only: Union[Unset, bool] = UNSET,
    completed_only: Union[Unset, bool] = UNSET,
    suspicious_only: Union[Unset, bool] = UNSET,
    rejected_only: Union[Unset, bool] = UNSET,
    local_only: Union[Unset, bool] = UNSET,
    unauthorized_only: Union[Unset, bool] = UNSET,
    roamingconnectionid: Union[Unset, str] = UNSET,
    organizationunitcode: Union[Unset, str] = UNSET,
    tariff_id: Union[Unset, str] = UNSET,
    pricegreaterthen: Union[Unset, float] = UNSET,
    pricelessthen: Union[Unset, float] = UNSET,
    kwhgreaterthen: Union[Unset, float] = UNSET,
    kwhlessthen: Union[Unset, float] = UNSET,
    contractid: Union[Unset, str] = UNSET,
    providerid: Union[Unset, str] = UNSET,
    authorizationreferenceid: Union[Unset, str] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    order_by: Union[Unset, GetAllSessionsOrderBy] = GetAllSessionsOrderBy.START,
    descending: Union[Unset, bool] = UNSET,
) -> Response[Union[List["SessionDto"], LongshipError]]:
    """Get a list of sessions.

     Get a paged list of sessions, taken the filters into account.

    Args:
        skip (Union[Unset, int]):
        take (Union[Unset, int]):
        search (Union[Unset, str]):
        connector_number (Union[Unset, int]):
        chargepoint_id (Union[Unset, str]):
        running_only (Union[Unset, bool]):
        completed_only (Union[Unset, bool]):
        suspicious_only (Union[Unset, bool]):
        rejected_only (Union[Unset, bool]):
        local_only (Union[Unset, bool]):
        unauthorized_only (Union[Unset, bool]):
        roamingconnectionid (Union[Unset, str]):
        organizationunitcode (Union[Unset, str]):
        tariff_id (Union[Unset, str]):
        pricegreaterthen (Union[Unset, float]):
        pricelessthen (Union[Unset, float]):
        kwhgreaterthen (Union[Unset, float]):
        kwhlessthen (Union[Unset, float]):
        contractid (Union[Unset, str]):
        providerid (Union[Unset, str]):
        authorizationreferenceid (Union[Unset, str]):
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):
        order_by (Union[Unset, GetAllSessionsOrderBy]):  Default: GetAllSessionsOrderBy.START.
        descending (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[List['SessionDto'], LongshipError]]
    """

    kwargs = _get_kwargs(
        skip=skip,
        take=take,
        search=search,
        connector_number=connector_number,
        chargepoint_id=chargepoint_id,
        running_only=running_only,
        completed_only=completed_only,
        suspicious_only=suspicious_only,
        rejected_only=rejected_only,
        local_only=local_only,
        unauthorized_only=unauthorized_only,
        roamingconnectionid=roamingconnectionid,
        organizationunitcode=organizationunitcode,
        tariff_id=tariff_id,
        pricegreaterthen=pricegreaterthen,
        pricelessthen=pricelessthen,
        kwhgreaterthen=kwhgreaterthen,
        kwhlessthen=kwhlessthen,
        contractid=contractid,
        providerid=providerid,
        authorizationreferenceid=authorizationreferenceid,
        from_=from_,
        to=to,
        order_by=order_by,
        descending=descending,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    skip: Union[Unset, int] = UNSET,
    take: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
    connector_number: Union[Unset, int] = UNSET,
    chargepoint_id: Union[Unset, str] = UNSET,
    running_only: Union[Unset, bool] = UNSET,
    completed_only: Union[Unset, bool] = UNSET,
    suspicious_only: Union[Unset, bool] = UNSET,
    rejected_only: Union[Unset, bool] = UNSET,
    local_only: Union[Unset, bool] = UNSET,
    unauthorized_only: Union[Unset, bool] = UNSET,
    roamingconnectionid: Union[Unset, str] = UNSET,
    organizationunitcode: Union[Unset, str] = UNSET,
    tariff_id: Union[Unset, str] = UNSET,
    pricegreaterthen: Union[Unset, float] = UNSET,
    pricelessthen: Union[Unset, float] = UNSET,
    kwhgreaterthen: Union[Unset, float] = UNSET,
    kwhlessthen: Union[Unset, float] = UNSET,
    contractid: Union[Unset, str] = UNSET,
    providerid: Union[Unset, str] = UNSET,
    authorizationreferenceid: Union[Unset, str] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    order_by: Union[Unset, GetAllSessionsOrderBy] = GetAllSessionsOrderBy.START,
    descending: Union[Unset, bool] = UNSET,
) -> Optional[Union[List["SessionDto"], LongshipError]]:
    """Get a list of sessions.

     Get a paged list of sessions, taken the filters into account.

    Args:
        skip (Union[Unset, int]):
        take (Union[Unset, int]):
        search (Union[Unset, str]):
        connector_number (Union[Unset, int]):
        chargepoint_id (Union[Unset, str]):
        running_only (Union[Unset, bool]):
        completed_only (Union[Unset, bool]):
        suspicious_only (Union[Unset, bool]):
        rejected_only (Union[Unset, bool]):
        local_only (Union[Unset, bool]):
        unauthorized_only (Union[Unset, bool]):
        roamingconnectionid (Union[Unset, str]):
        organizationunitcode (Union[Unset, str]):
        tariff_id (Union[Unset, str]):
        pricegreaterthen (Union[Unset, float]):
        pricelessthen (Union[Unset, float]):
        kwhgreaterthen (Union[Unset, float]):
        kwhlessthen (Union[Unset, float]):
        contractid (Union[Unset, str]):
        providerid (Union[Unset, str]):
        authorizationreferenceid (Union[Unset, str]):
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):
        order_by (Union[Unset, GetAllSessionsOrderBy]):  Default: GetAllSessionsOrderBy.START.
        descending (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[List['SessionDto'], LongshipError]
    """

    return (
        await asyncio_detailed(
            client=client,
            skip=skip,
            take=take,
            search=search,
            connector_number=connector_number,
            chargepoint_id=chargepoint_id,
            running_only=running_only,
            completed_only=completed_only,
            suspicious_only=suspicious_only,
            rejected_only=rejected_only,
            local_only=local_only,
            unauthorized_only=unauthorized_only,
            roamingconnectionid=roamingconnectionid,
            organizationunitcode=organizationunitcode,
            tariff_id=tariff_id,
            pricegreaterthen=pricegreaterthen,
            pricelessthen=pricelessthen,
            kwhgreaterthen=kwhgreaterthen,
            kwhlessthen=kwhlessthen,
            contractid=contractid,
            providerid=providerid,
            authorizationreferenceid=authorizationreferenceid,
            from_=from_,
            to=to,
            order_by=order_by,
            descending=descending,
        )
    ).parsed
