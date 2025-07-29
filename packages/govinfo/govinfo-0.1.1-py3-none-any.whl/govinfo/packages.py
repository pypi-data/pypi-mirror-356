from datetime import date, datetime

from pydantic import ConfigDict, Field

from govinfo.config import RequestArgs
from govinfo.exceptions import GovinfoException
from govinfo.models import Branch, GovinfoModel


class PackageInfo(GovinfoModel):
    package_id: str
    last_modified: datetime
    package_link: str
    doc_class: str
    title: str
    congress: int
    date_issued: date


class GranuleMetadata(GovinfoModel):
    title: str
    granule_id: str
    granule_link: str
    granule_class: str
    md5: str = Field(default=None)


class GranuleContainer(GovinfoModel):
    count: int
    offset: int | None
    page_size: int
    next_page: str | None
    previous_page: str | None
    granules: list[GranuleMetadata]
    message: str = Field(default=None)


class PackageSummary(GovinfoModel):
    # "allow" since there are so many variations on what is returned
    model_config = ConfigDict(extra="allow")
    category: str
    date_issued: date
    collection_code: str
    collection_name: str
    doc_class: str
    publisher: str
    last_modfied: datetime
    branch: Branch
    # TODO: specify download model
    download: dict
    # TODO: specify other_identifier model
    other_identifier: dict


# TODO: create models that inherit from PackageSummary for specific packages types
# start with BILLS, PLAW, CREC, CRPT, CPRT


class PackagesMixin:
    def _build_granules_request(
        self,
        package_id: str,
        **kwargs,
    ) -> RequestArgs:
        path = f"packages/{package_id}/granules"
        params = self._set_params(**kwargs)
        return (path, params)

    def granules(self, package_id: str, **kwargs):
        """Call the packages/{package_id}/granules endpoint of the GovInfo API."""
        args = self._build_granules_request(package_id, **kwargs)

        try:
            result = self._get(args)
        except GovinfoException as e:
            raise e

        validated = GranuleContainer(**result.data)
        return validated.model_dump()
