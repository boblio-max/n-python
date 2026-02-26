import inspect
import functools
import dataclasses
from typing import (
    get_origin,
    get_args,
    Union,
    Any,
)
from validate import validate

# -------------------------
# Global Config
# -------------------------

STRICT_ENABLED = True


def enable():
    global STRICT_ENABLED
    STRICT_ENABLED = True


def disable():
    global STRICT_ENABLED
    STRICT_ENABLED = False


# -------------------------
# Error System
# -------------------------

class StrictTypeError(TypeError):
    pass


def build_error(name, expected, value):
    return StrictTypeError(
        f"""
StrictPy Type Error
-------------------
Parameter : {name}
Expected  : {expected}
Received  : {type(value)}
Value     : {repr(value)}
"""
    )


# -------------------------
# Validation Engine
# -------------------------

_type_cache = {}


def validate(value, expected_type, name="value"):
    if not STRICT_ENABLED:
        return

    if expected_type is Any:
        return

    # Cache parsed origin/args
    if expected_type in _type_cache:
        origin, args = _type_cache[expected_type]
    else:
        origin = get_origin(expected_type)
        args = get_args(expected_type)
        _type_cache[expected_type] = (origin, args)

    # Simple type
    if origin is None:
        if isinstance(expected_type, type):
            if not isinstance(value, expected_type):
                raise build_error(name, expected_type, value)
            return
        return

    # Union / Optional
    if origin is Union:
        for option in args:
            try:
                validate(value, option, name)
                return
            except StrictTypeError:
                continue
        raise build_error(name, expected_type, value)

    # List
    if origin is list:
        if not isinstance(value, list):
            raise build_error(name, list, value)
        inner = args[0]
        for i, item in enumerate(value):
            validate(item, inner, f"{name}[{i}]")
        return

    # Dict
    if origin is dict:
        if not isinstance(value, dict):
            raise build_error(name, dict, value)
        key_type, val_type = args
        for k, v in value.items():
            validate(k, key_type, f"{name}.key")
            validate(v, val_type, f"{name}[{k}]")
        return

    # Tuple
    if origin is tuple:
        if not isinstance(value, tuple):
            raise build_error(name, tuple, value)
        if len(args) == 2 and args[1] is Ellipsis:
            for i, item in enumerate(value):
                validate(item, args[0], f"{name}[{i}]")
        else:
            if len(value) != len(args):
                raise build_error(name, expected_type, value)
            for i, (item, t) in enumerate(zip(value, args)):
                validate(item, t, f"{name}[{i}]")
        return

    # Set
    if origin is set:
        if not isinstance(value, set):
            raise build_error(name, set, value)
        inner = args[0]
        for item in value:
            validate(item, inner, f"{name}.item")
        return


# -------------------------
# Function Decorator
# -------------------------

def strict(obj):
    if inspect.isclass(obj):
        return _strict_class(obj)
    elif callable(obj):
        return _strict_function(obj)
    return obj


def _strict_function(func):
    signature = inspect.signature(func)
    annotations = func.__annotations__

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not STRICT_ENABLED:
            return func(*args, **kwargs)

        bound = signature.bind(*args, **kwargs)
        bound.apply_defaults()

        # Validate parameters
        for name, value in bound.arguments.items():
            if name in annotations:
                validate(value, annotations[name], name)

        result = func(*args, **kwargs)

        # Validate return
        if "return" in annotations:
            validate(result, annotations["return"], "return")

        return result

    return wrapper


# -------------------------
# Class Decorator
# -------------------------

def _strict_class(cls):
    annotations = getattr(cls, "__annotations__", {})

    original_setattr = cls.__setattr__

    def __setattr__(self, key, value):
        if STRICT_ENABLED and key in annotations:
            validate(value, annotations[key], key)
        original_setattr(self, key, value)

    cls.__setattr__ = __setattr__

    # Validate dataclass post-init
    if dataclasses.is_dataclass(cls):
        original_post_init = getattr(cls, "__post_init__", None)

        def __post_init__(self, *args, **kwargs):
            for field, field_type in annotations.items():
                value = getattr(self, field)
                validate(value, field_type, field)
            if original_post_init:
                original_post_init(self, *args, **kwargs)

        cls.__post_init__ = __post_init__

    return cls
