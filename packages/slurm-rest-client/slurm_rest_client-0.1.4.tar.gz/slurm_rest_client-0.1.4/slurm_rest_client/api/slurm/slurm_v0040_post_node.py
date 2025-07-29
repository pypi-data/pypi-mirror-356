from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.v0040_openapi_resp import V0040OpenapiResp
from ...models.v0040_update_node_msg import V0040UpdateNodeMsg
from ...types import Response


def _get_kwargs(
    node_name: str,
    *,
    body: V0040UpdateNodeMsg,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/slurm/v0.0.40/node/{node_name}",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[V0040OpenapiResp]:
    if response.status_code == 200:
        response_200 = V0040OpenapiResp.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[V0040OpenapiResp]:
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
    body: V0040UpdateNodeMsg,
) -> Response[V0040OpenapiResp]:
    """update node properties

    Args:
        node_name (str):
        body (V0040UpdateNodeMsg):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V0040OpenapiResp]
    """

    kwargs = _get_kwargs(
        node_name=node_name,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    node_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: V0040UpdateNodeMsg,
) -> Optional[V0040OpenapiResp]:
    """update node properties

    Args:
        node_name (str):
        body (V0040UpdateNodeMsg):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V0040OpenapiResp
    """

    return sync_detailed(
        node_name=node_name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    node_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: V0040UpdateNodeMsg,
) -> Response[V0040OpenapiResp]:
    """update node properties

    Args:
        node_name (str):
        body (V0040UpdateNodeMsg):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V0040OpenapiResp]
    """

    kwargs = _get_kwargs(
        node_name=node_name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    node_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: V0040UpdateNodeMsg,
) -> Optional[V0040OpenapiResp]:
    """update node properties

    Args:
        node_name (str):
        body (V0040UpdateNodeMsg):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V0040OpenapiResp
    """

    return (
        await asyncio_detailed(
            node_name=node_name,
            client=client,
            body=body,
        )
    ).parsed
