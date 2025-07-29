from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.slurmdb_v0040_get_wckeys_response_200 import SlurmdbV0040GetWckeysResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    cluster: Union[Unset, str] = UNSET,
    format_: Union[Unset, str] = UNSET,
    id: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    only_defaults: Union[Unset, str] = UNSET,
    usage_end: Union[Unset, str] = UNSET,
    usage_start: Union[Unset, str] = UNSET,
    user: Union[Unset, str] = UNSET,
    with_usage: Union[Unset, str] = UNSET,
    with_deleted: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["cluster"] = cluster

    params["format"] = format_

    params["id"] = id

    params["name"] = name

    params["only_defaults"] = only_defaults

    params["usage_end"] = usage_end

    params["usage_start"] = usage_start

    params["user"] = user

    params["with_usage"] = with_usage

    params["with_deleted"] = with_deleted

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/slurmdb/v0.0.40/wckeys",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[SlurmdbV0040GetWckeysResponse200]:
    if response.status_code == 200:
        response_200 = SlurmdbV0040GetWckeysResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[SlurmdbV0040GetWckeysResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    cluster: Union[Unset, str] = UNSET,
    format_: Union[Unset, str] = UNSET,
    id: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    only_defaults: Union[Unset, str] = UNSET,
    usage_end: Union[Unset, str] = UNSET,
    usage_start: Union[Unset, str] = UNSET,
    user: Union[Unset, str] = UNSET,
    with_usage: Union[Unset, str] = UNSET,
    with_deleted: Union[Unset, str] = UNSET,
) -> Response[SlurmdbV0040GetWckeysResponse200]:
    """Get wckey list

    Args:
        cluster (Union[Unset, str]):
        format_ (Union[Unset, str]):
        id (Union[Unset, str]):
        name (Union[Unset, str]):
        only_defaults (Union[Unset, str]):
        usage_end (Union[Unset, str]):
        usage_start (Union[Unset, str]):
        user (Union[Unset, str]):
        with_usage (Union[Unset, str]):
        with_deleted (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SlurmdbV0040GetWckeysResponse200]
    """

    kwargs = _get_kwargs(
        cluster=cluster,
        format_=format_,
        id=id,
        name=name,
        only_defaults=only_defaults,
        usage_end=usage_end,
        usage_start=usage_start,
        user=user,
        with_usage=with_usage,
        with_deleted=with_deleted,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    cluster: Union[Unset, str] = UNSET,
    format_: Union[Unset, str] = UNSET,
    id: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    only_defaults: Union[Unset, str] = UNSET,
    usage_end: Union[Unset, str] = UNSET,
    usage_start: Union[Unset, str] = UNSET,
    user: Union[Unset, str] = UNSET,
    with_usage: Union[Unset, str] = UNSET,
    with_deleted: Union[Unset, str] = UNSET,
) -> Optional[SlurmdbV0040GetWckeysResponse200]:
    """Get wckey list

    Args:
        cluster (Union[Unset, str]):
        format_ (Union[Unset, str]):
        id (Union[Unset, str]):
        name (Union[Unset, str]):
        only_defaults (Union[Unset, str]):
        usage_end (Union[Unset, str]):
        usage_start (Union[Unset, str]):
        user (Union[Unset, str]):
        with_usage (Union[Unset, str]):
        with_deleted (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SlurmdbV0040GetWckeysResponse200
    """

    return sync_detailed(
        client=client,
        cluster=cluster,
        format_=format_,
        id=id,
        name=name,
        only_defaults=only_defaults,
        usage_end=usage_end,
        usage_start=usage_start,
        user=user,
        with_usage=with_usage,
        with_deleted=with_deleted,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    cluster: Union[Unset, str] = UNSET,
    format_: Union[Unset, str] = UNSET,
    id: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    only_defaults: Union[Unset, str] = UNSET,
    usage_end: Union[Unset, str] = UNSET,
    usage_start: Union[Unset, str] = UNSET,
    user: Union[Unset, str] = UNSET,
    with_usage: Union[Unset, str] = UNSET,
    with_deleted: Union[Unset, str] = UNSET,
) -> Response[SlurmdbV0040GetWckeysResponse200]:
    """Get wckey list

    Args:
        cluster (Union[Unset, str]):
        format_ (Union[Unset, str]):
        id (Union[Unset, str]):
        name (Union[Unset, str]):
        only_defaults (Union[Unset, str]):
        usage_end (Union[Unset, str]):
        usage_start (Union[Unset, str]):
        user (Union[Unset, str]):
        with_usage (Union[Unset, str]):
        with_deleted (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SlurmdbV0040GetWckeysResponse200]
    """

    kwargs = _get_kwargs(
        cluster=cluster,
        format_=format_,
        id=id,
        name=name,
        only_defaults=only_defaults,
        usage_end=usage_end,
        usage_start=usage_start,
        user=user,
        with_usage=with_usage,
        with_deleted=with_deleted,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    cluster: Union[Unset, str] = UNSET,
    format_: Union[Unset, str] = UNSET,
    id: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    only_defaults: Union[Unset, str] = UNSET,
    usage_end: Union[Unset, str] = UNSET,
    usage_start: Union[Unset, str] = UNSET,
    user: Union[Unset, str] = UNSET,
    with_usage: Union[Unset, str] = UNSET,
    with_deleted: Union[Unset, str] = UNSET,
) -> Optional[SlurmdbV0040GetWckeysResponse200]:
    """Get wckey list

    Args:
        cluster (Union[Unset, str]):
        format_ (Union[Unset, str]):
        id (Union[Unset, str]):
        name (Union[Unset, str]):
        only_defaults (Union[Unset, str]):
        usage_end (Union[Unset, str]):
        usage_start (Union[Unset, str]):
        user (Union[Unset, str]):
        with_usage (Union[Unset, str]):
        with_deleted (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SlurmdbV0040GetWckeysResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            cluster=cluster,
            format_=format_,
            id=id,
            name=name,
            only_defaults=only_defaults,
            usage_end=usage_end,
            usage_start=usage_start,
            user=user,
            with_usage=with_usage,
            with_deleted=with_deleted,
        )
    ).parsed
