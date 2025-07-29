from json import JSONDecodeError

import httpx

from govinfo.collections import CollectionsMixin
from govinfo.config import BASE_URL, OFFSET_DEFAULT, PAGE_DEFAULT, RequestArgs
from govinfo.exceptions import GovinfoException
from govinfo.models import Result
from govinfo.packages import PackagesMixin


class Govinfo(CollectionsMixin, PackagesMixin):
    """Wrapper class for the GovInfo API.

    Users can supply an API key or use the default value, DEMO_KEY"""

    def __init__(self, api_key: str = "DEMO_KEY"):
        self._url = f"{BASE_URL}"
        self._api_key = api_key

    def _get(self, args: RequestArgs) -> Result:
        headers = {"x-api-key": self._api_key}
        path, params = args
        with httpx.Client(base_url=self._url, headers=headers, params=params) as client:
            response = client.get(path)
            try:
                data = response.json()
            except (ValueError, JSONDecodeError) as e:
                raise GovinfoException("Bad JSON in response") from e
            is_success = 299 >= response.status_code >= 200
            if is_success:
                return Result(
                    response.status_code, message=response.reason_phrase, data=data
                )
            raise GovinfoException(f"{response.status_code}: {response.reason_phrase}")

    def __repr__(self) -> str:
        api_key = "user supplied" if self._is_api_key_set() else self._api_key
        return f"Govinfo(url={self._url!r}, api_key={api_key!r})"

    def _is_api_key_set(self) -> bool:
        return self._api_key != "DEMO_KEY"

    def _set_params(self, *args, **kwargs) -> dict[str, str]:
        default_params = {"offsetMark": OFFSET_DEFAULT, "pageSize": PAGE_DEFAULT}
        params = (
            default_params
            if not kwargs
            else default_params
            | {
                key.split("_")[0]
                + "".join(word.capitalize() for word in key.split("_")[1:]): value
                for key, value in kwargs.items()
            }
        )
        return params
