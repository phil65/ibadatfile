# AGENTS.md

## Overview

`ibadatfile` is a small Python wrapper around iba's `ibaFilesLite.dll` COM server
(`IbaFilesLite.IbaFile`) for reading iba PDA `.dat` measurement files into numpy arrays
and pandas DataFrames. Reading files only works on **Windows** with the DLL registered
(`regsvr32 ibaFilesLite.dll`) and a Python whose bitness matches the DLL. The package
itself imports on any OS (pywin32 is imported lazily).

## Architecture

All logic lives in `src/ibadatfile/ibadatfile.py`:

- `IbaDatFile`: wraps the COM reader (`win32com.client.dynamic.Dispatch`). Context manager
  (`__enter__` opens, `__exit__` closes), iterable over channels, `file["name"]` looks a
  channel up by name (raises `IndexError`). File-level info via `QueryInfoByName`:
  `frames()`, `clk()`, `starttime()`, `signal_count()`, `recorder_*()`. `index()` builds a
  `DatetimeIndex` from start time + clock; `data()` returns one DataFrame of all channels.
- `IbaChannel`: wraps one COM channel object. Metadata getters (`name()`, `unit()`,
  `pda_type()`, ...), `data()` (numpy array; bool for digital, int16 when the PDA type says
  so), `series()` (named `pd.Series`).
- `read_ibadat(path, raw_mode=False, preload=True)`: one-call convenience returning a DataFrame.
- `_variant()`: creates the by-ref VARIANT out-parameter for `Query*Data` calls.

`src/ibadatfile/__init__.py` re-exports `IbaDatFile`, `IbaChannel`, `read_ibadat` and package
metadata. `src/ibadatfile/log.py` holds a template `get_logger` helper (currently unused).

## Where to look

| Task | Location |
| --- | --- |
| Reading logic, channel API | `src/ibadatfile/ibadatfile.py` |
| Public exports, version | `src/ibadatfile/__init__.py` |
| Tests | `tests/test_reading.py` (placeholder only) |
| CI (Windows runners) | `.github/workflows/build.yml` |
| Docs build / Pages deploy | `.github/workflows/documentation.yml`, `mkdocs.yml` |
| Dev tasks | `duties.py` |
| Hooks | `.pre-commit-config.yaml` |

## Commands

```bash
uv sync --all-extras                 # setup (default groups: dev, lint, docs)
uv run pytest                        # tests
uv run ruff check . && uv run ruff format --check .
uv run ty check                      # type check (src only, warnings fail CI)
uv run deptry src                    # dependency declarations
uv run mkdocs-mknodes build          # docs -> ./site
uv build
uvx duty lint | lint_check | test | build | serve | version   # duty is not a project dependency
```

CI (`build.yml`) runs ruff, `ty check`, pytest with coverage on `windows-latest` for
Python 3.13 and 3.14 (3.14 is `continue-on-error`). Releases are published from tags
by the `release` job; don't create tags.

## Conventions

- Python >= 3.13, `from __future__ import annotations`, Google-style docstrings
  (no types in `Args`), ruff with preview rules, line length 100, `datetime` imported as `dt`.
- Tests are plain pytest functions (no classes).
- Docs site is the mkdocs-mknodes default: README is the index page, API/dev pages are
  auto-generated. `docs/` is intentionally empty; there are no hand-written pages.

## Pitfalls

- Copier-managed project (`.copier-answers.yml`, template `phil65/copier-phil65`). Don't
  hand-edit template-owned files without need; add dependencies below the
  `# Only add below (Copier)` markers in `pyproject.toml`.
- Keep pywin32 imports (`pythoncom`, `pywintypes`, `win32com`) inside functions so
  `import ibadatfile` works on Linux (docs, ty, tooling). They are listed in
  `[tool.ty.analysis] allowed-unresolved-imports` and mapped in
  `[tool.deptry.package_module_name_map]`.
- Nothing can be tested for real without Windows, the registered DLL and sample `.dat`
  files; the test suite is a placeholder. Don't add tests that require the COM server
  unless they skip when it's unavailable.
- `pywin32` is declared with `platform_system == 'Windows'`; `numpy` and `pandas` are
  direct runtime dependencies.
- `.github/copilot-instructions.md` holds older style notes that overlap with this file.
