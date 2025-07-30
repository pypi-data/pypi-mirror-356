from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.get_all_locations_accesstype import GetAllLocationsAccesstype
from ...models.get_all_locations_chargerpowertype import GetAllLocationsChargerpowertype
from ...models.get_all_locations_order_by import GetAllLocationsOrderBy
from ...types import Unset
from ...models.longship_error import LongshipError
from ...models.location_dto import LocationDto


def _get_kwargs(
    *,
    skip: Union[Unset, int] = UNSET,
    take: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
    organizationunitcode: Union[Unset, str] = UNSET,
    accesstype: Union[
        Unset, GetAllLocationsAccesstype
    ] = GetAllLocationsAccesstype.PUBLIC,
    chargerpowertype: Union[
        Unset, GetAllLocationsChargerpowertype
    ] = GetAllLocationsChargerpowertype.AC,
    order_by: Union[Unset, GetAllLocationsOrderBy] = GetAllLocationsOrderBy.NAME,
    descending: Union[Unset, bool] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["skip"] = skip

    params["take"] = take

    params["search"] = search

    params["organizationunitcode"] = organizationunitcode

    json_accesstype: Union[Unset, str] = UNSET
    if not isinstance(accesstype, Unset):
        json_accesstype = accesstype.value

    params["accesstype"] = json_accesstype

    json_chargerpowertype: Union[Unset, str] = UNSET
    if not isinstance(chargerpowertype, Unset):
        json_chargerpowertype = chargerpowertype.value

    params["chargerpowertype"] = json_chargerpowertype

    json_order_by: Union[Unset, str] = UNSET
    if not isinstance(order_by, Unset):
        json_order_by = order_by.value

    params["orderBy"] = json_order_by

    params["descending"] = descending

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/v1/locations",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[List["LocationDto"], LongshipError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for componentsschemaslocation_dto_array_item_data in _response_200:
            componentsschemaslocation_dto_array_item = LocationDto.from_dict(
                componentsschemaslocation_dto_array_item_data
            )

            response_200.append(componentsschemaslocation_dto_array_item)

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
) -> Response[Union[List["LocationDto"], LongshipError]]:
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
    organizationunitcode: Union[Unset, str] = UNSET,
    accesstype: Union[
        Unset, GetAllLocationsAccesstype
    ] = GetAllLocationsAccesstype.PUBLIC,
    chargerpowertype: Union[
        Unset, GetAllLocationsChargerpowertype
    ] = GetAllLocationsChargerpowertype.AC,
    order_by: Union[Unset, GetAllLocationsOrderBy] = GetAllLocationsOrderBy.NAME,
    descending: Union[Unset, bool] = UNSET,
) -> Response[Union[List["LocationDto"], LongshipError]]:
    """Get a list of locations.

     Get a paged list of locations, taken the filters into account.

    Args:
        skip (Union[Unset, int]):
        take (Union[Unset, int]):
        search (Union[Unset, str]):
        organizationunitcode (Union[Unset, str]):
        accesstype (Union[Unset, GetAllLocationsAccesstype]):  Default:
            GetAllLocationsAccesstype.PUBLIC.
        chargerpowertype (Union[Unset, GetAllLocationsChargerpowertype]):  Default:
            GetAllLocationsChargerpowertype.AC.
        order_by (Union[Unset, GetAllLocationsOrderBy]):  Default: GetAllLocationsOrderBy.NAME.
        descending (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[List['LocationDto'], LongshipError]]
    """

    kwargs = _get_kwargs(
        skip=skip,
        take=take,
        search=search,
        organizationunitcode=organizationunitcode,
        accesstype=accesstype,
        chargerpowertype=chargerpowertype,
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
    organizationunitcode: Union[Unset, str] = UNSET,
    accesstype: Union[
        Unset, GetAllLocationsAccesstype
    ] = GetAllLocationsAccesstype.PUBLIC,
    chargerpowertype: Union[
        Unset, GetAllLocationsChargerpowertype
    ] = GetAllLocationsChargerpowertype.AC,
    order_by: Union[Unset, GetAllLocationsOrderBy] = GetAllLocationsOrderBy.NAME,
    descending: Union[Unset, bool] = UNSET,
) -> Optional[Union[List["LocationDto"], LongshipError]]:
    """Get a list of locations.

     Get a paged list of locations, taken the filters into account.

    Args:
        skip (Union[Unset, int]):
        take (Union[Unset, int]):
        search (Union[Unset, str]):
        organizationunitcode (Union[Unset, str]):
        accesstype (Union[Unset, GetAllLocationsAccesstype]):  Default:
            GetAllLocationsAccesstype.PUBLIC.
        chargerpowertype (Union[Unset, GetAllLocationsChargerpowertype]):  Default:
            GetAllLocationsChargerpowertype.AC.
        order_by (Union[Unset, GetAllLocationsOrderBy]):  Default: GetAllLocationsOrderBy.NAME.
        descending (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[List['LocationDto'], LongshipError]
    """

    return sync_detailed(
        client=client,
        skip=skip,
        take=take,
        search=search,
        organizationunitcode=organizationunitcode,
        accesstype=accesstype,
        chargerpowertype=chargerpowertype,
        order_by=order_by,
        descending=descending,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    skip: Union[Unset, int] = UNSET,
    take: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
    organizationunitcode: Union[Unset, str] = UNSET,
    accesstype: Union[
        Unset, GetAllLocationsAccesstype
    ] = GetAllLocationsAccesstype.PUBLIC,
    chargerpowertype: Union[
        Unset, GetAllLocationsChargerpowertype
    ] = GetAllLocationsChargerpowertype.AC,
    order_by: Union[Unset, GetAllLocationsOrderBy] = GetAllLocationsOrderBy.NAME,
    descending: Union[Unset, bool] = UNSET,
) -> Response[Union[List["LocationDto"], LongshipError]]:
    """Get a list of locations.

     Get a paged list of locations, taken the filters into account.

    Args:
        skip (Union[Unset, int]):
        take (Union[Unset, int]):
        search (Union[Unset, str]):
        organizationunitcode (Union[Unset, str]):
        accesstype (Union[Unset, GetAllLocationsAccesstype]):  Default:
            GetAllLocationsAccesstype.PUBLIC.
        chargerpowertype (Union[Unset, GetAllLocationsChargerpowertype]):  Default:
            GetAllLocationsChargerpowertype.AC.
        order_by (Union[Unset, GetAllLocationsOrderBy]):  Default: GetAllLocationsOrderBy.NAME.
        descending (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[List['LocationDto'], LongshipError]]
    """

    kwargs = _get_kwargs(
        skip=skip,
        take=take,
        search=search,
        organizationunitcode=organizationunitcode,
        accesstype=accesstype,
        chargerpowertype=chargerpowertype,
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
    organizationunitcode: Union[Unset, str] = UNSET,
    accesstype: Union[
        Unset, GetAllLocationsAccesstype
    ] = GetAllLocationsAccesstype.PUBLIC,
    chargerpowertype: Union[
        Unset, GetAllLocationsChargerpowertype
    ] = GetAllLocationsChargerpowertype.AC,
    order_by: Union[Unset, GetAllLocationsOrderBy] = GetAllLocationsOrderBy.NAME,
    descending: Union[Unset, bool] = UNSET,
) -> Optional[Union[List["LocationDto"], LongshipError]]:
    """Get a list of locations.

     Get a paged list of locations, taken the filters into account.

    Args:
        skip (Union[Unset, int]):
        take (Union[Unset, int]):
        search (Union[Unset, str]):
        organizationunitcode (Union[Unset, str]):
        accesstype (Union[Unset, GetAllLocationsAccesstype]):  Default:
            GetAllLocationsAccesstype.PUBLIC.
        chargerpowertype (Union[Unset, GetAllLocationsChargerpowertype]):  Default:
            GetAllLocationsChargerpowertype.AC.
        order_by (Union[Unset, GetAllLocationsOrderBy]):  Default: GetAllLocationsOrderBy.NAME.
        descending (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[List['LocationDto'], LongshipError]
    """

    return (
        await asyncio_detailed(
            client=client,
            skip=skip,
            take=take,
            search=search,
            organizationunitcode=organizationunitcode,
            accesstype=accesstype,
            chargerpowertype=chargerpowertype,
            order_by=order_by,
            descending=descending,
        )
    ).parsed
