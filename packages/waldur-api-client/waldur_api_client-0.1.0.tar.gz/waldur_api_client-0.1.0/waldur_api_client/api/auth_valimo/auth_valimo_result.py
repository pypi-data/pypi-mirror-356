from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.auth_result import AuthResult
from ...models.auth_result_uuid_request import AuthResultUUIDRequest
from ...types import Response


def _get_kwargs(
    *,
    body: AuthResultUUIDRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/auth-valimo/result/",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[AuthResult]:
    if response.status_code == 200:
        response_200 = AuthResult.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[AuthResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: AuthResultUUIDRequest,
) -> Response[AuthResult]:
    """
            To get PKI login status and details - issue post request against /api/auth-valimo/result/
            with uuid in parameters.

            Possible states:
             - Scheduled - login process is scheduled
             - Processing - login is in progress
             - OK - login was successful. Response will contain token.
             - Canceled - login was canceled by user or timed out. Field details will contain additional
    info.
             - Erred - unexpected exception happened during login process.


    Args:
        body (AuthResultUUIDRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthResult]
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
    client: AuthenticatedClient,
    body: AuthResultUUIDRequest,
) -> Optional[AuthResult]:
    """
            To get PKI login status and details - issue post request against /api/auth-valimo/result/
            with uuid in parameters.

            Possible states:
             - Scheduled - login process is scheduled
             - Processing - login is in progress
             - OK - login was successful. Response will contain token.
             - Canceled - login was canceled by user or timed out. Field details will contain additional
    info.
             - Erred - unexpected exception happened during login process.


    Args:
        body (AuthResultUUIDRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthResult
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: AuthResultUUIDRequest,
) -> Response[AuthResult]:
    """
            To get PKI login status and details - issue post request against /api/auth-valimo/result/
            with uuid in parameters.

            Possible states:
             - Scheduled - login process is scheduled
             - Processing - login is in progress
             - OK - login was successful. Response will contain token.
             - Canceled - login was canceled by user or timed out. Field details will contain additional
    info.
             - Erred - unexpected exception happened during login process.


    Args:
        body (AuthResultUUIDRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthResult]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: AuthResultUUIDRequest,
) -> Optional[AuthResult]:
    """
            To get PKI login status and details - issue post request against /api/auth-valimo/result/
            with uuid in parameters.

            Possible states:
             - Scheduled - login process is scheduled
             - Processing - login is in progress
             - OK - login was successful. Response will contain token.
             - Canceled - login was canceled by user or timed out. Field details will contain additional
    info.
             - Erred - unexpected exception happened during login process.


    Args:
        body (AuthResultUUIDRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthResult
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
