from sqlalchemy.orm import registry, relationship

from application import dataclasses

from . import tables

mapper = registry()

mapper.map_imperatively(dataclasses.Book, tables.books)