from application import dataclasses
from sqlalchemy.orm import registry, relationship

from . import tables

mapper = registry()

mapper.map_imperatively(dataclasses.User, tables.users)
