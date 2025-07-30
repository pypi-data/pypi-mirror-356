from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.agent import Agent
from ...models.agent_request import AgentRequest
from ...types import Response


def _get_kwargs(
    *,
    body: AgentRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/agent",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Agent]:
    if response.status_code == 201:
        response_201 = Agent.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Agent]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: AgentRequest,
) -> Response[Agent]:
    """Provides CRUD operations for Agent instances.

    This ViewSet manages Agent records, ensuring that users can only interact
    with agents based on their permissions and organizational context.
    It filters agent listings for users and handles the logic for creating
    agents, including associating them with the correct organization and owner.

    Authentication uses UserAPIKeyAuthentication and PrivyAuthentication.
    Permissions are based on IsAuthenticated, with queryset filtering providing
    row-level access control.

    Class Attributes:
        queryset (QuerySet): The default queryset for listing agents, initially all agents.
                             This is further filtered by `get_queryset()`.
        serializer_class (AgentSerializer): The serializer used for validating and
                                          deserializing input, and for serializing output.
        authentication_classes (list): List of authentication classes to use.
        permission_classes (list): List of permission classes to use.
        parser_classes (list): List of parser classes for handling request data.
        lookup_field (str): The model field used for looking up individual instances (UUID 'id').

    Args:
        body (AgentRequest): Serializes Agent model instances to JSON and validates data for
            creating
            or updating Agent instances.

            This serializer provides a comprehensive representation of an Agent,
            including its type, endpoint, and nested details for related 'organization'
            and 'owner' for read operations, while allowing 'organization' and 'owner' IDs
            for write operations.

            Attributes:
                organization_detail (OrganizationMinimalSerializer): Read-only nested
                    serializer for the agent's organization. Displays minimal details.
                owner_detail (UserProfileMinimalSerializer): Read-only nested serializer
                    for the agent's owner's user profile. Displays minimal details.
                    Can be null if the agent has no owner or the owner has no profile.
                type (CharField): The type of the agent (e.g., GENERIC_ADK, OPENAI_SDK).
                                  Uses the choices defined in the Agent model's AgentType enum.

            Meta:
                model (Agent): The model class that this serializer works with.
                fields (tuple): The fields to include in the serialized output.
                    Includes standard Agent fields like 'endpoint', 'type',
                    and the read-only nested details.
                read_only_fields (tuple): Fields that are read-only and cannot be
                    set during create/update operations through this serializer.
                    This includes 'id', 'created_at', 'updated_at', and the
                    nested detail fields.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Agent]
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
    body: AgentRequest,
) -> Optional[Agent]:
    """Provides CRUD operations for Agent instances.

    This ViewSet manages Agent records, ensuring that users can only interact
    with agents based on their permissions and organizational context.
    It filters agent listings for users and handles the logic for creating
    agents, including associating them with the correct organization and owner.

    Authentication uses UserAPIKeyAuthentication and PrivyAuthentication.
    Permissions are based on IsAuthenticated, with queryset filtering providing
    row-level access control.

    Class Attributes:
        queryset (QuerySet): The default queryset for listing agents, initially all agents.
                             This is further filtered by `get_queryset()`.
        serializer_class (AgentSerializer): The serializer used for validating and
                                          deserializing input, and for serializing output.
        authentication_classes (list): List of authentication classes to use.
        permission_classes (list): List of permission classes to use.
        parser_classes (list): List of parser classes for handling request data.
        lookup_field (str): The model field used for looking up individual instances (UUID 'id').

    Args:
        body (AgentRequest): Serializes Agent model instances to JSON and validates data for
            creating
            or updating Agent instances.

            This serializer provides a comprehensive representation of an Agent,
            including its type, endpoint, and nested details for related 'organization'
            and 'owner' for read operations, while allowing 'organization' and 'owner' IDs
            for write operations.

            Attributes:
                organization_detail (OrganizationMinimalSerializer): Read-only nested
                    serializer for the agent's organization. Displays minimal details.
                owner_detail (UserProfileMinimalSerializer): Read-only nested serializer
                    for the agent's owner's user profile. Displays minimal details.
                    Can be null if the agent has no owner or the owner has no profile.
                type (CharField): The type of the agent (e.g., GENERIC_ADK, OPENAI_SDK).
                                  Uses the choices defined in the Agent model's AgentType enum.

            Meta:
                model (Agent): The model class that this serializer works with.
                fields (tuple): The fields to include in the serialized output.
                    Includes standard Agent fields like 'endpoint', 'type',
                    and the read-only nested details.
                read_only_fields (tuple): Fields that are read-only and cannot be
                    set during create/update operations through this serializer.
                    This includes 'id', 'created_at', 'updated_at', and the
                    nested detail fields.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Agent
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: AgentRequest,
) -> Response[Agent]:
    """Provides CRUD operations for Agent instances.

    This ViewSet manages Agent records, ensuring that users can only interact
    with agents based on their permissions and organizational context.
    It filters agent listings for users and handles the logic for creating
    agents, including associating them with the correct organization and owner.

    Authentication uses UserAPIKeyAuthentication and PrivyAuthentication.
    Permissions are based on IsAuthenticated, with queryset filtering providing
    row-level access control.

    Class Attributes:
        queryset (QuerySet): The default queryset for listing agents, initially all agents.
                             This is further filtered by `get_queryset()`.
        serializer_class (AgentSerializer): The serializer used for validating and
                                          deserializing input, and for serializing output.
        authentication_classes (list): List of authentication classes to use.
        permission_classes (list): List of permission classes to use.
        parser_classes (list): List of parser classes for handling request data.
        lookup_field (str): The model field used for looking up individual instances (UUID 'id').

    Args:
        body (AgentRequest): Serializes Agent model instances to JSON and validates data for
            creating
            or updating Agent instances.

            This serializer provides a comprehensive representation of an Agent,
            including its type, endpoint, and nested details for related 'organization'
            and 'owner' for read operations, while allowing 'organization' and 'owner' IDs
            for write operations.

            Attributes:
                organization_detail (OrganizationMinimalSerializer): Read-only nested
                    serializer for the agent's organization. Displays minimal details.
                owner_detail (UserProfileMinimalSerializer): Read-only nested serializer
                    for the agent's owner's user profile. Displays minimal details.
                    Can be null if the agent has no owner or the owner has no profile.
                type (CharField): The type of the agent (e.g., GENERIC_ADK, OPENAI_SDK).
                                  Uses the choices defined in the Agent model's AgentType enum.

            Meta:
                model (Agent): The model class that this serializer works with.
                fields (tuple): The fields to include in the serialized output.
                    Includes standard Agent fields like 'endpoint', 'type',
                    and the read-only nested details.
                read_only_fields (tuple): Fields that are read-only and cannot be
                    set during create/update operations through this serializer.
                    This includes 'id', 'created_at', 'updated_at', and the
                    nested detail fields.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Agent]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: AgentRequest,
) -> Optional[Agent]:
    """Provides CRUD operations for Agent instances.

    This ViewSet manages Agent records, ensuring that users can only interact
    with agents based on their permissions and organizational context.
    It filters agent listings for users and handles the logic for creating
    agents, including associating them with the correct organization and owner.

    Authentication uses UserAPIKeyAuthentication and PrivyAuthentication.
    Permissions are based on IsAuthenticated, with queryset filtering providing
    row-level access control.

    Class Attributes:
        queryset (QuerySet): The default queryset for listing agents, initially all agents.
                             This is further filtered by `get_queryset()`.
        serializer_class (AgentSerializer): The serializer used for validating and
                                          deserializing input, and for serializing output.
        authentication_classes (list): List of authentication classes to use.
        permission_classes (list): List of permission classes to use.
        parser_classes (list): List of parser classes for handling request data.
        lookup_field (str): The model field used for looking up individual instances (UUID 'id').

    Args:
        body (AgentRequest): Serializes Agent model instances to JSON and validates data for
            creating
            or updating Agent instances.

            This serializer provides a comprehensive representation of an Agent,
            including its type, endpoint, and nested details for related 'organization'
            and 'owner' for read operations, while allowing 'organization' and 'owner' IDs
            for write operations.

            Attributes:
                organization_detail (OrganizationMinimalSerializer): Read-only nested
                    serializer for the agent's organization. Displays minimal details.
                owner_detail (UserProfileMinimalSerializer): Read-only nested serializer
                    for the agent's owner's user profile. Displays minimal details.
                    Can be null if the agent has no owner or the owner has no profile.
                type (CharField): The type of the agent (e.g., GENERIC_ADK, OPENAI_SDK).
                                  Uses the choices defined in the Agent model's AgentType enum.

            Meta:
                model (Agent): The model class that this serializer works with.
                fields (tuple): The fields to include in the serialized output.
                    Includes standard Agent fields like 'endpoint', 'type',
                    and the read-only nested details.
                read_only_fields (tuple): Fields that are read-only and cannot be
                    set during create/update operations through this serializer.
                    This includes 'id', 'created_at', 'updated_at', and the
                    nested detail fields.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Agent
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
