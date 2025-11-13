# Forums Constants

## Overview

This module defines configuration for forum functionality, including model references and content display settings.

## Constants

### Model References

- **`HTK_FORUM_MODEL`** - Default: `None` - Forum model (app_label.ModelName)
- **`HTK_FORUM_THREAD_MODEL`** - Default: `None` - Forum thread model
- **`HTK_FORUM_MESSAGE_MODEL`** - Default: `None` - Forum message model
- **`HTK_FORUM_TAG_MODEL`** - Default: `None` - Forum tag model

### Content Configuration

- **`FORUM_SNIPPET_LENGTH`** - Default: `100` - Maximum characters to display in forum snippets/previews

## Usage Examples

### Configure Forum Models

```python
# In Django settings.py
HTK_FORUM_MODEL = 'forums.Forum'
HTK_FORUM_THREAD_MODEL = 'forums.Thread'
HTK_FORUM_MESSAGE_MODEL = 'forums.Message'
HTK_FORUM_TAG_MODEL = 'forums.Tag'
```

### Generate Thread Snippet

```python
from htk.apps.forums.constants import FORUM_SNIPPET_LENGTH

message = "This is a very long forum message..."
snippet = message[:FORUM_SNIPPET_LENGTH] + '...'
```

### Load Forum Models Dynamically

```python
from django.apps import apps
from htk.apps.forums.constants import HTK_FORUM_MODEL, HTK_FORUM_THREAD_MODEL

Forum = apps.get_model(HTK_FORUM_MODEL)
Thread = apps.get_model(HTK_FORUM_THREAD_MODEL)
```
