from collections.abc import Iterator
from contextlib import suppress
from typing import Any, TypeVar

from polyfactory.exceptions import MissingDependencyException
from polyfactory.factories import (
    BaseFactory,
    DataclassFactory,
    TypedDictFactory,
)

T = TypeVar("T")

factories: list[type[BaseFactory]] = []

with suppress(MissingDependencyException):
    from polyfactory.factories.beanie_odm_factory import BeanieDocumentFactory

    factories.append(BeanieDocumentFactory)
with suppress(MissingDependencyException):
    from polyfactory.factories.odmantic_odm_factory import OdmanticModelFactory

    factories.append(OdmanticModelFactory)
with suppress(MissingDependencyException):
    from polyfactory.factories.msgspec_factory import MsgspecFactory

    factories.append(MsgspecFactory)
with suppress(MissingDependencyException):
    from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory

    factories.append(SQLAlchemyFactory)
with suppress(MissingDependencyException):
    from polyfactory.factories.pydantic_factory import ModelFactory

    factories.append(ModelFactory)
factories.extend([DataclassFactory, TypedDictFactory])
with suppress(MissingDependencyException):
    from polyfactory.factories.attrs_factory import AttrsFactory

    factories.append(AttrsFactory)


def unifactory(
    cls: type[T], bases: tuple[type[BaseFactory], ...] | None = None, **kwargs: Any
) -> type[BaseFactory[T]]:
    for factory in factories:
        if factory.is_supported_type(cls):
            return factory.create_factory(model=cls, bases=bases, **kwargs)
    message = f"Did not find a factory for type {cls}"
    raise (ValueError(message))


def build(cls: type[T], **kwargs: Any) -> T:
    return unifactory(cls)().build(**kwargs)


def batch(cls: type[T], size: int, **kwargs: Any) -> list[T]:
    return unifactory(cls)().batch(size=size, **kwargs)


def coverage(cls: type[T], **kwargs: Any) -> Iterator[T]:
    return unifactory(cls)().coverage(**kwargs)
