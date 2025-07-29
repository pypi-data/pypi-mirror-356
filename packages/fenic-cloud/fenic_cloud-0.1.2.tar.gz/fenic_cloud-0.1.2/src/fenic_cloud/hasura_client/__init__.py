"""
Hasura client package for interacting with Hasura GraphQL API
"""

import fenic_cloud.hasura_client.generated_graphql_client as generated_graphql_client
from fenic_cloud.hasura_client.client import HasuraClient
from fenic_cloud.hasura_client.generated_graphql_client import (
    TypedefExecutionStatusReferenceEnum as GraphQLExecutionStatusEnum,
)
from fenic_cloud.hasura_client.generated_graphql_client.exceptions import (
    GraphQLClientError,
    GraphQLClientGraphQLError,
    GraphQLClientGraphQLMultiError,
    GraphQLClientHttpError,
    GraphQLClientInvalidMessageFormat,
    GraphQLClientInvalidResponseError,
)

__all__ = [
    "HasuraClient",
    "GraphQLClientError",
    "GraphQLClientHttpError",
    "GraphQLClientInvalidResponseError",
    "GraphQLClientGraphQLError",
    "GraphQLClientGraphQLMultiError",
    "GraphQLClientInvalidMessageFormat",
    "generated_graphql_client",
    "GraphQLExecutionStatusEnum",
]
