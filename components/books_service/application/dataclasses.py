from typing import List, Optional
import datetime
import attr


@attr.dataclass
class Book:
    id: Optional[int] = None
    title: Optional[str] = None
    subtitle: Optional[str] = None
    price: Optional[float] = None
    rating: Optional[int] = None
    authors: Optional[str] = None
    publisher: Optional[str] = None
    year: Optional[int] = None
    pages: Optional[int] = None
    desc: Optional[str] = None