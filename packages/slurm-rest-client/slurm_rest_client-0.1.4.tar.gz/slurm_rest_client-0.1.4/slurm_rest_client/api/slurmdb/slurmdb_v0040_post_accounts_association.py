from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.v0040_openapi_accounts_add_cond_resp import V0040OpenapiAccountsAddCondResp
from ...models.v0040_openapi_accounts_add_cond_resp_str import V0040OpenapiAccountsAddCondRespStr
from ...types import Response


def _get_kwargs(
    *,
    body: V0040OpenapiAccountsAddCondResp,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/slurmdb/v0.0.40/accounts_association",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[V0040OpenapiAccountsAddCondRespStr]:
    if response.status_code == 200:
        response_200 = V0040OpenapiAccountsAddCondRespStr.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[V0040OpenapiAccountsAddCondRespStr]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: V0040OpenapiAccountsAddCondResp,
) -> Response[V0040OpenapiAccountsAddCondRespStr]:
    """Add accounts with conditional association

    Args:
        body (V0040OpenapiAccountsAddCondResp):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V0040OpenapiAccountsAddCondRespStr]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: V0040OpenapiAccountsAddCondResp,
) -> Optional[V0040OpenapiAccountsAddCondRespStr]:
    """Add accounts with conditional association

    Args:
        body (V0040OpenapiAccountsAddCondResp):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V0040OpenapiAccountsAddCondRespStr
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: V0040OpenapiAccountsAddCondResp,
) -> Response[V0040OpenapiAccountsAddCondRespStr]:
    """Add accounts with conditional association

    Args:
        body (V0040OpenapiAccountsAddCondResp):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[V0040OpenapiAccountsAddCondRespStr]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: V0040OpenapiAccountsAddCondResp,
) -> Optional[V0040OpenapiAccountsAddCondRespStr]:
    """Add accounts with conditional association

    Args:
        body (V0040OpenapiAccountsAddCondResp):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        V0040OpenapiAccountsAddCondRespStr
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
