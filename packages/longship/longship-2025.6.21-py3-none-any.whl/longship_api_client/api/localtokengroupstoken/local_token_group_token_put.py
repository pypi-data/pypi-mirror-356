from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.local_token_group_token_put_dto import LocalTokenGroupTokenPutDto
from ...models.longship_error import LongshipError


def _get_kwargs(
    id: str,
    token_uid: str,
    *,
    body: LocalTokenGroupTokenPutDto,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "put",
        "url": "/v1/localtokengroups/{id}/token/{token_uid}".format(
            id=id,
            token_uid=token_uid,
        ),
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, LongshipError]]:
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = LongshipError.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = LongshipError.from_dict(response.json())

        return response_422
    if response.status_code == HTTPStatus.CONFLICT:
        response_409 = LongshipError.from_dict(response.json())

        return response_409
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = LongshipError.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = LongshipError.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = LongshipError.from_dict(response.json())

        return response_500
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = LongshipError.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.ACCEPTED:
        response_202 = cast(Any, None)
        return response_202
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, LongshipError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    token_uid: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: LocalTokenGroupTokenPutDto,
) -> Response[Union[Any, LongshipError]]:
    """Updates a localtokengrouptoken.

     Updates a localtokengrouptoken.

    Args:
        id (str):
        token_uid (str):
        body (LocalTokenGroupTokenPutDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, LongshipError]]
    """

    kwargs = _get_kwargs(
        id=id,
        token_uid=token_uid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    token_uid: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: LocalTokenGroupTokenPutDto,
) -> Optional[Union[Any, LongshipError]]:
    """Updates a localtokengrouptoken.

     Updates a localtokengrouptoken.

    Args:
        id (str):
        token_uid (str):
        body (LocalTokenGroupTokenPutDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, LongshipError]
    """

    return sync_detailed(
        id=id,
        token_uid=token_uid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    id: str,
    token_uid: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: LocalTokenGroupTokenPutDto,
) -> Response[Union[Any, LongshipError]]:
    """Updates a localtokengrouptoken.

     Updates a localtokengrouptoken.

    Args:
        id (str):
        token_uid (str):
        body (LocalTokenGroupTokenPutDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, LongshipError]]
    """

    kwargs = _get_kwargs(
        id=id,
        token_uid=token_uid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    token_uid: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: LocalTokenGroupTokenPutDto,
) -> Optional[Union[Any, LongshipError]]:
    """Updates a localtokengrouptoken.

     Updates a localtokengrouptoken.

    Args:
        id (str):
        token_uid (str):
        body (LocalTokenGroupTokenPutDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, LongshipError]
    """

    return (
        await asyncio_detailed(
            id=id,
            token_uid=token_uid,
            client=client,
            body=body,
        )
    ).parsed
