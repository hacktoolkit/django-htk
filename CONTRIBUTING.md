# Contributing to Django HTK

HTK is a shared Django toolkit. Contributions should keep reusable code boring, explicit, and easy to adopt across downstream apps.

## Workflow

1. Scope the change and identify public API, migration, or compatibility risk.
2. Make the smallest coherent patch.
3. Run a relevant check or test before handing off.
4. Update docs/examples when behavior, structure, or recommended usage changes.

## Django App Structure

For new Django apps/modules, use a `models/` package when there is more than one model or when the model set is expected to grow:

```text
apps/example/models/
├── __init__.py
├── README.md
├── thing.py
└── thing_event.py
```

`models/__init__.py` should explicitly re-export the public models:

```python
from htk.apps.example.models.thing import Thing
from htk.apps.example.models.thing_event import ThingEvent

__all__ = (
    'Thing',
    'ThingEvent',
)
```

This gives us small model files while preserving the familiar import path:

```python
from htk.apps.example.models import Thing
```

Do not use dynamic filesystem imports in `models/__init__.py`. If two model files depend on each other, prefer string model references or local imports inside methods to avoid circular imports.

A single-model app may stay as `models.py` if the package form would add noise, but new multi-model apps should use the package pattern by default.

## Tests and Checks

Run the narrowest meaningful verification for your change. For model work, prefer at least one of:

- `python -m compileall -q <changed paths>`
- `python manage.py makemigrations <app> --check --dry-run --settings=<test settings>`
- focused Django app tests

Document what you ran in the PR or handoff.
