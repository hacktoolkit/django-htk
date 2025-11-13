# Models

## Classes
- **`HtkBaseModel`** (models/classes.py) - An abstract class extending Django models.Model
- **`AbstractAttribute`** (models/classes.py) - An abstract class for storing an arbitrary attribute on a Django model
- **`AbstractAttributeHolderClassFactory`** (models/classes.py) - Creates an attribute holder class for multi-inheritance
- **`CrossDBForeignKey`** (models/fields/cross_db_foreign_key.py) - Django does not support for field relations between databases (See Reference 1)
- **`ULID`** (models/fields/types.py) - ULID class that extends the `ulid.ULID` class with additional methods
- **`ULIDField`** (models/fields/ulid.py) - ULID Field

## Functions
- **`json_encode`** (models/classes.py) - Returns a dictionary that can be `json.dumps()`-ed as a JSON representation of this object
- **`json_decode`** (models/classes.py) - Iterates over a flat dictionary `payload` and
- **`attribute_fields`** (models/classes.py) - Returns a sequence (list or tuple) of attribute keys
- **`boolean_attributes_lookup`** (models/classes.py) - Returns a dictionary of attribute keys that are
- **`normalize_model_field_value`** (models/utils.py) - Deserializes/normalizes the value for a particular model field.
