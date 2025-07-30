from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.generate_error_response import GenerateErrorResponse
from ...models.generate_request_request import GenerateRequestRequest
from ...models.generate_success_response import GenerateSuccessResponse
from ...types import Response


def _get_kwargs(
    *,
    body: Union[
        GenerateRequestRequest,
        GenerateRequestRequest,
        GenerateRequestRequest,
    ],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/generate",
    }

    if isinstance(body, GenerateRequestRequest):
        _json_body = body.to_dict()

        _kwargs["json"] = _json_body
        headers["Content-Type"] = "application/json"
    if isinstance(body, GenerateRequestRequest):
        _data_body = body.to_dict()

        _kwargs["data"] = _data_body
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, GenerateRequestRequest):
        _files_body = body.to_multipart()

        _kwargs["files"] = _files_body
        headers["Content-Type"] = "multipart/form-data"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GenerateErrorResponse, GenerateSuccessResponse]]:
    if response.status_code == 200:
        response_200 = GenerateSuccessResponse.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = GenerateErrorResponse.from_dict(response.json())

        return response_400
    if response.status_code == 402:
        response_402 = GenerateErrorResponse.from_dict(response.json())

        return response_402
    if response.status_code == 403:
        response_403 = GenerateErrorResponse.from_dict(response.json())

        return response_403
    if response.status_code == 500:
        response_500 = GenerateErrorResponse.from_dict(response.json())

        return response_500
    if response.status_code == 502:
        response_502 = GenerateErrorResponse.from_dict(response.json())

        return response_502
    if response.status_code == 504:
        response_504 = GenerateErrorResponse.from_dict(response.json())

        return response_504
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[GenerateErrorResponse, GenerateSuccessResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: Union[
        GenerateRequestRequest,
        GenerateRequestRequest,
        GenerateRequestRequest,
    ],
) -> Response[Union[GenerateErrorResponse, GenerateSuccessResponse]]:
    """Generate text using AI Provider

     Handles POST requests to generate text via a configured AI provider.
    The request body should match the AI provider's chat completions (or similar) format,
    though the 'model' field will be overridden by the server-configured generator model ID.
    Billing and logging are handled internally.

    Args:
        body (GenerateRequestRequest):
        body (GenerateRequestRequest):
        body (GenerateRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GenerateErrorResponse, GenerateSuccessResponse]]
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
    body: Union[
        GenerateRequestRequest,
        GenerateRequestRequest,
        GenerateRequestRequest,
    ],
) -> Optional[Union[GenerateErrorResponse, GenerateSuccessResponse]]:
    """Generate text using AI Provider

     Handles POST requests to generate text via a configured AI provider.
    The request body should match the AI provider's chat completions (or similar) format,
    though the 'model' field will be overridden by the server-configured generator model ID.
    Billing and logging are handled internally.

    Args:
        body (GenerateRequestRequest):
        body (GenerateRequestRequest):
        body (GenerateRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GenerateErrorResponse, GenerateSuccessResponse]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: Union[
        GenerateRequestRequest,
        GenerateRequestRequest,
        GenerateRequestRequest,
    ],
) -> Response[Union[GenerateErrorResponse, GenerateSuccessResponse]]:
    """Generate text using AI Provider

     Handles POST requests to generate text via a configured AI provider.
    The request body should match the AI provider's chat completions (or similar) format,
    though the 'model' field will be overridden by the server-configured generator model ID.
    Billing and logging are handled internally.

    Args:
        body (GenerateRequestRequest):
        body (GenerateRequestRequest):
        body (GenerateRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GenerateErrorResponse, GenerateSuccessResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: Union[
        GenerateRequestRequest,
        GenerateRequestRequest,
        GenerateRequestRequest,
    ],
) -> Optional[Union[GenerateErrorResponse, GenerateSuccessResponse]]:
    """Generate text using AI Provider

     Handles POST requests to generate text via a configured AI provider.
    The request body should match the AI provider's chat completions (or similar) format,
    though the 'model' field will be overridden by the server-configured generator model ID.
    Billing and logging are handled internally.

    Args:
        body (GenerateRequestRequest):
        body (GenerateRequestRequest):
        body (GenerateRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GenerateErrorResponse, GenerateSuccessResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
