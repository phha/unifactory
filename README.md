# Unifactory

Unifactory is a spin off from [fastapi-overrider](https://github.com/phha/fastapi-overrider).
A simple tool to automatically choose a matching factory from [polyfactory's inventory](https://polyfactory.litestar.dev/usage/library_factories/index.html).

## Installation

`pip install unifactory`

## Examples

```python
from polyfactory.pytest_plugin import register_fixture
from unifactory import unifactory, build, batch, coverage

@dataclass
class Person:
    name: str
    age: float
    height: float
    weight: float

some_person = build(Person)
five_persons = batch(Person, 5)
all_persons = coverage(Person)
person_factory = register_fixture(unifactory(Person), name="person_factory")
```
