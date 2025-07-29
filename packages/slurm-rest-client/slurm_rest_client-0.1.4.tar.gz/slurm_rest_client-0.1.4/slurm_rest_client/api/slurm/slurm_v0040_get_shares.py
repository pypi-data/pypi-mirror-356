from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.v0040_openapi_shares_resp import V0040OpenapiSharesResp
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    accounts: Union[Unset, str] = UNSET,
    users: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["accounts"] = accounts

    params["users"] = users

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/slurm/v0.0.40/shares",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[V0040OpenapiSharesResp]:
    if response.status_code == 200:
        response_200 = V0040OpenapiSharesResp.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[V0040OpenapiSharesResp]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    accounts: Union[Unset, str] = UNSET,
    users: Union[Unset, str] = UNSET,
) -> Response[V0040OpenapiSharesResp]:
    """get fairshare info

    Args:
        accounts (Union[Unset, str]):
        users (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V0040OpenapiSharesResp]
    """

    kwargs = _get_kwargs(
        accounts=accounts,
        users=users,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    accounts: Union[Unset, str] = UNSET,
    users: Union[Unset, str] = UNSET,
) -> Optional[V0040OpenapiSharesResp]:
    """get fairshare info

    Args:
        accounts (Union[Unset, str]):
        users (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V0040OpenapiSharesResp
    """

    return sync_detailed(
        client=client,
        accounts=accounts,
        users=users,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    accounts: Union[Unset, str] = UNSET,
    users: Union[Unset, str] = UNSET,
) -> Response[V0040OpenapiSharesResp]:
    """get fairshare info

    Args:
        accounts (Union[Unset, str]):
        users (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V0040OpenapiSharesResp]
    """

    kwargs = _get_kwargs(
        accounts=accounts,
        users=users,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    accounts: Union[Unset, str] = UNSET,
    users: Union[Unset, str] = UNSET,
) -> Optional[V0040OpenapiSharesResp]:
    """get fairshare info

    Args:
        accounts (Union[Unset, str]):
        users (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V0040OpenapiSharesResp
    """

    return (
        await asyncio_detailed(
            client=client,
            accounts=accounts,
            users=users,
        )
    ).parsed
