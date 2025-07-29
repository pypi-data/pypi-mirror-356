from abc import ABCMeta

from ed_domain.core.aggregate_roots.location import Location
from ed_domain.persistence.async_repositories.abc_async_generic_repository import \
    ABCAsyncGenericRepository


class ABCAsyncLocationRepository(
    ABCAsyncGenericRepository[Location],
    metaclass=ABCMeta,
):
    ...
