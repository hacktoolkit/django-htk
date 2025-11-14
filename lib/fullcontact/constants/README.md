# FullContact API Constants

Configuration constants for FullContact API integration.

## Configuration Settings

```python
from htk.lib.fullcontact.constants import HTK_FULLCONTACT_PERSON_CLASS
```

## Person Class Configuration

Specify the Python class path for FullContact Person objects:

```python
# settings.py
HTK_FULLCONTACT_PERSON_CLASS = 'htk.lib.fullcontact.classes.FullContactPerson'
```

## Usage Example

```python
from django.utils.module_loading import import_string
from htk.lib.fullcontact.constants import HTK_FULLCONTACT_PERSON_CLASS

# Dynamically import the Person class
PersonClass = import_string(HTK_FULLCONTACT_PERSON_CLASS)
person = PersonClass(email='user@example.com')
```
