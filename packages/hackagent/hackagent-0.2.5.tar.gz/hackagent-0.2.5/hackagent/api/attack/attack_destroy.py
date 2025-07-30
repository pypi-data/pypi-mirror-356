from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import Response


def _get_kwargs(
    id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": f"/api/attack/{id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Any]:
    if response.status_code == 204:
        return None
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[Any]:
    """Manages Attack configurations through standard CRUD operations.

    This ViewSet allows clients to:
    - Create new Attack configurations.
    - List existing Attack configurations (with filtering based on user/org).
    - Retrieve details of a specific Attack configuration.
    - Update an existing Attack configuration.
    - Delete an Attack configuration.

    The actual execution of an attack based on these configurations, and the
    management of run statuses or results, are handled by other parts of the API
    (e.g., potentially a RunViewSet or similar).

    Attributes:
        queryset: The base queryset, retrieving all Attack objects with related
                  entities (agent, owner, organization) pre-fetched.
        serializer_class: The serializer (`AttackSerializer`) used for data
                          conversion for Attack configurations.
        authentication_classes: List of authentication backends used.
        permission_classes: List of permission enforcement classes.
        parser_classes: List of parsers for request data (JSONParser).
        lookup_field: The model field used for looking up individual instances ('id').

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[Any]:
    """Manages Attack configurations through standard CRUD operations.

    This ViewSet allows clients to:
    - Create new Attack configurations.
    - List existing Attack configurations (with filtering based on user/org).
    - Retrieve details of a specific Attack configuration.
    - Update an existing Attack configuration.
    - Delete an Attack configuration.

    The actual execution of an attack based on these configurations, and the
    management of run statuses or results, are handled by other parts of the API
    (e.g., potentially a RunViewSet or similar).

    Attributes:
        queryset: The base queryset, retrieving all Attack objects with related
                  entities (agent, owner, organization) pre-fetched.
        serializer_class: The serializer (`AttackSerializer`) used for data
                          conversion for Attack configurations.
        authentication_classes: List of authentication backends used.
        permission_classes: List of permission enforcement classes.
        parser_classes: List of parsers for request data (JSONParser).
        lookup_field: The model field used for looking up individual instances ('id').

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
