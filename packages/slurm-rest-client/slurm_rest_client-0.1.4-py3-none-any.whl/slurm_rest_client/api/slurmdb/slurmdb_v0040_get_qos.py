from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.slurmdb_v0040_get_qos_preempt_mode import SlurmdbV0040GetQosPreemptMode
from ...models.v0040_openapi_slurmdbd_qos_resp import V0040OpenapiSlurmdbdQosResp
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    description: Union[Unset, str] = UNSET,
    id: Union[Unset, str] = UNSET,
    format_: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    preempt_mode: Union[Unset, SlurmdbV0040GetQosPreemptMode] = UNSET,
    with_deleted: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["description"] = description

    params["id"] = id

    params["format"] = format_

    params["name"] = name

    json_preempt_mode: Union[Unset, str] = UNSET
    if not isinstance(preempt_mode, Unset):
        json_preempt_mode = preempt_mode.value

    params["preempt_mode"] = json_preempt_mode

    params["with_deleted"] = with_deleted

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/slurmdb/v0.0.40/qos",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[V0040OpenapiSlurmdbdQosResp]:
    if response.status_code == 200:
        response_200 = V0040OpenapiSlurmdbdQosResp.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[V0040OpenapiSlurmdbdQosResp]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    description: Union[Unset, str] = UNSET,
    id: Union[Unset, str] = UNSET,
    format_: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    preempt_mode: Union[Unset, SlurmdbV0040GetQosPreemptMode] = UNSET,
    with_deleted: Union[Unset, str] = UNSET,
) -> Response[V0040OpenapiSlurmdbdQosResp]:
    """Get QOS list

    Args:
        description (Union[Unset, str]):
        id (Union[Unset, str]):
        format_ (Union[Unset, str]):
        name (Union[Unset, str]):
        preempt_mode (Union[Unset, SlurmdbV0040GetQosPreemptMode]):
        with_deleted (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V0040OpenapiSlurmdbdQosResp]
    """

    kwargs = _get_kwargs(
        description=description,
        id=id,
        format_=format_,
        name=name,
        preempt_mode=preempt_mode,
        with_deleted=with_deleted,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    description: Union[Unset, str] = UNSET,
    id: Union[Unset, str] = UNSET,
    format_: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    preempt_mode: Union[Unset, SlurmdbV0040GetQosPreemptMode] = UNSET,
    with_deleted: Union[Unset, str] = UNSET,
) -> Optional[V0040OpenapiSlurmdbdQosResp]:
    """Get QOS list

    Args:
        description (Union[Unset, str]):
        id (Union[Unset, str]):
        format_ (Union[Unset, str]):
        name (Union[Unset, str]):
        preempt_mode (Union[Unset, SlurmdbV0040GetQosPreemptMode]):
        with_deleted (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V0040OpenapiSlurmdbdQosResp
    """

    return sync_detailed(
        client=client,
        description=description,
        id=id,
        format_=format_,
        name=name,
        preempt_mode=preempt_mode,
        with_deleted=with_deleted,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    description: Union[Unset, str] = UNSET,
    id: Union[Unset, str] = UNSET,
    format_: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    preempt_mode: Union[Unset, SlurmdbV0040GetQosPreemptMode] = UNSET,
    with_deleted: Union[Unset, str] = UNSET,
) -> Response[V0040OpenapiSlurmdbdQosResp]:
    """Get QOS list

    Args:
        description (Union[Unset, str]):
        id (Union[Unset, str]):
        format_ (Union[Unset, str]):
        name (Union[Unset, str]):
        preempt_mode (Union[Unset, SlurmdbV0040GetQosPreemptMode]):
        with_deleted (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V0040OpenapiSlurmdbdQosResp]
    """

    kwargs = _get_kwargs(
        description=description,
        id=id,
        format_=format_,
        name=name,
        preempt_mode=preempt_mode,
        with_deleted=with_deleted,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    description: Union[Unset, str] = UNSET,
    id: Union[Unset, str] = UNSET,
    format_: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    preempt_mode: Union[Unset, SlurmdbV0040GetQosPreemptMode] = UNSET,
    with_deleted: Union[Unset, str] = UNSET,
) -> Optional[V0040OpenapiSlurmdbdQosResp]:
    """Get QOS list

    Args:
        description (Union[Unset, str]):
        id (Union[Unset, str]):
        format_ (Union[Unset, str]):
        name (Union[Unset, str]):
        preempt_mode (Union[Unset, SlurmdbV0040GetQosPreemptMode]):
        with_deleted (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V0040OpenapiSlurmdbdQosResp
    """

    return (
        await asyncio_detailed(
            client=client,
            description=description,
            id=id,
            format_=format_,
            name=name,
            preempt_mode=preempt_mode,
            with_deleted=with_deleted,
        )
    ).parsed
