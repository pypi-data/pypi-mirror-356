from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.slurmdb_v0040_get_clusters_classification import SlurmdbV0040GetClustersClassification
from ...models.slurmdb_v0040_get_clusters_flags import SlurmdbV0040GetClustersFlags
from ...models.v0040_openapi_clusters_resp import V0040OpenapiClustersResp
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    classification: Union[Unset, SlurmdbV0040GetClustersClassification] = UNSET,
    cluster: Union[Unset, str] = UNSET,
    federation: Union[Unset, str] = UNSET,
    flags: Union[Unset, SlurmdbV0040GetClustersFlags] = UNSET,
    format_: Union[Unset, str] = UNSET,
    rpc_version: Union[Unset, str] = UNSET,
    usage_end: Union[Unset, str] = UNSET,
    usage_start: Union[Unset, str] = UNSET,
    with_deleted: Union[Unset, str] = UNSET,
    with_usage: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_classification: Union[Unset, str] = UNSET
    if not isinstance(classification, Unset):
        json_classification = classification.value

    params["classification"] = json_classification

    params["cluster"] = cluster

    params["federation"] = federation

    json_flags: Union[Unset, str] = UNSET
    if not isinstance(flags, Unset):
        json_flags = flags.value

    params["flags"] = json_flags

    params["format"] = format_

    params["rpc_version"] = rpc_version

    params["usage_end"] = usage_end

    params["usage_start"] = usage_start

    params["with_deleted"] = with_deleted

    params["with_usage"] = with_usage

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/slurmdb/v0.0.40/clusters",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[V0040OpenapiClustersResp]:
    if response.status_code == 200:
        response_200 = V0040OpenapiClustersResp.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[V0040OpenapiClustersResp]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    classification: Union[Unset, SlurmdbV0040GetClustersClassification] = UNSET,
    cluster: Union[Unset, str] = UNSET,
    federation: Union[Unset, str] = UNSET,
    flags: Union[Unset, SlurmdbV0040GetClustersFlags] = UNSET,
    format_: Union[Unset, str] = UNSET,
    rpc_version: Union[Unset, str] = UNSET,
    usage_end: Union[Unset, str] = UNSET,
    usage_start: Union[Unset, str] = UNSET,
    with_deleted: Union[Unset, str] = UNSET,
    with_usage: Union[Unset, str] = UNSET,
) -> Response[V0040OpenapiClustersResp]:
    """Get cluster list

    Args:
        classification (Union[Unset, SlurmdbV0040GetClustersClassification]):
        cluster (Union[Unset, str]):
        federation (Union[Unset, str]):
        flags (Union[Unset, SlurmdbV0040GetClustersFlags]):
        format_ (Union[Unset, str]):
        rpc_version (Union[Unset, str]):
        usage_end (Union[Unset, str]):
        usage_start (Union[Unset, str]):
        with_deleted (Union[Unset, str]):
        with_usage (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V0040OpenapiClustersResp]
    """

    kwargs = _get_kwargs(
        classification=classification,
        cluster=cluster,
        federation=federation,
        flags=flags,
        format_=format_,
        rpc_version=rpc_version,
        usage_end=usage_end,
        usage_start=usage_start,
        with_deleted=with_deleted,
        with_usage=with_usage,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    classification: Union[Unset, SlurmdbV0040GetClustersClassification] = UNSET,
    cluster: Union[Unset, str] = UNSET,
    federation: Union[Unset, str] = UNSET,
    flags: Union[Unset, SlurmdbV0040GetClustersFlags] = UNSET,
    format_: Union[Unset, str] = UNSET,
    rpc_version: Union[Unset, str] = UNSET,
    usage_end: Union[Unset, str] = UNSET,
    usage_start: Union[Unset, str] = UNSET,
    with_deleted: Union[Unset, str] = UNSET,
    with_usage: Union[Unset, str] = UNSET,
) -> Optional[V0040OpenapiClustersResp]:
    """Get cluster list

    Args:
        classification (Union[Unset, SlurmdbV0040GetClustersClassification]):
        cluster (Union[Unset, str]):
        federation (Union[Unset, str]):
        flags (Union[Unset, SlurmdbV0040GetClustersFlags]):
        format_ (Union[Unset, str]):
        rpc_version (Union[Unset, str]):
        usage_end (Union[Unset, str]):
        usage_start (Union[Unset, str]):
        with_deleted (Union[Unset, str]):
        with_usage (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V0040OpenapiClustersResp
    """

    return sync_detailed(
        client=client,
        classification=classification,
        cluster=cluster,
        federation=federation,
        flags=flags,
        format_=format_,
        rpc_version=rpc_version,
        usage_end=usage_end,
        usage_start=usage_start,
        with_deleted=with_deleted,
        with_usage=with_usage,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    classification: Union[Unset, SlurmdbV0040GetClustersClassification] = UNSET,
    cluster: Union[Unset, str] = UNSET,
    federation: Union[Unset, str] = UNSET,
    flags: Union[Unset, SlurmdbV0040GetClustersFlags] = UNSET,
    format_: Union[Unset, str] = UNSET,
    rpc_version: Union[Unset, str] = UNSET,
    usage_end: Union[Unset, str] = UNSET,
    usage_start: Union[Unset, str] = UNSET,
    with_deleted: Union[Unset, str] = UNSET,
    with_usage: Union[Unset, str] = UNSET,
) -> Response[V0040OpenapiClustersResp]:
    """Get cluster list

    Args:
        classification (Union[Unset, SlurmdbV0040GetClustersClassification]):
        cluster (Union[Unset, str]):
        federation (Union[Unset, str]):
        flags (Union[Unset, SlurmdbV0040GetClustersFlags]):
        format_ (Union[Unset, str]):
        rpc_version (Union[Unset, str]):
        usage_end (Union[Unset, str]):
        usage_start (Union[Unset, str]):
        with_deleted (Union[Unset, str]):
        with_usage (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V0040OpenapiClustersResp]
    """

    kwargs = _get_kwargs(
        classification=classification,
        cluster=cluster,
        federation=federation,
        flags=flags,
        format_=format_,
        rpc_version=rpc_version,
        usage_end=usage_end,
        usage_start=usage_start,
        with_deleted=with_deleted,
        with_usage=with_usage,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    classification: Union[Unset, SlurmdbV0040GetClustersClassification] = UNSET,
    cluster: Union[Unset, str] = UNSET,
    federation: Union[Unset, str] = UNSET,
    flags: Union[Unset, SlurmdbV0040GetClustersFlags] = UNSET,
    format_: Union[Unset, str] = UNSET,
    rpc_version: Union[Unset, str] = UNSET,
    usage_end: Union[Unset, str] = UNSET,
    usage_start: Union[Unset, str] = UNSET,
    with_deleted: Union[Unset, str] = UNSET,
    with_usage: Union[Unset, str] = UNSET,
) -> Optional[V0040OpenapiClustersResp]:
    """Get cluster list

    Args:
        classification (Union[Unset, SlurmdbV0040GetClustersClassification]):
        cluster (Union[Unset, str]):
        federation (Union[Unset, str]):
        flags (Union[Unset, SlurmdbV0040GetClustersFlags]):
        format_ (Union[Unset, str]):
        rpc_version (Union[Unset, str]):
        usage_end (Union[Unset, str]):
        usage_start (Union[Unset, str]):
        with_deleted (Union[Unset, str]):
        with_usage (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V0040OpenapiClustersResp
    """

    return (
        await asyncio_detailed(
            client=client,
            classification=classification,
            cluster=cluster,
            federation=federation,
            flags=flags,
            format_=format_,
            rpc_version=rpc_version,
            usage_end=usage_end,
            usage_start=usage_start,
            with_deleted=with_deleted,
            with_usage=with_usage,
        )
    ).parsed
