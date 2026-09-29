# n-python

a growing collection of tiny dependency-free Python libraries for stuff I got sick of rewriting: config management, task logging, and general helpers. every lib is standalone, stdlib-only, and pip-installable on its own.

## what's inside

- **autoconfig** — a `Config` class that merges defaults + env vars + CLI args with validation and immutability, so `cfg.lr` just works and nobody can typo-mutate it at runtime
- **autolog** — timestamped task logging: `info(...)` to log, `save()` to persist everything to `logs.txt`
- **general/** — shared misc helpers

```bash
pip install -e ./autoconfig
pip install -e ./autolog
```

```python
import autoconfig
cfg = autoconfig.Config(lr=0.001)
print(cfg.lr)
```

## stack

pure Python stdlib, deliberately zero-dependency. this repo grows over time — a new folder per library, each with its own examples.
