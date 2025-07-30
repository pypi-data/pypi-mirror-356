from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.message_log_dto import MessageLogDto
from ...types import Unset
import datetime
from ...models.longship_error import LongshipError


def _get_kwargs(
    id: str,
    *,
    skip: Union[Unset, int] = UNSET,
    take: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    transaction_id: Union[Unset, str] = UNSET,
    response_only: Union[Unset, bool] = UNSET,
    request_only: Union[Unset, bool] = UNSET,
    charger_to_cpo_only: Union[Unset, bool] = UNSET,
    cpo_to_charger_only: Union[Unset, bool] = UNSET,
    message_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["skip"] = skip

    params["take"] = take

    params["search"] = search

    json_from_: Union[Unset, str] = UNSET
    if not isinstance(from_, Unset):
        json_from_ = from_.isoformat()
    params["from"] = json_from_

    json_to: Union[Unset, str] = UNSET
    if not isinstance(to, Unset):
        json_to = to.isoformat()
    params["to"] = json_to

    params["transactionId"] = transaction_id

    params["responseOnly"] = response_only

    params["requestOnly"] = request_only

    params["chargerToCpoOnly"] = charger_to_cpo_only

    params["cpoToChargerOnly"] = cpo_to_charger_only

    params["messageId"] = message_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/v1/chargepoints/{id}/messages".format(
            id=id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[List["MessageLogDto"], LongshipError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for componentsschemasmessage_log_dto_array_item_data in _response_200:
            componentsschemasmessage_log_dto_array_item = MessageLogDto.from_dict(
                componentsschemasmessage_log_dto_array_item_data
            )

            response_200.append(componentsschemasmessage_log_dto_array_item)

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
) -> Response[Union[List["MessageLogDto"], LongshipError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    skip: Union[Unset, int] = UNSET,
    take: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    transaction_id: Union[Unset, str] = UNSET,
    response_only: Union[Unset, bool] = UNSET,
    request_only: Union[Unset, bool] = UNSET,
    charger_to_cpo_only: Union[Unset, bool] = UNSET,
    cpo_to_charger_only: Union[Unset, bool] = UNSET,
    message_id: Union[Unset, str] = UNSET,
) -> Response[Union[List["MessageLogDto"], LongshipError]]:
    """Get a list of chargepointmessages.

     Get a paged list of chargepointmessages, taken the filters into account.

    Args:
        id (str):
        skip (Union[Unset, int]):
        take (Union[Unset, int]):
        search (Union[Unset, str]):
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):
        transaction_id (Union[Unset, str]):
        response_only (Union[Unset, bool]):
        request_only (Union[Unset, bool]):
        charger_to_cpo_only (Union[Unset, bool]):
        cpo_to_charger_only (Union[Unset, bool]):
        message_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[List['MessageLogDto'], LongshipError]]
    """

    kwargs = _get_kwargs(
        id=id,
        skip=skip,
        take=take,
        search=search,
        from_=from_,
        to=to,
        transaction_id=transaction_id,
        response_only=response_only,
        request_only=request_only,
        charger_to_cpo_only=charger_to_cpo_only,
        cpo_to_charger_only=cpo_to_charger_only,
        message_id=message_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    skip: Union[Unset, int] = UNSET,
    take: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    transaction_id: Union[Unset, str] = UNSET,
    response_only: Union[Unset, bool] = UNSET,
    request_only: Union[Unset, bool] = UNSET,
    charger_to_cpo_only: Union[Unset, bool] = UNSET,
    cpo_to_charger_only: Union[Unset, bool] = UNSET,
    message_id: Union[Unset, str] = UNSET,
) -> Optional[Union[List["MessageLogDto"], LongshipError]]:
    """Get a list of chargepointmessages.

     Get a paged list of chargepointmessages, taken the filters into account.

    Args:
        id (str):
        skip (Union[Unset, int]):
        take (Union[Unset, int]):
        search (Union[Unset, str]):
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):
        transaction_id (Union[Unset, str]):
        response_only (Union[Unset, bool]):
        request_only (Union[Unset, bool]):
        charger_to_cpo_only (Union[Unset, bool]):
        cpo_to_charger_only (Union[Unset, bool]):
        message_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[List['MessageLogDto'], LongshipError]
    """

    return sync_detailed(
        id=id,
        client=client,
        skip=skip,
        take=take,
        search=search,
        from_=from_,
        to=to,
        transaction_id=transaction_id,
        response_only=response_only,
        request_only=request_only,
        charger_to_cpo_only=charger_to_cpo_only,
        cpo_to_charger_only=cpo_to_charger_only,
        message_id=message_id,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    skip: Union[Unset, int] = UNSET,
    take: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    transaction_id: Union[Unset, str] = UNSET,
    response_only: Union[Unset, bool] = UNSET,
    request_only: Union[Unset, bool] = UNSET,
    charger_to_cpo_only: Union[Unset, bool] = UNSET,
    cpo_to_charger_only: Union[Unset, bool] = UNSET,
    message_id: Union[Unset, str] = UNSET,
) -> Response[Union[List["MessageLogDto"], LongshipError]]:
    """Get a list of chargepointmessages.

     Get a paged list of chargepointmessages, taken the filters into account.

    Args:
        id (str):
        skip (Union[Unset, int]):
        take (Union[Unset, int]):
        search (Union[Unset, str]):
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):
        transaction_id (Union[Unset, str]):
        response_only (Union[Unset, bool]):
        request_only (Union[Unset, bool]):
        charger_to_cpo_only (Union[Unset, bool]):
        cpo_to_charger_only (Union[Unset, bool]):
        message_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[List['MessageLogDto'], LongshipError]]
    """

    kwargs = _get_kwargs(
        id=id,
        skip=skip,
        take=take,
        search=search,
        from_=from_,
        to=to,
        transaction_id=transaction_id,
        response_only=response_only,
        request_only=request_only,
        charger_to_cpo_only=charger_to_cpo_only,
        cpo_to_charger_only=cpo_to_charger_only,
        message_id=message_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    skip: Union[Unset, int] = UNSET,
    take: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
    transaction_id: Union[Unset, str] = UNSET,
    response_only: Union[Unset, bool] = UNSET,
    request_only: Union[Unset, bool] = UNSET,
    charger_to_cpo_only: Union[Unset, bool] = UNSET,
    cpo_to_charger_only: Union[Unset, bool] = UNSET,
    message_id: Union[Unset, str] = UNSET,
) -> Optional[Union[List["MessageLogDto"], LongshipError]]:
    """Get a list of chargepointmessages.

     Get a paged list of chargepointmessages, taken the filters into account.

    Args:
        id (str):
        skip (Union[Unset, int]):
        take (Union[Unset, int]):
        search (Union[Unset, str]):
        from_ (Union[Unset, datetime.datetime]):
        to (Union[Unset, datetime.datetime]):
        transaction_id (Union[Unset, str]):
        response_only (Union[Unset, bool]):
        request_only (Union[Unset, bool]):
        charger_to_cpo_only (Union[Unset, bool]):
        cpo_to_charger_only (Union[Unset, bool]):
        message_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[List['MessageLogDto'], LongshipError]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            skip=skip,
            take=take,
            search=search,
            from_=from_,
            to=to,
            transaction_id=transaction_id,
            response_only=response_only,
            request_only=request_only,
            charger_to_cpo_only=charger_to_cpo_only,
            cpo_to_charger_only=cpo_to_charger_only,
            message_id=message_id,
        )
    ).parsed
