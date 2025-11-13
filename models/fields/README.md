# Fields

## Exports
- `CrossDBForeignKey`
- `StarRatingField`
- `IntegerRangeField`
- `ULIDField`

## Classes
- **`CrossDBForeignKey`** (fields/cross_db_foreign_key.py) - Django does not support for field relations between databases (See Reference 1)
- **`ULID`** (fields/types.py) - ULID class that extends the `ulid.ULID` class with additional methods
- **`ULIDField`** (fields/ulid.py) - ULID Field
