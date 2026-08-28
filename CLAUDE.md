# n-python

n-python is a curated collection of small Python utility libraries aimed at reducing boilerplate. The current sub-packages are `autoconfig` (default/CLI/env merging with validation and immutability) and `autolog` (timestamped task logging with file persistence), with a `general` folder for shared helpers. Each library is standalone and pip-installable.

## Build / Test / Lint Commands

- Install (per library, from repo root): `pip install -e ./autoconfig` and/or `pip install -e ./autolog`
- Build: `python -m build` inside a library folder, or `pip install -e .` for editable installs
- Test: no test suite is defined in this repo — exercise the examples from each README manually
- Lint: not configured
- Dev / run: `python -c "import autoconfig; cfg = autoconfig.Config(lr=0.001); print(cfg.lr)"`

## Code Style Rules

- Language/version: Python 3.10+
- Paradigm: each library is a small flat package; immutable config + dict-or-attribute access; small logging helpers
- Types: light type hints; dataclasses are used where appropriate
- Formatting: PEP 8 (no formatter configured)
- Imports / module style: each library is a top-level subpackage; siblings import via package root
- Dependencies: standard library only — both libraries aim to be dependency-free

## Verification Criteria

Before claiming any task done, Claude MUST:
1. Run `python -c "import autoconfig, autolog"` (from the repo root) to confirm the libraries import.
2. Exercise the `Config` example from the README and confirm attribute access works.
3. Exercise `info(...)` / `save()` from `autolog` and confirm `logs.txt` is created in the working directory.
4. Report the exact commands run and their outcomes in the final message.
