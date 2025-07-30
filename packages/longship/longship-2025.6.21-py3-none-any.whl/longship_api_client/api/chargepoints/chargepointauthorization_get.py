from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.charge_point_authorize_get_dto import ChargePointAuthorizeGetDto
from ...models.longship_error import LongshipError


def _get_kwargs(
    id: str,
    authorization_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/v1/chargepoints/{id}/authorization/{authorization_id}".format(
            id=id,
            authorization_id=authorization_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ChargePointAuthorizeGetDto, LongshipError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ChargePointAuthorizeGetDto.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = LongshipError.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = LongshipError.from_dict(response.json())

        return response_500
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = LongshipError.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = LongshipError.from_dict(response.json())

        return response_403
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ChargePointAuthorizeGetDto, LongshipError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    authorization_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[ChargePointAuthorizeGetDto, LongshipError]]:
    """Gets the chargepointauthorization.

     Gets the chargepointauthorization base on the id.

    Args:
        id (str):
        authorization_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ChargePointAuthorizeGetDto, LongshipError]]
    """

    kwargs = _get_kwargs(
        id=id,
        authorization_id=authorization_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    authorization_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[ChargePointAuthorizeGetDto, LongshipError]]:
    """Gets the chargepointauthorization.

     Gets the chargepointauthorization base on the id.

    Args:
        id (str):
        authorization_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ChargePointAuthorizeGetDto, LongshipError]
    """

    return sync_detailed(
        id=id,
        authorization_id=authorization_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: str,
    authorization_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[ChargePointAuthorizeGetDto, LongshipError]]:
    """Gets the chargepointauthorization.

     Gets the chargepointauthorization base on the id.

    Args:
        id (str):
        authorization_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ChargePointAuthorizeGetDto, LongshipError]]
    """

    kwargs = _get_kwargs(
        id=id,
        authorization_id=authorization_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    authorization_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[ChargePointAuthorizeGetDto, LongshipError]]:
    """Gets the chargepointauthorization.

     Gets the chargepointauthorization base on the id.

    Args:
        id (str):
        authorization_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ChargePointAuthorizeGetDto, LongshipError]
    """

    return (
        await asyncio_detailed(
            id=id,
            authorization_id=authorization_id,
            client=client,
        )
    ).parsed
