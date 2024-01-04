from dataclasses import asdict, dataclass

import pytest

from unifactory import batch, build, coverage, unifactory


@dataclass
class DataclassItem:
    name: str


@pytest.mark.anyio()
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
async def test_beanie() -> None:
    # given
    pytest.importorskip("beanie")
    from beanie import Document, init_beanie
    from mongomock_motor import AsyncMongoMockClient

    class Item(Document):
        name: str

    client = AsyncMongoMockClient()
    await init_beanie(database=client.get_database("db"), document_models=[Item])

    # when
    item = unifactory(Item)().build()

    # then
    assert isinstance(item, Document)


def test_odmantic() -> None:
    # given
    pytest.importorskip("odmantic")
    from odmantic import Model

    class Item(Model):
        name: str

    # when
    item = unifactory(Item)().build()

    # then
    assert isinstance(item, Model)


def test_msgspec() -> None:
    # given
    pytest.importorskip("msgspec")
    from msgspec import Struct

    class Item(Struct):
        name: str

    # when
    item = unifactory(Item)().build()

    # then
    assert isinstance(item, Struct)


def test_sqlalchemy() -> None:
    # given
    pytest.importorskip("sqlalchemy")
    from sqlalchemy import Column, Integer
    from sqlalchemy.orm import DeclarativeBase

    class Base(DeclarativeBase):
        pass

    class Item(Base):
        __tablename__ = "items"
        item_id = Column(Integer, primary_key=True)

    # when
    item = unifactory(Item)().build()

    # then
    assert isinstance(item, Base)


def test_pydantic() -> None:
    # given
    pytest.importorskip("pydantic")
    from pydantic import BaseModel

    class Item(BaseModel):
        name: str

    # when
    item = unifactory(Item)().build()

    # then
    assert isinstance(item, BaseModel)


def test_dataclass() -> None:
    # when
    item = unifactory(DataclassItem)().build()

    # then
    assert "name" in asdict(item)


def test_typeddict() -> None:
    # given
    from typing import TypedDict

    class Item(TypedDict):
        name: str

    # when
    item = unifactory(Item)().build()

    # then
    assert "name" in item


def test_attrs() -> None:
    # given
    pytest.importorskip("attrs")
    from attrs import asdict, define

    @define
    class Item:
        name: str

    # when
    item = unifactory(Item)().build()

    # then
    assert "name" in asdict(item)


def test_unsupported() -> None:
    # given
    class Item:
        pass

    with pytest.raises(ValueError, match=r"Did not find a factory for type.*"):
        # when
        unifactory(Item)().build()

        # then raise ValueError


def test_build() -> None:
    # when
    item = build(DataclassItem)

    # then
    assert isinstance(item, DataclassItem)
    assert "name" in asdict(item)


# when
@pytest.mark.parametrize("item", batch(DataclassItem, 5))
def test_batch(item: DataclassItem) -> None:
    # then
    assert isinstance(item, DataclassItem)
    assert "name" in asdict(item)


cov_items = coverage(DataclassItem)


# when
@pytest.mark.parametrize("item", coverage(DataclassItem))
def test_coverage(item: DataclassItem) -> None:
    # then
    assert isinstance(item, DataclassItem)
    assert "name" in asdict(item)


@pytest.fixture()
def anyio_backend() -> str:
    return "asyncio"
