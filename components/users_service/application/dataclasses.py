from typing import List, Optional
import datetime
import attr


@attr.dataclass
class User:
    id: Optional[int] = None
    name: Optional[str] = None
    login: Optional[str] = None
    password: Optional[str] = None
