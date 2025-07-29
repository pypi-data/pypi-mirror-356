from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.v0040_openapi_partition_resp import V0040OpenapiPartitionResp
from ...types import UNSET, Response, Unset


def _get_kwargs(
    partition_name: str,
    *,
    update_time: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["update_time"] = update_time

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/slurm/v0.0.40/partition/{partition_name}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[V0040OpenapiPartitionResp]:
    if response.status_code == 200:
        response_200 = V0040OpenapiPartitionResp.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[V0040OpenapiPartitionResp]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    partition_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    update_time: Union[Unset, int] = UNSET,
) -> Response[V0040OpenapiPartitionResp]:
    """get partition info

    Args:
        partition_name (str):
        update_time (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V0040OpenapiPartitionResp]
    """

    kwargs = _get_kwargs(
        partition_name=partition_name,
        update_time=update_time,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    partition_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    update_time: Union[Unset, int] = UNSET,
) -> Optional[V0040OpenapiPartitionResp]:
    """get partition info

    Args:
        partition_name (str):
        update_time (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V0040OpenapiPartitionResp
    """

    return sync_detailed(
        partition_name=partition_name,
        client=client,
        update_time=update_time,
    ).parsed


async def asyncio_detailed(
    partition_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    update_time: Union[Unset, int] = UNSET,
) -> Response[V0040OpenapiPartitionResp]:
    """get partition info

    Args:
        partition_name (str):
        update_time (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V0040OpenapiPartitionResp]
    """

    kwargs = _get_kwargs(
        partition_name=partition_name,
        update_time=update_time,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    partition_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    update_time: Union[Unset, int] = UNSET,
) -> Optional[V0040OpenapiPartitionResp]:
    """get partition info

    Args:
        partition_name (str):
        update_time (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V0040OpenapiPartitionResp
    """

    return (
        await asyncio_detailed(
            partition_name=partition_name,
            client=client,
            update_time=update_time,
        )
    ).parsed
