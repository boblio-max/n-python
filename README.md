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


