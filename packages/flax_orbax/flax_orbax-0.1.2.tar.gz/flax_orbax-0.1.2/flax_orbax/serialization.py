# Convenience library for serializing and deserializing dataclasses / flax models / jax dtypestructs / things that are not usually serializable
import ast
import dataclasses
import importlib
import json
import sys
from dataclasses import asdict, is_dataclass
from functools import partial, wraps
from typing import Callable

import yaml


@dataclasses.dataclass
class SerializableObject:
    """An object that cannot be serialized directly, but can be created from a factory function (which is serializable).

    This is useful for serializing optax optimizers, which are generally not serializable.

    Note: factory must be serializable (ie not a lambda)
    """

    factory: Callable
    args: list = dataclasses.field(default_factory=list)
    kwargs: dict = dataclasses.field(default_factory=dict)

    def __post_init__(self):
        self.object = self.factory(*self.args, **self.kwargs)

    @property
    def __class__(self):
        return self.object.__class__

    def __getattr__(self, name):
        return getattr(self.object, name)

    def __getitem__(self, name):
        return self.object[name]

    def __call__(self, *args, **kwargs):
        return self.object(*args, **kwargs)

    def __repr__(self):
        return f"{repr(self.object)} (recreatable by {self.factory}(*{self.args}, **{self.kwargs}))"


def wrap(serializable_callable: Callable):
    """Wraps a function to return objects that are serialized by re-running the function.

    Note: To work, the function and its arguments must be serializable.
    """

    @wraps(serializable_callable)
    def wrapper(*args, **kwargs):
        return SerializableObject(
            factory=serializable_callable, args=args, kwargs=kwargs
        )

    return wrapper


def get_fields(dataclass):
    names = set(field.name for field in dataclasses.fields(dataclass))
    if {"name", "parent"} <= set(names):
        names = names - {"name", "parent"}
    return names


def main_representer(dumper, data):
    # MUST BE REGISTERED AS NONE
    if dataclasses.is_dataclass(data) and not isinstance(data, type):
        class_name = "%s.%s" % (
            data.__class__.__module__,
            data.__class__.__name__,
        )
        tag = "tag:yaml.org,2002:python/object/apply:" + class_name
        mapping = {"kwds": {name: getattr(data, name) for name in get_fields(data)}}
        return dumper.represent_mapping(tag, mapping)
    return dumper.represent_object(data)


# Register the representer for all dataclasses
yaml.add_multi_representer(object, main_representer)
