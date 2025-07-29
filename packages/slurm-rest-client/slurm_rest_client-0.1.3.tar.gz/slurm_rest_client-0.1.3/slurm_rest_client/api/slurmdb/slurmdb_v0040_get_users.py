from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.slurmdb_v0040_get_users_admin_level import SlurmdbV0040GetUsersAdminLevel
from ...models.slurmdb_v0040_get_users_response_200 import SlurmdbV0040GetUsersResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    admin_level: Union[Unset, SlurmdbV0040GetUsersAdminLevel] = UNSET,
    default_account: Union[Unset, str] = UNSET,
    default_wckey: Union[Unset, str] = UNSET,
    with_assocs: Union[Unset, str] = UNSET,
    with_coords: Union[Unset, str] = UNSET,
    with_deleted: Union[Unset, str] = UNSET,
    with_wckeys: Union[Unset, str] = UNSET,
    without_defaults: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_admin_level: Union[Unset, str] = UNSET
    if not isinstance(admin_level, Unset):
        json_admin_level = admin_level.value

    params["admin_level"] = json_admin_level

    params["default_account"] = default_account

    params["default_wckey"] = default_wckey

    params["with_assocs"] = with_assocs

    params["with_coords"] = with_coords

    params["with_deleted"] = with_deleted

    params["with_wckeys"] = with_wckeys

    params["without_defaults"] = without_defaults

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/slurmdb/v0.0.40/users",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[SlurmdbV0040GetUsersResponse200]:
    if response.status_code == 200:
        response_200 = SlurmdbV0040GetUsersResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[SlurmdbV0040GetUsersResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    admin_level: Union[Unset, SlurmdbV0040GetUsersAdminLevel] = UNSET,
    default_account: Union[Unset, str] = UNSET,
    default_wckey: Union[Unset, str] = UNSET,
    with_assocs: Union[Unset, str] = UNSET,
    with_coords: Union[Unset, str] = UNSET,
    with_deleted: Union[Unset, str] = UNSET,
    with_wckeys: Union[Unset, str] = UNSET,
    without_defaults: Union[Unset, str] = UNSET,
) -> Response[SlurmdbV0040GetUsersResponse200]:
    """Get user list

    Args:
        admin_level (Union[Unset, SlurmdbV0040GetUsersAdminLevel]):
        default_account (Union[Unset, str]):
        default_wckey (Union[Unset, str]):
        with_assocs (Union[Unset, str]):
        with_coords (Union[Unset, str]):
        with_deleted (Union[Unset, str]):
        with_wckeys (Union[Unset, str]):
        without_defaults (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SlurmdbV0040GetUsersResponse200]
    """

    kwargs = _get_kwargs(
        admin_level=admin_level,
        default_account=default_account,
        default_wckey=default_wckey,
        with_assocs=with_assocs,
        with_coords=with_coords,
        with_deleted=with_deleted,
        with_wckeys=with_wckeys,
        without_defaults=without_defaults,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    admin_level: Union[Unset, SlurmdbV0040GetUsersAdminLevel] = UNSET,
    default_account: Union[Unset, str] = UNSET,
    default_wckey: Union[Unset, str] = UNSET,
    with_assocs: Union[Unset, str] = UNSET,
    with_coords: Union[Unset, str] = UNSET,
    with_deleted: Union[Unset, str] = UNSET,
    with_wckeys: Union[Unset, str] = UNSET,
    without_defaults: Union[Unset, str] = UNSET,
) -> Optional[SlurmdbV0040GetUsersResponse200]:
    """Get user list

    Args:
        admin_level (Union[Unset, SlurmdbV0040GetUsersAdminLevel]):
        default_account (Union[Unset, str]):
        default_wckey (Union[Unset, str]):
        with_assocs (Union[Unset, str]):
        with_coords (Union[Unset, str]):
        with_deleted (Union[Unset, str]):
        with_wckeys (Union[Unset, str]):
        without_defaults (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SlurmdbV0040GetUsersResponse200
    """

    return sync_detailed(
        client=client,
        admin_level=admin_level,
        default_account=default_account,
        default_wckey=default_wckey,
        with_assocs=with_assocs,
        with_coords=with_coords,
        with_deleted=with_deleted,
        with_wckeys=with_wckeys,
        without_defaults=without_defaults,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    admin_level: Union[Unset, SlurmdbV0040GetUsersAdminLevel] = UNSET,
    default_account: Union[Unset, str] = UNSET,
    default_wckey: Union[Unset, str] = UNSET,
    with_assocs: Union[Unset, str] = UNSET,
    with_coords: Union[Unset, str] = UNSET,
    with_deleted: Union[Unset, str] = UNSET,
    with_wckeys: Union[Unset, str] = UNSET,
    without_defaults: Union[Unset, str] = UNSET,
) -> Response[SlurmdbV0040GetUsersResponse200]:
    """Get user list

    Args:
        admin_level (Union[Unset, SlurmdbV0040GetUsersAdminLevel]):
        default_account (Union[Unset, str]):
        default_wckey (Union[Unset, str]):
        with_assocs (Union[Unset, str]):
        with_coords (Union[Unset, str]):
        with_deleted (Union[Unset, str]):
        with_wckeys (Union[Unset, str]):
        without_defaults (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SlurmdbV0040GetUsersResponse200]
    """

    kwargs = _get_kwargs(
        admin_level=admin_level,
        default_account=default_account,
        default_wckey=default_wckey,
        with_assocs=with_assocs,
        with_coords=with_coords,
        with_deleted=with_deleted,
        with_wckeys=with_wckeys,
        without_defaults=without_defaults,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    admin_level: Union[Unset, SlurmdbV0040GetUsersAdminLevel] = UNSET,
    default_account: Union[Unset, str] = UNSET,
    default_wckey: Union[Unset, str] = UNSET,
    with_assocs: Union[Unset, str] = UNSET,
    with_coords: Union[Unset, str] = UNSET,
    with_deleted: Union[Unset, str] = UNSET,
    with_wckeys: Union[Unset, str] = UNSET,
    without_defaults: Union[Unset, str] = UNSET,
) -> Optional[SlurmdbV0040GetUsersResponse200]:
    """Get user list

    Args:
        admin_level (Union[Unset, SlurmdbV0040GetUsersAdminLevel]):
        default_account (Union[Unset, str]):
        default_wckey (Union[Unset, str]):
        with_assocs (Union[Unset, str]):
        with_coords (Union[Unset, str]):
        with_deleted (Union[Unset, str]):
        with_wckeys (Union[Unset, str]):
        without_defaults (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SlurmdbV0040GetUsersResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            admin_level=admin_level,
            default_account=default_account,
            default_wckey=default_wckey,
            with_assocs=with_assocs,
            with_coords=with_coords,
            with_deleted=with_deleted,
            with_wckeys=with_wckeys,
            without_defaults=without_defaults,
        )
    ).parsed
