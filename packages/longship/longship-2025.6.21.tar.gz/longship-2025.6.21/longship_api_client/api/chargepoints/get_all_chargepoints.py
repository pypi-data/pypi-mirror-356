from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.get_all_chargepoints_operationalstatus import (
    GetAllChargepointsOperationalstatus,
)
from ...models.chargepoint_dto import ChargepointDto
from ...models.get_all_chargepoints_accesstype import GetAllChargepointsAccesstype
from ...models.get_all_chargepoints_chargerpowertype import (
    GetAllChargepointsChargerpowertype,
)
from ...types import Unset
from ...models.longship_error import LongshipError
from ...models.get_all_chargepoints_order_by import GetAllChargepointsOrderBy


def _get_kwargs(
    *,
    skip: Union[Unset, int] = UNSET,
    take: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
    is_online: Union[Unset, bool] = UNSET,
    tariff_id: Union[Unset, str] = UNSET,
    operationalstatus: Union[
        Unset, GetAllChargepointsOperationalstatus
    ] = GetAllChargepointsOperationalstatus.AVAILABLE,
    accesstype: Union[
        Unset, GetAllChargepointsAccesstype
    ] = GetAllChargepointsAccesstype.NEW,
    chargerpowertype: Union[
        Unset, GetAllChargepointsChargerpowertype
    ] = GetAllChargepointsChargerpowertype.AC,
    organizationunitcode: Union[Unset, str] = UNSET,
    inactiveonly: Union[Unset, bool] = UNSET,
    firmwareversion: Union[Unset, str] = UNSET,
    model: Union[Unset, str] = UNSET,
    vendor: Union[Unset, str] = UNSET,
    order_by: Union[Unset, GetAllChargepointsOrderBy] = GetAllChargepointsOrderBy.NAME,
    descending: Union[Unset, bool] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["skip"] = skip

    params["take"] = take

    params["search"] = search

    params["isOnline"] = is_online

    params["tariffId"] = tariff_id

    json_operationalstatus: Union[Unset, str] = UNSET
    if not isinstance(operationalstatus, Unset):
        json_operationalstatus = operationalstatus.value

    params["operationalstatus"] = json_operationalstatus

    json_accesstype: Union[Unset, str] = UNSET
    if not isinstance(accesstype, Unset):
        json_accesstype = accesstype.value

    params["accesstype"] = json_accesstype

    json_chargerpowertype: Union[Unset, str] = UNSET
    if not isinstance(chargerpowertype, Unset):
        json_chargerpowertype = chargerpowertype.value

    params["chargerpowertype"] = json_chargerpowertype

    params["organizationunitcode"] = organizationunitcode

    params["inactiveonly"] = inactiveonly

    params["firmwareversion"] = firmwareversion

    params["model"] = model

    params["vendor"] = vendor

    json_order_by: Union[Unset, str] = UNSET
    if not isinstance(order_by, Unset):
        json_order_by = order_by.value

    params["orderBy"] = json_order_by

    params["descending"] = descending

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/v1/chargepoints",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[List["ChargepointDto"], LongshipError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for componentsschemaschargepoint_dto_array_item_data in _response_200:
            componentsschemaschargepoint_dto_array_item = ChargepointDto.from_dict(
                componentsschemaschargepoint_dto_array_item_data
            )

            response_200.append(componentsschemaschargepoint_dto_array_item)

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
) -> Response[Union[List["ChargepointDto"], LongshipError]]:
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
    is_online: Union[Unset, bool] = UNSET,
    tariff_id: Union[Unset, str] = UNSET,
    operationalstatus: Union[
        Unset, GetAllChargepointsOperationalstatus
    ] = GetAllChargepointsOperationalstatus.AVAILABLE,
    accesstype: Union[
        Unset, GetAllChargepointsAccesstype
    ] = GetAllChargepointsAccesstype.NEW,
    chargerpowertype: Union[
        Unset, GetAllChargepointsChargerpowertype
    ] = GetAllChargepointsChargerpowertype.AC,
    organizationunitcode: Union[Unset, str] = UNSET,
    inactiveonly: Union[Unset, bool] = UNSET,
    firmwareversion: Union[Unset, str] = UNSET,
    model: Union[Unset, str] = UNSET,
    vendor: Union[Unset, str] = UNSET,
    order_by: Union[Unset, GetAllChargepointsOrderBy] = GetAllChargepointsOrderBy.NAME,
    descending: Union[Unset, bool] = UNSET,
) -> Response[Union[List["ChargepointDto"], LongshipError]]:
    """Get a list of chargepoints.

     Get a paged list of chargepoints, taken the filters into account.

    Args:
        skip (Union[Unset, int]):
        take (Union[Unset, int]):
        search (Union[Unset, str]):
        is_online (Union[Unset, bool]):
        tariff_id (Union[Unset, str]):
        operationalstatus (Union[Unset, GetAllChargepointsOperationalstatus]):  Default:
            GetAllChargepointsOperationalstatus.AVAILABLE.
        accesstype (Union[Unset, GetAllChargepointsAccesstype]):  Default:
            GetAllChargepointsAccesstype.NEW.
        chargerpowertype (Union[Unset, GetAllChargepointsChargerpowertype]):  Default:
            GetAllChargepointsChargerpowertype.AC.
        organizationunitcode (Union[Unset, str]):
        inactiveonly (Union[Unset, bool]):
        firmwareversion (Union[Unset, str]):
        model (Union[Unset, str]):
        vendor (Union[Unset, str]):
        order_by (Union[Unset, GetAllChargepointsOrderBy]):  Default:
            GetAllChargepointsOrderBy.NAME.
        descending (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[List['ChargepointDto'], LongshipError]]
    """

    kwargs = _get_kwargs(
        skip=skip,
        take=take,
        search=search,
        is_online=is_online,
        tariff_id=tariff_id,
        operationalstatus=operationalstatus,
        accesstype=accesstype,
        chargerpowertype=chargerpowertype,
        organizationunitcode=organizationunitcode,
        inactiveonly=inactiveonly,
        firmwareversion=firmwareversion,
        model=model,
        vendor=vendor,
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
    is_online: Union[Unset, bool] = UNSET,
    tariff_id: Union[Unset, str] = UNSET,
    operationalstatus: Union[
        Unset, GetAllChargepointsOperationalstatus
    ] = GetAllChargepointsOperationalstatus.AVAILABLE,
    accesstype: Union[
        Unset, GetAllChargepointsAccesstype
    ] = GetAllChargepointsAccesstype.NEW,
    chargerpowertype: Union[
        Unset, GetAllChargepointsChargerpowertype
    ] = GetAllChargepointsChargerpowertype.AC,
    organizationunitcode: Union[Unset, str] = UNSET,
    inactiveonly: Union[Unset, bool] = UNSET,
    firmwareversion: Union[Unset, str] = UNSET,
    model: Union[Unset, str] = UNSET,
    vendor: Union[Unset, str] = UNSET,
    order_by: Union[Unset, GetAllChargepointsOrderBy] = GetAllChargepointsOrderBy.NAME,
    descending: Union[Unset, bool] = UNSET,
) -> Optional[Union[List["ChargepointDto"], LongshipError]]:
    """Get a list of chargepoints.

     Get a paged list of chargepoints, taken the filters into account.

    Args:
        skip (Union[Unset, int]):
        take (Union[Unset, int]):
        search (Union[Unset, str]):
        is_online (Union[Unset, bool]):
        tariff_id (Union[Unset, str]):
        operationalstatus (Union[Unset, GetAllChargepointsOperationalstatus]):  Default:
            GetAllChargepointsOperationalstatus.AVAILABLE.
        accesstype (Union[Unset, GetAllChargepointsAccesstype]):  Default:
            GetAllChargepointsAccesstype.NEW.
        chargerpowertype (Union[Unset, GetAllChargepointsChargerpowertype]):  Default:
            GetAllChargepointsChargerpowertype.AC.
        organizationunitcode (Union[Unset, str]):
        inactiveonly (Union[Unset, bool]):
        firmwareversion (Union[Unset, str]):
        model (Union[Unset, str]):
        vendor (Union[Unset, str]):
        order_by (Union[Unset, GetAllChargepointsOrderBy]):  Default:
            GetAllChargepointsOrderBy.NAME.
        descending (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[List['ChargepointDto'], LongshipError]
    """

    return sync_detailed(
        client=client,
        skip=skip,
        take=take,
        search=search,
        is_online=is_online,
        tariff_id=tariff_id,
        operationalstatus=operationalstatus,
        accesstype=accesstype,
        chargerpowertype=chargerpowertype,
        organizationunitcode=organizationunitcode,
        inactiveonly=inactiveonly,
        firmwareversion=firmwareversion,
        model=model,
        vendor=vendor,
        order_by=order_by,
        descending=descending,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    skip: Union[Unset, int] = UNSET,
    take: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
    is_online: Union[Unset, bool] = UNSET,
    tariff_id: Union[Unset, str] = UNSET,
    operationalstatus: Union[
        Unset, GetAllChargepointsOperationalstatus
    ] = GetAllChargepointsOperationalstatus.AVAILABLE,
    accesstype: Union[
        Unset, GetAllChargepointsAccesstype
    ] = GetAllChargepointsAccesstype.NEW,
    chargerpowertype: Union[
        Unset, GetAllChargepointsChargerpowertype
    ] = GetAllChargepointsChargerpowertype.AC,
    organizationunitcode: Union[Unset, str] = UNSET,
    inactiveonly: Union[Unset, bool] = UNSET,
    firmwareversion: Union[Unset, str] = UNSET,
    model: Union[Unset, str] = UNSET,
    vendor: Union[Unset, str] = UNSET,
    order_by: Union[Unset, GetAllChargepointsOrderBy] = GetAllChargepointsOrderBy.NAME,
    descending: Union[Unset, bool] = UNSET,
) -> Response[Union[List["ChargepointDto"], LongshipError]]:
    """Get a list of chargepoints.

     Get a paged list of chargepoints, taken the filters into account.

    Args:
        skip (Union[Unset, int]):
        take (Union[Unset, int]):
        search (Union[Unset, str]):
        is_online (Union[Unset, bool]):
        tariff_id (Union[Unset, str]):
        operationalstatus (Union[Unset, GetAllChargepointsOperationalstatus]):  Default:
            GetAllChargepointsOperationalstatus.AVAILABLE.
        accesstype (Union[Unset, GetAllChargepointsAccesstype]):  Default:
            GetAllChargepointsAccesstype.NEW.
        chargerpowertype (Union[Unset, GetAllChargepointsChargerpowertype]):  Default:
            GetAllChargepointsChargerpowertype.AC.
        organizationunitcode (Union[Unset, str]):
        inactiveonly (Union[Unset, bool]):
        firmwareversion (Union[Unset, str]):
        model (Union[Unset, str]):
        vendor (Union[Unset, str]):
        order_by (Union[Unset, GetAllChargepointsOrderBy]):  Default:
            GetAllChargepointsOrderBy.NAME.
        descending (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[List['ChargepointDto'], LongshipError]]
    """

    kwargs = _get_kwargs(
        skip=skip,
        take=take,
        search=search,
        is_online=is_online,
        tariff_id=tariff_id,
        operationalstatus=operationalstatus,
        accesstype=accesstype,
        chargerpowertype=chargerpowertype,
        organizationunitcode=organizationunitcode,
        inactiveonly=inactiveonly,
        firmwareversion=firmwareversion,
        model=model,
        vendor=vendor,
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
    is_online: Union[Unset, bool] = UNSET,
    tariff_id: Union[Unset, str] = UNSET,
    operationalstatus: Union[
        Unset, GetAllChargepointsOperationalstatus
    ] = GetAllChargepointsOperationalstatus.AVAILABLE,
    accesstype: Union[
        Unset, GetAllChargepointsAccesstype
    ] = GetAllChargepointsAccesstype.NEW,
    chargerpowertype: Union[
        Unset, GetAllChargepointsChargerpowertype
    ] = GetAllChargepointsChargerpowertype.AC,
    organizationunitcode: Union[Unset, str] = UNSET,
    inactiveonly: Union[Unset, bool] = UNSET,
    firmwareversion: Union[Unset, str] = UNSET,
    model: Union[Unset, str] = UNSET,
    vendor: Union[Unset, str] = UNSET,
    order_by: Union[Unset, GetAllChargepointsOrderBy] = GetAllChargepointsOrderBy.NAME,
    descending: Union[Unset, bool] = UNSET,
) -> Optional[Union[List["ChargepointDto"], LongshipError]]:
    """Get a list of chargepoints.

     Get a paged list of chargepoints, taken the filters into account.

    Args:
        skip (Union[Unset, int]):
        take (Union[Unset, int]):
        search (Union[Unset, str]):
        is_online (Union[Unset, bool]):
        tariff_id (Union[Unset, str]):
        operationalstatus (Union[Unset, GetAllChargepointsOperationalstatus]):  Default:
            GetAllChargepointsOperationalstatus.AVAILABLE.
        accesstype (Union[Unset, GetAllChargepointsAccesstype]):  Default:
            GetAllChargepointsAccesstype.NEW.
        chargerpowertype (Union[Unset, GetAllChargepointsChargerpowertype]):  Default:
            GetAllChargepointsChargerpowertype.AC.
        organizationunitcode (Union[Unset, str]):
        inactiveonly (Union[Unset, bool]):
        firmwareversion (Union[Unset, str]):
        model (Union[Unset, str]):
        vendor (Union[Unset, str]):
        order_by (Union[Unset, GetAllChargepointsOrderBy]):  Default:
            GetAllChargepointsOrderBy.NAME.
        descending (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[List['ChargepointDto'], LongshipError]
    """

    return (
        await asyncio_detailed(
            client=client,
            skip=skip,
            take=take,
            search=search,
            is_online=is_online,
            tariff_id=tariff_id,
            operationalstatus=operationalstatus,
            accesstype=accesstype,
            chargerpowertype=chargerpowertype,
            organizationunitcode=organizationunitcode,
            inactiveonly=inactiveonly,
            firmwareversion=firmwareversion,
            model=model,
            vendor=vendor,
            order_by=order_by,
            descending=descending,
        )
    ).parsed
