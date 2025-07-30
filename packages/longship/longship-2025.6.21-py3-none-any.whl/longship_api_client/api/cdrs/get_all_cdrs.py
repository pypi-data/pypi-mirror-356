from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.cdr_dto import CdrDto
from ...models.get_all_cdrs_order_by import GetAllCdrsOrderBy
from ...types import Unset
import datetime
from ...models.longship_error import LongshipError


def _get_kwargs(
    *,
    skip: Union[Unset, int] = UNSET,
    take: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
    providerexclude: Union[Unset, str] = UNSET,
    tariff_id: Union[Unset, str] = UNSET,
    idtag: Union[Unset, str] = UNSET,
    authorizationreferenceid: Union[Unset, str] = UNSET,
    providerid: Union[Unset, str] = UNSET,
    pricegreaterthen: Union[Unset, float] = UNSET,
    pricelessthen: Union[Unset, float] = UNSET,
    kwhgreaterthen: Union[Unset, float] = UNSET,
    kwhlessthen: Union[Unset, float] = UNSET,
    durationinhoursgreaterthen: Union[Unset, float] = UNSET,
    durationinhourslessthen: Union[Unset, float] = UNSET,
    chargepoint_id: Union[Unset, str] = UNSET,
    connector_number: Union[Unset, int] = UNSET,
    roamingconnectionid: Union[Unset, str] = UNSET,
    organizationunitcode: Union[Unset, str] = UNSET,
    local_only: Union[Unset, bool] = UNSET,
    order_by: Union[Unset, GetAllCdrsOrderBy] = GetAllCdrsOrderBy.STARTDATETIME,
    descending: Union[Unset, bool] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["skip"] = skip

    params["take"] = take

    params["search"] = search

    params["providerexclude"] = providerexclude

    params["tariffId"] = tariff_id

    params["idtag"] = idtag

    params["authorizationreferenceid"] = authorizationreferenceid

    params["providerid"] = providerid

    params["pricegreaterthen"] = pricegreaterthen

    params["pricelessthen"] = pricelessthen

    params["kwhgreaterthen"] = kwhgreaterthen

    params["kwhlessthen"] = kwhlessthen

    params["durationinhoursgreaterthen"] = durationinhoursgreaterthen

    params["durationinhourslessthen"] = durationinhourslessthen

    params["chargepointId"] = chargepoint_id

    params["connectorNumber"] = connector_number

    params["roamingconnectionid"] = roamingconnectionid

    params["organizationunitcode"] = organizationunitcode

    params["localOnly"] = local_only

    json_order_by: Union[Unset, str] = UNSET
    if not isinstance(order_by, Unset):
        json_order_by = order_by.value

    params["orderBy"] = json_order_by

    params["descending"] = descending

    json_from_: Union[Unset, str] = UNSET
    if not isinstance(from_, Unset):
        json_from_ = from_.isoformat()
    params["from"] = json_from_

    json_to: Union[Unset, str] = UNSET
    if not isinstance(to, Unset):
        json_to = to.isoformat()
    params["to"] = json_to

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/v1/cdrs",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[List["CdrDto"], LongshipError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for componentsschemascdr_dto_array_item_data in _response_200:
            componentsschemascdr_dto_array_item = CdrDto.from_dict(
                componentsschemascdr_dto_array_item_data
            )

            response_200.append(componentsschemascdr_dto_array_item)

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
) -> Response[Union[List["CdrDto"], LongshipError]]:
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
    providerexclude: Union[Unset, str] = UNSET,
    tariff_id: Union[Unset, str] = UNSET,
    idtag: Union[Unset, str] = UNSET,
    authorizationreferenceid: Union[Unset, str] = UNSET,
    providerid: Union[Unset, str] = UNSET,
    pricegreaterthen: Union[Unset, float] = UNSET,
    pricelessthen: Union[Unset, float] = UNSET,
    kwhgreaterthen: Union[Unset, float] = UNSET,
    kwhlessthen: Union[Unset, float] = UNSET,
    durationinhoursgreaterthen: Union[Unset, float] = UNSET,
    durationinhourslessthen: Union[Unset, float] = UNSET,
    chargepoint_id: Union[Unset, str] = UNSET,
    connector_number: Union[Unset, int] = UNSET,
    roamingconnectionid: Union[Unset, str] = UNSET,
    organizationunitcode: Union[Unset, str] = UNSET,
    local_only: Union[Unset, bool] = UNSET,
    order_by: Union[Unset, GetAllCdrsOrderBy] = GetAllCdrsOrderBy.STARTDATETIME,
    descending: Union[Unset, bool] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
) -> Response[Union[List["CdrDto"], LongshipError]]:
    """Get a list of cdrs.

     Get a paged list of cdrs, taken the filters into account.

    Args:
        skip (Union[Unset, int]):
        take (Union[Unset, int]):
        search (Union[Unset, str]):
        providerexclude (Union[Unset, str]):
        tariff_id (Union[Unset, str]):
        idtag (Union[Unset, str]):
        authorizationreferenceid (Union[Unset, str]):
        providerid (Union[Unset, str]):
        pricegreaterthen (Union[Unset, float]):
        pricelessthen (Union[Unset, float]):
        kwhgreaterthen (Union[Unset, float]):
        kwhlessthen (Union[Unset, float]):
        durationinhoursgreaterthen (Union[Unset, float]):
        durationinhourslessthen (Union[Unset, float]):
        chargepoint_id (Union[Unset, str]):
        connector_number (Union[Unset, int]):
        roamingconnectionid (Union[Unset, str]):
        organizationunitcode (Union[Unset, str]):
        local_only (Union[Unset, bool]):
        order_by (Union[Unset, GetAllCdrsOrderBy]):  Default: GetAllCdrsOrderBy.STARTDATETIME.
        descending (Union[Unset, bool]):
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[List['CdrDto'], LongshipError]]
    """

    kwargs = _get_kwargs(
        skip=skip,
        take=take,
        search=search,
        providerexclude=providerexclude,
        tariff_id=tariff_id,
        idtag=idtag,
        authorizationreferenceid=authorizationreferenceid,
        providerid=providerid,
        pricegreaterthen=pricegreaterthen,
        pricelessthen=pricelessthen,
        kwhgreaterthen=kwhgreaterthen,
        kwhlessthen=kwhlessthen,
        durationinhoursgreaterthen=durationinhoursgreaterthen,
        durationinhourslessthen=durationinhourslessthen,
        chargepoint_id=chargepoint_id,
        connector_number=connector_number,
        roamingconnectionid=roamingconnectionid,
        organizationunitcode=organizationunitcode,
        local_only=local_only,
        order_by=order_by,
        descending=descending,
        from_=from_,
        to=to,
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
    providerexclude: Union[Unset, str] = UNSET,
    tariff_id: Union[Unset, str] = UNSET,
    idtag: Union[Unset, str] = UNSET,
    authorizationreferenceid: Union[Unset, str] = UNSET,
    providerid: Union[Unset, str] = UNSET,
    pricegreaterthen: Union[Unset, float] = UNSET,
    pricelessthen: Union[Unset, float] = UNSET,
    kwhgreaterthen: Union[Unset, float] = UNSET,
    kwhlessthen: Union[Unset, float] = UNSET,
    durationinhoursgreaterthen: Union[Unset, float] = UNSET,
    durationinhourslessthen: Union[Unset, float] = UNSET,
    chargepoint_id: Union[Unset, str] = UNSET,
    connector_number: Union[Unset, int] = UNSET,
    roamingconnectionid: Union[Unset, str] = UNSET,
    organizationunitcode: Union[Unset, str] = UNSET,
    local_only: Union[Unset, bool] = UNSET,
    order_by: Union[Unset, GetAllCdrsOrderBy] = GetAllCdrsOrderBy.STARTDATETIME,
    descending: Union[Unset, bool] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
) -> Optional[Union[List["CdrDto"], LongshipError]]:
    """Get a list of cdrs.

     Get a paged list of cdrs, taken the filters into account.

    Args:
        skip (Union[Unset, int]):
        take (Union[Unset, int]):
        search (Union[Unset, str]):
        providerexclude (Union[Unset, str]):
        tariff_id (Union[Unset, str]):
        idtag (Union[Unset, str]):
        authorizationreferenceid (Union[Unset, str]):
        providerid (Union[Unset, str]):
        pricegreaterthen (Union[Unset, float]):
        pricelessthen (Union[Unset, float]):
        kwhgreaterthen (Union[Unset, float]):
        kwhlessthen (Union[Unset, float]):
        durationinhoursgreaterthen (Union[Unset, float]):
        durationinhourslessthen (Union[Unset, float]):
        chargepoint_id (Union[Unset, str]):
        connector_number (Union[Unset, int]):
        roamingconnectionid (Union[Unset, str]):
        organizationunitcode (Union[Unset, str]):
        local_only (Union[Unset, bool]):
        order_by (Union[Unset, GetAllCdrsOrderBy]):  Default: GetAllCdrsOrderBy.STARTDATETIME.
        descending (Union[Unset, bool]):
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[List['CdrDto'], LongshipError]
    """

    return sync_detailed(
        client=client,
        skip=skip,
        take=take,
        search=search,
        providerexclude=providerexclude,
        tariff_id=tariff_id,
        idtag=idtag,
        authorizationreferenceid=authorizationreferenceid,
        providerid=providerid,
        pricegreaterthen=pricegreaterthen,
        pricelessthen=pricelessthen,
        kwhgreaterthen=kwhgreaterthen,
        kwhlessthen=kwhlessthen,
        durationinhoursgreaterthen=durationinhoursgreaterthen,
        durationinhourslessthen=durationinhourslessthen,
        chargepoint_id=chargepoint_id,
        connector_number=connector_number,
        roamingconnectionid=roamingconnectionid,
        organizationunitcode=organizationunitcode,
        local_only=local_only,
        order_by=order_by,
        descending=descending,
        from_=from_,
        to=to,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    skip: Union[Unset, int] = UNSET,
    take: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
    providerexclude: Union[Unset, str] = UNSET,
    tariff_id: Union[Unset, str] = UNSET,
    idtag: Union[Unset, str] = UNSET,
    authorizationreferenceid: Union[Unset, str] = UNSET,
    providerid: Union[Unset, str] = UNSET,
    pricegreaterthen: Union[Unset, float] = UNSET,
    pricelessthen: Union[Unset, float] = UNSET,
    kwhgreaterthen: Union[Unset, float] = UNSET,
    kwhlessthen: Union[Unset, float] = UNSET,
    durationinhoursgreaterthen: Union[Unset, float] = UNSET,
    durationinhourslessthen: Union[Unset, float] = UNSET,
    chargepoint_id: Union[Unset, str] = UNSET,
    connector_number: Union[Unset, int] = UNSET,
    roamingconnectionid: Union[Unset, str] = UNSET,
    organizationunitcode: Union[Unset, str] = UNSET,
    local_only: Union[Unset, bool] = UNSET,
    order_by: Union[Unset, GetAllCdrsOrderBy] = GetAllCdrsOrderBy.STARTDATETIME,
    descending: Union[Unset, bool] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
) -> Response[Union[List["CdrDto"], LongshipError]]:
    """Get a list of cdrs.

     Get a paged list of cdrs, taken the filters into account.

    Args:
        skip (Union[Unset, int]):
        take (Union[Unset, int]):
        search (Union[Unset, str]):
        providerexclude (Union[Unset, str]):
        tariff_id (Union[Unset, str]):
        idtag (Union[Unset, str]):
        authorizationreferenceid (Union[Unset, str]):
        providerid (Union[Unset, str]):
        pricegreaterthen (Union[Unset, float]):
        pricelessthen (Union[Unset, float]):
        kwhgreaterthen (Union[Unset, float]):
        kwhlessthen (Union[Unset, float]):
        durationinhoursgreaterthen (Union[Unset, float]):
        durationinhourslessthen (Union[Unset, float]):
        chargepoint_id (Union[Unset, str]):
        connector_number (Union[Unset, int]):
        roamingconnectionid (Union[Unset, str]):
        organizationunitcode (Union[Unset, str]):
        local_only (Union[Unset, bool]):
        order_by (Union[Unset, GetAllCdrsOrderBy]):  Default: GetAllCdrsOrderBy.STARTDATETIME.
        descending (Union[Unset, bool]):
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[List['CdrDto'], LongshipError]]
    """

    kwargs = _get_kwargs(
        skip=skip,
        take=take,
        search=search,
        providerexclude=providerexclude,
        tariff_id=tariff_id,
        idtag=idtag,
        authorizationreferenceid=authorizationreferenceid,
        providerid=providerid,
        pricegreaterthen=pricegreaterthen,
        pricelessthen=pricelessthen,
        kwhgreaterthen=kwhgreaterthen,
        kwhlessthen=kwhlessthen,
        durationinhoursgreaterthen=durationinhoursgreaterthen,
        durationinhourslessthen=durationinhourslessthen,
        chargepoint_id=chargepoint_id,
        connector_number=connector_number,
        roamingconnectionid=roamingconnectionid,
        organizationunitcode=organizationunitcode,
        local_only=local_only,
        order_by=order_by,
        descending=descending,
        from_=from_,
        to=to,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    skip: Union[Unset, int] = UNSET,
    take: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
    providerexclude: Union[Unset, str] = UNSET,
    tariff_id: Union[Unset, str] = UNSET,
    idtag: Union[Unset, str] = UNSET,
    authorizationreferenceid: Union[Unset, str] = UNSET,
    providerid: Union[Unset, str] = UNSET,
    pricegreaterthen: Union[Unset, float] = UNSET,
    pricelessthen: Union[Unset, float] = UNSET,
    kwhgreaterthen: Union[Unset, float] = UNSET,
    kwhlessthen: Union[Unset, float] = UNSET,
    durationinhoursgreaterthen: Union[Unset, float] = UNSET,
    durationinhourslessthen: Union[Unset, float] = UNSET,
    chargepoint_id: Union[Unset, str] = UNSET,
    connector_number: Union[Unset, int] = UNSET,
    roamingconnectionid: Union[Unset, str] = UNSET,
    organizationunitcode: Union[Unset, str] = UNSET,
    local_only: Union[Unset, bool] = UNSET,
    order_by: Union[Unset, GetAllCdrsOrderBy] = GetAllCdrsOrderBy.STARTDATETIME,
    descending: Union[Unset, bool] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
) -> Optional[Union[List["CdrDto"], LongshipError]]:
    """Get a list of cdrs.

     Get a paged list of cdrs, taken the filters into account.

    Args:
        skip (Union[Unset, int]):
        take (Union[Unset, int]):
        search (Union[Unset, str]):
        providerexclude (Union[Unset, str]):
        tariff_id (Union[Unset, str]):
        idtag (Union[Unset, str]):
        authorizationreferenceid (Union[Unset, str]):
        providerid (Union[Unset, str]):
        pricegreaterthen (Union[Unset, float]):
        pricelessthen (Union[Unset, float]):
        kwhgreaterthen (Union[Unset, float]):
        kwhlessthen (Union[Unset, float]):
        durationinhoursgreaterthen (Union[Unset, float]):
        durationinhourslessthen (Union[Unset, float]):
        chargepoint_id (Union[Unset, str]):
        connector_number (Union[Unset, int]):
        roamingconnectionid (Union[Unset, str]):
        organizationunitcode (Union[Unset, str]):
        local_only (Union[Unset, bool]):
        order_by (Union[Unset, GetAllCdrsOrderBy]):  Default: GetAllCdrsOrderBy.STARTDATETIME.
        descending (Union[Unset, bool]):
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[List['CdrDto'], LongshipError]
    """

    return (
        await asyncio_detailed(
            client=client,
            skip=skip,
            take=take,
            search=search,
            providerexclude=providerexclude,
            tariff_id=tariff_id,
            idtag=idtag,
            authorizationreferenceid=authorizationreferenceid,
            providerid=providerid,
            pricegreaterthen=pricegreaterthen,
            pricelessthen=pricelessthen,
            kwhgreaterthen=kwhgreaterthen,
            kwhlessthen=kwhlessthen,
            durationinhoursgreaterthen=durationinhoursgreaterthen,
            durationinhourslessthen=durationinhourslessthen,
            chargepoint_id=chargepoint_id,
            connector_number=connector_number,
            roamingconnectionid=roamingconnectionid,
            organizationunitcode=organizationunitcode,
            local_only=local_only,
            order_by=order_by,
            descending=descending,
            from_=from_,
            to=to,
        )
    ).parsed
