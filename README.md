# N-Python

**N-Python** is a collection of Python libraries designed to **speed up Python coding**, reduce repetitive tasks, and make development more efficient. Each library in Nython focuses on solving a common pain point in Python programming, from configuration management to automation and beyond.

This repository will grow over time as more libraries are added.

---

## Current Libraries

### 1. Autoconfig

`autoconfig` is a **lightweight configuration library** that simplifies handling default values, environment variables, and command-line arguments while providing **validation** and **immutability**. Perfect for ML experiments, scripts, or any Python project with configurable parameters.

#### Features

- Merge defaults, CLI arguments, and environment variables.  
- Validate types and ensure required values exist.  
- Immutable configs to prevent accidental runtime changes.  
- Access config values via attributes or as a dictionary.  
- Easy logging and reproducibility.

#### Example Usage

```python
import autoconfig

cfg = autoconfig.Config(
    lr=0.001,
    batch_size=32,
    epochs=10,
    model_name="resnet18",
    data_path="./data"
)

print(cfg.lr)          # 0.001
print(cfg.as_dict())   # {'lr': 0.001, 'batch_size': 32, 'epochs': 10, 'model_name': 'resnet18', 'data_path': './data'}
```

### 2. Autolog
`autolog` is a **simple and effective library* that simplifies logging of different tasks in python, while providing data dependig on those. Perfect for readability and collaboration on python projects with timable measurements

#### Features

- Setting logs such as INFO and METRIC with automatic timestamps
- saving logs directly to a local text file for easy access
- Easy changability for logs to prevent errors

#### Example Usage
```python
from autolog import info, get_log, set_log, change_log_entry, save
info("Program started")
info("Performing initial setup")
info("Setup complete")

# View current logs
logs = get_log()
print("Current Logs:\n", logs)

# Change a specific log entry
# (for demonstration, change the first timestamp entry)
timestamps = list(_data.keys())
if timestamps:
    change_log_entry(timestamps[0], "Program successfully started")

# Save logs to file
save()
print("Logs saved to logs.txt")
```

### 3. StrictPy
`StrictPy` is a **runtime enforcement library* that makes Python’s type hints actually execute as contracts. By decorating functions or classes with @strict, it validates arguments, return values, and annotated attributes during execution, raising clear errors when types don’t match.


### Features
- Runtime Function Validation – Enforces parameter and return type hints during execution.
- Nested Generic Support – Validates list[int], dict[str, float], tuple[int, ...], set[str], including deep nesting.
- Union & Optional Handling – Supports Union and Optional types with proper branch validation.
- Class Attribute Enforcement – Ensures annotated class attributes maintain correct types when assigned.
- Dataclass Integration – Automatically validates annotated dataclass fields after initialization.
- Rich Error Messages – Provides detailed type mismatch reports including parameter name, expected type, actual type, and value.

#### Example Usage
```python
from strictpy import strict
from typing import Optional


@strict
def greet(name: str, age: Optional[int]) -> str:
    if age is None:
        return f"Hello {name}"
    return f"Hello {name}, age {age}"


# ✅ Valid
print(greet("Alice", 25))
print(greet("Bob", None))


# ❌ Invalid
greet(123, 25)      # name must be str
greet("Eve", "20")  # age must be int or None
```
