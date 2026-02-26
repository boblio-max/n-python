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
