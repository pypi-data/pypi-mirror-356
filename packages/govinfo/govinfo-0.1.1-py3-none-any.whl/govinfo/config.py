from typing import NewType

BASE_URL = "https://api.govinfo.gov"
PAGE_DEFAULT = 20
OFFSET_DEFAULT = "*"

RequestArgs = NewType("RequestArgs", tuple[str, dict])
