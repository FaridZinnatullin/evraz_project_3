from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    Boolean,
    DateTime,
    BigInteger,
    Text
)
import datetime

naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

metadata = MetaData(naming_convention=naming_convention)

books = Table(
    'Books',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(128), nullable=False),
    Column('author', String(128), nullable=False),
    Column('available', Boolean, default=False),
)
