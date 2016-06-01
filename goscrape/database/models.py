from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship

from goscrape.database.connection import Base

application_category_table = Table('app_category', Base.metadata,
                                   Column('app_id', Integer, ForeignKey('apps.id')),
                                   Column('category_id', Integer, ForeignKey('categories.id'))
                                   )


class Application(Base):
    __tablename__ = 'apps'
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    component_name = Column("comp_name", String(150), unique=True, nullable=False)
    name = Column("name", String(500), nullable=False)
    size = Column("size", Integer, nullable=False, default=0)
    version = Column("version", String(10), nullable=False, default="0.0")
    active_installs = Column("act_install", Integer, nullable=False, default=0)
    price = Column("price", Integer, nullable=False, default=0)
    rate = Column("rate", Integer, nullable=False, default=0)
    icon = Column("icon", String(500), nullable=True)
    description = Column("desc", Text, nullable=True)

    developer_id = Column(Integer, ForeignKey('developers.id'))
    developer = relationship("Developer", back_populates="apps")

    categories = relationship(
        "Category",
        secondary=application_category_table,
        back_populates="apps")

    def __init__(self, component_name):
        self.component_name = component_name


class Developer(Base):
    __tablename__ = 'developers'
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    slug = Column("slug", String(150), nullable=False, unique=True)
    name = Column("name", String(500), nullable=True)

    apps = relationship("Application")

    def __init__(self, slug, name=None):
        if not name:
            name = slug

        self.slug = slug
        self.name = name


class Category(Base):
    __tablename__ = 'categories'
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    slug = Column("slug", String(150), nullable=False, unique=True)
    name = Column("name", String(500), nullable=True)
    is_game = Column("is_game", Boolean, nullable=False, default=False)

    apps = relationship(
        "Application",
        secondary=application_category_table,
        back_populates="categories")

    def __init__(self, slug, name=None):
        if not name:
            name = slug

        self.slug = slug
        self.name = name
