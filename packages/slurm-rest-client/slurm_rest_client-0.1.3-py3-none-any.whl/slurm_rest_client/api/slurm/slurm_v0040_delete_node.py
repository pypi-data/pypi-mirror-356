from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.slurm_v0040_delete_node_response_200 import SlurmV0040DeleteNodeResponse200
from ...types import Response


def _get_kwargs(
    node_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": f"/slurm/v0.0.40/node/{node_name}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[SlurmV0040DeleteNodeResponse200]:
    if response.status_code == 200:
        response_200 = SlurmV0040DeleteNodeResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[SlurmV0040DeleteNodeResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    node_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[SlurmV0040DeleteNodeResponse200]:
    """delete node

    Args:
        node_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SlurmV0040DeleteNodeResponse200]
    """

    kwargs = _get_kwargs(
        node_name=node_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    node_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[SlurmV0040DeleteNodeResponse200]:
    """delete node

    Args:
        node_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SlurmV0040DeleteNodeResponse200
    """

    return sync_detailed(
        node_name=node_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    node_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[SlurmV0040DeleteNodeResponse200]:
    """delete node

    Args:
        node_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SlurmV0040DeleteNodeResponse200]
    """

    kwargs = _get_kwargs(
        node_name=node_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    node_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[SlurmV0040DeleteNodeResponse200]:
    """delete node

    Args:
        node_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SlurmV0040DeleteNodeResponse200
    """

    return (
        await asyncio_detailed(
            node_name=node_name,
            client=client,
        )
    ).parsed
