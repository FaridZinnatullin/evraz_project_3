from typing import List, Optional
import datetime
import attr


@attr.dataclass
class Book:
    id: Optional[int] = None
    name: Optional[str] = None
    author: Optional[str] = None
    available: Optional[bool] = None


