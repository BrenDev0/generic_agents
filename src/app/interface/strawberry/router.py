import logging
from strawberry.fastapi import GraphQLRouter
from src.app.interface.strawberry.schema import schema
logger = logging.getLogger(__name__)


def get_strawberry_graphql_router():
    logger.info("=== Creating GraphQL Router ===")
    logger.info(f"Schema value: {schema}")
    logger.info(f"Schema type: {type(schema)}")
    if schema is None:
        raise ValueError("GraphQL schema cannot be None")
    return GraphQLRouter(schema, path="/graphql")