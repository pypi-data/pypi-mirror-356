from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.slurm_v0040_get_job_flags import SlurmV0040GetJobFlags
from ...models.slurm_v0040_get_job_response_200 import SlurmV0040GetJobResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    job_id: str,
    *,
    update_time: Union[Unset, str] = UNSET,
    flags: Union[Unset, SlurmV0040GetJobFlags] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["update_time"] = update_time

    json_flags: Union[Unset, str] = UNSET
    if not isinstance(flags, Unset):
        json_flags = flags.value

    params["flags"] = json_flags

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/slurm/v0.0.40/job/{job_id}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[SlurmV0040GetJobResponse200]:
    if response.status_code == 200:
        response_200 = SlurmV0040GetJobResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[SlurmV0040GetJobResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    job_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    update_time: Union[Unset, str] = UNSET,
    flags: Union[Unset, SlurmV0040GetJobFlags] = UNSET,
) -> Response[SlurmV0040GetJobResponse200]:
    """get job info

    Args:
        job_id (str):
        update_time (Union[Unset, str]):
        flags (Union[Unset, SlurmV0040GetJobFlags]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SlurmV0040GetJobResponse200]
    """

    kwargs = _get_kwargs(
        job_id=job_id,
        update_time=update_time,
        flags=flags,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    job_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    update_time: Union[Unset, str] = UNSET,
    flags: Union[Unset, SlurmV0040GetJobFlags] = UNSET,
) -> Optional[SlurmV0040GetJobResponse200]:
    """get job info

    Args:
        job_id (str):
        update_time (Union[Unset, str]):
        flags (Union[Unset, SlurmV0040GetJobFlags]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SlurmV0040GetJobResponse200
    """

    return sync_detailed(
        job_id=job_id,
        client=client,
        update_time=update_time,
        flags=flags,
    ).parsed


async def asyncio_detailed(
    job_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    update_time: Union[Unset, str] = UNSET,
    flags: Union[Unset, SlurmV0040GetJobFlags] = UNSET,
) -> Response[SlurmV0040GetJobResponse200]:
    """get job info

    Args:
        job_id (str):
        update_time (Union[Unset, str]):
        flags (Union[Unset, SlurmV0040GetJobFlags]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SlurmV0040GetJobResponse200]
    """

    kwargs = _get_kwargs(
        job_id=job_id,
        update_time=update_time,
        flags=flags,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    job_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    update_time: Union[Unset, str] = UNSET,
    flags: Union[Unset, SlurmV0040GetJobFlags] = UNSET,
) -> Optional[SlurmV0040GetJobResponse200]:
    """get job info

    Args:
        job_id (str):
        update_time (Union[Unset, str]):
        flags (Union[Unset, SlurmV0040GetJobFlags]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SlurmV0040GetJobResponse200
    """

    return (
        await asyncio_detailed(
            job_id=job_id,
            client=client,
            update_time=update_time,
            flags=flags,
        )
    ).parsed
