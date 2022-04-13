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
#
# books = Table(
#     'Books',
#     metadata,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('name', String(128), nullable=False),
#     Column('author', String(128), nullable=False),
#     Column('available', Boolean, default=False),
# )
#
# metadata = MetaData()


books = Table(
    'Books',
    metadata,
    Column('id', BigInteger, primary_key=True),
    Column('title', String(1000)),
    Column('subtitle', String(1000)),
    Column('price', String(100)),
    Column('rating', Integer),
    Column('authors', String(500)),
    Column('publisher', String(500)),
    Column('year', Integer),
    Column('pages', Integer),
    Column('desc', String(10000)),

)
