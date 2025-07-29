from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.slurm_v0040_get_reservations_response_200 import SlurmV0040GetReservationsResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    update_time: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["update_time"] = update_time

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/slurm/v0.0.40/reservations",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[SlurmV0040GetReservationsResponse200]:
    if response.status_code == 200:
        response_200 = SlurmV0040GetReservationsResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[SlurmV0040GetReservationsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    update_time: Union[Unset, int] = UNSET,
) -> Response[SlurmV0040GetReservationsResponse200]:
    """get all reservation info

    Args:
        update_time (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SlurmV0040GetReservationsResponse200]
    """

    kwargs = _get_kwargs(
        update_time=update_time,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    update_time: Union[Unset, int] = UNSET,
) -> Optional[SlurmV0040GetReservationsResponse200]:
    """get all reservation info

    Args:
        update_time (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SlurmV0040GetReservationsResponse200
    """

    return sync_detailed(
        client=client,
        update_time=update_time,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    update_time: Union[Unset, int] = UNSET,
) -> Response[SlurmV0040GetReservationsResponse200]:
    """get all reservation info

    Args:
        update_time (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SlurmV0040GetReservationsResponse200]
    """

    kwargs = _get_kwargs(
        update_time=update_time,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    update_time: Union[Unset, int] = UNSET,
) -> Optional[SlurmV0040GetReservationsResponse200]:
    """get all reservation info

    Args:
        update_time (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SlurmV0040GetReservationsResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            update_time=update_time,
        )
    ).parsed
