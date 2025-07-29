from pydantic.networks import HttpUrl

from govinfo.config import RequestArgs
from govinfo.exceptions import GovinfoException
from govinfo.models import GovinfoModel
from govinfo.packages import PackageInfo


class SummaryItem(GovinfoModel):
    collection_code: str
    collection_name: str
    package_count: int
    granule_count: int | None


class CollectionSummary(GovinfoModel):
    collections: list[SummaryItem]


class CollectionContainer(GovinfoModel):
    count: int
    message: str | None
    next_page: HttpUrl | None
    previous_page: HttpUrl | None
    packages: list[PackageInfo]


class CollectionsMixin:
    def _build_collections_request(
        self,
        collection: str = None,
        start_date: str = None,
        end_date: str = None,
        **kwargs,
    ) -> RequestArgs:
        endpoint_parts = ["collections", collection, start_date, end_date]
        path = "/".join(part for part in endpoint_parts if part is not None)
        params = self._set_params(**kwargs)
        return (path, params)

    def collections(
        self,
        collection: str = None,
        start_date: str = None,
        end_date: str = None,
        **kwargs,
    ):
        """Call the collections endpoint of the GovInfo API."""
        args = self._build_collections_request(
            collection, start_date, end_date, **kwargs
        )

        try:
            result = self._get(args)
        except GovinfoException as e:
            raise e

        if collection is None:
            validated = CollectionSummary(**result.data)
        else:
            validated = CollectionContainer(**result.data)
        # TODO: dump with(out) alias?
        return validated.model_dump()
