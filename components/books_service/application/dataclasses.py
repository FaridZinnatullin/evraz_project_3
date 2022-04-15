import datetime
from typing import Optional

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
    service_tag: Optional[str] = None
    batch_datetime: Optional[str] = None


@attr.dataclass
class Booking:
    user_id: int
    book_id: int
    created_datetime: Optional[datetime.datetime] = None
    expiry_datetime: Optional[datetime.datetime] = None
    redeemed: Optional[bool] = False
    id: Optional[int] = None
