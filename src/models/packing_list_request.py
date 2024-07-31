from typing import Optional, List

from pydantic import BaseModel


class PackingListRequest(BaseModel):
    is_work: bool
    items_preferences: Optional[List[str]] = None
    activities_preferences: Optional[List[str]] = None
