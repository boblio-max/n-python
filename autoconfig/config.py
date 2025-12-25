from .sources import load_cli_args, load_env_vars
from .validate import validate_and_cast

class Config:
    """
    Central configuration object.
    Supports defaults, CLI args, env vars, validation, and immutability.
    """

    def __init__(self, **defaults):
        # 1. Schema: store type for each key
        super().__setattr__('_schema', {k: type(v) for k, v in defaults.items()})
        # 2. Store default values
        super().__setattr__('_values', defaults.copy())

        # 3. Load external sources
        cli_values = load_cli_args(self._schema.keys())
        env_values = load_env_vars(self._schema.keys())

        # 4. Merge: CLI > ENV > DEFAULT
        for key in self._schema:
            if key in cli_values:
                self._values[key] = cli_values[key]
            elif key in env_values:
                self._values[key] = env_values[key]

        # 5. Validate and cast
        for key, expected_type in self._schema.items():
            self._values[key] = validate_and_cast(key, self._values.get(key), expected_type)

        # 6. Freeze object
        super().__setattr__('_frozen', True)

    def __getattr__(self, name):
        # Access internal _values safely via __dict__ to avoid recursion
        _values = self.__dict__.get('_values', {})
        if name in _values:
            return _values[name]
        raise AttributeError(f"No such config value: '{name}'")

    def __setattr__(self, name, value):
        # Prevent mutation after creation
        if self.__dict__.get('_frozen', False):
            raise AttributeError("Config is immutable after creation")
        super().__setattr__(name, value)

    def as_dict(self):
        # Return a plain dictionary of values
        return dict(self._values)
