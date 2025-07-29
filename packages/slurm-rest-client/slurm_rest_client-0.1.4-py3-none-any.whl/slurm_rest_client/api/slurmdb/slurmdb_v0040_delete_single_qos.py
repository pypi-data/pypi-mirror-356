from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.v0040_openapi_slurmdbd_qos_removed_resp import V0040OpenapiSlurmdbdQosRemovedResp
from ...types import Response


def _get_kwargs(
    qos: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": f"/slurmdb/v0.0.40/qos/{qos}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[V0040OpenapiSlurmdbdQosRemovedResp]:
    if response.status_code == 200:
        response_200 = V0040OpenapiSlurmdbdQosRemovedResp.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[V0040OpenapiSlurmdbdQosRemovedResp]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    qos: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[V0040OpenapiSlurmdbdQosRemovedResp]:
    """Delete QOS

    Args:
        qos (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V0040OpenapiSlurmdbdQosRemovedResp]
    """

    kwargs = _get_kwargs(
        qos=qos,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    qos: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[V0040OpenapiSlurmdbdQosRemovedResp]:
    """Delete QOS

    Args:
        qos (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V0040OpenapiSlurmdbdQosRemovedResp
    """

    return sync_detailed(
        qos=qos,
        client=client,
    ).parsed


async def asyncio_detailed(
    qos: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[V0040OpenapiSlurmdbdQosRemovedResp]:
    """Delete QOS

    Args:
        qos (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V0040OpenapiSlurmdbdQosRemovedResp]
    """

    kwargs = _get_kwargs(
        qos=qos,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    qos: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[V0040OpenapiSlurmdbdQosRemovedResp]:
    """Delete QOS

    Args:
        qos (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V0040OpenapiSlurmdbdQosRemovedResp
    """

    return (
        await asyncio_detailed(
            qos=qos,
            client=client,
        )
    ).parsed
