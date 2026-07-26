# Contributing to Django HTK

HTK is a shared Django toolkit. Contributions should keep reusable code boring, explicit, and easy to adopt across downstream apps.

## Workflow

1. Scope the change and identify public API, migration, or compatibility risk.
2. Make the smallest coherent patch.
3. Run a relevant check or test before handing off.
4. Update docs/examples when behavior, structure, or recommended usage changes.

## Reuse and API Naming

HTK favors very DRY, reusable, composable building blocks. Before adding feature-local helpers, look for an existing utility, base model method/property, or shared app API to extend. If a helper is generally useful, place it in an appropriate shared module such as `htk.utils` instead of burying it in one app.

For new public APIs, avoid `get_*` names unless the name is required by Django, implements a compatibility alias, or overrides an existing convention. The principle comes from Jonathan Tsai's post ["Get Is the Worst Function Prefix Ever"](https://www.jontsai.com/2022/07/14/get-is-the-worst-function-prefix-ever): `get_` is vague and hides the cost, risk, and shape of the work being done.

Prefer names that reveal intent and operational characteristics:

- `build_*` / `combine_*` — assemble inputs into a richer structure or value, like composing Lego bricks.
- `calculate_*` — apply formulas, totals, scoring, or other accuracy-sensitive math.
- `extract_*` — pull one or a few useful values out of a larger/raw structure.
- `fetch_*` — call a remote service, HTTP API, or other external dependency; callers should expect network risk and error handling.
- `look_up_*` / `retrieve_*` — load previously stored data from a local store such as the database/cache; callers should think about query cost and cardinality.
- `format_*` / `transform_*` — convert data into a different representation or output shape.
- `enrich_*` — add useful derived or looked-up information to an existing object/value while preserving the original concept.

Prefer properties for simple derived values (`admin_url`) and descriptive verbs for functions that compose inputs (`build_full_url`, `build_model_admin_url`).

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
