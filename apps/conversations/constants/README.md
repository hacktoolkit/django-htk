# Conversations Constants

## Overview

This module defines configuration for conversation and messaging systems, including model references and message length constraints.

## Constants

### Model References

- **`HTK_CONVERSATION_MODEL`** - Default: `None` - Conversation model (app_label.ModelName)
- **`HTK_CONVERSATION_PARTICIPANT_MODEL`** - Default: `None` - Participant model
- **`HTK_CONVERSATION_MESSAGE_MODEL`** - Default: `None` - Message model
- **`HTK_CONVERSATION_MESSAGE_REACTION_MODEL`** - Default: `None` - Message reaction model

### Message Configuration

- **`HTK_CONVERSATION_MESSAGE_MAX_LENGTH`** - Default: `2048` - Maximum message length in characters

## Usage Examples

### Configure Models

```python
# In Django settings.py
HTK_CONVERSATION_MODEL = 'myapp.Conversation'
HTK_CONVERSATION_PARTICIPANT_MODEL = 'myapp.Participant'
HTK_CONVERSATION_MESSAGE_MODEL = 'myapp.Message'
HTK_CONVERSATION_MESSAGE_REACTION_MODEL = 'myapp.MessageReaction'
```

### Validate Message Length

```python
from htk.apps.conversations.constants import HTK_CONVERSATION_MESSAGE_MAX_LENGTH

message = "Hello, world!"
if len(message) > HTK_CONVERSATION_MESSAGE_MAX_LENGTH:
    raise ValueError(f'Message exceeds {HTK_CONVERSATION_MESSAGE_MAX_LENGTH} characters')
```

### Use Model References

```python
from django.apps import apps

from htk.apps.conversations.constants import HTK_CONVERSATION_MODEL

Conversation = apps.get_model(HTK_CONVERSATION_MODEL)
conversations = Conversation.objects.all()
```
