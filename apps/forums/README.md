# Forums App

Discussion forums and message threads.

## Quick Start

```python
from htk.apps.forums.models import Forum, ForumThread, ForumMessage

# Create forum
forum = Forum.objects.create(
    name='General Discussion',
    description='Discuss anything'
)

# Create thread
thread = ForumThread.objects.create(
    forum=forum,
    title='Welcome to our forum!',
    created_by=user
)

# Add message
message = ForumMessage.objects.create(
    thread=thread,
    content='Hello everyone!',
    created_by=user
)
```

## Models

- **`Forum`** - Discussion forum
- **`ForumThread`** - Topic/thread in forum
- **`ForumMessage`** - Message in thread
- **`ForumTag`** - Tag for threads

## Common Patterns

```python
# Get forum stats
forum.recent_thread()  # Last updated thread
forum.recent_message()  # Last message

# Tag threads
thread.tags.add('announcement', 'important')

# Search threads
Forum.objects.filter(title__icontains='django')
```

## URL Patterns

- `/forum/` - Forum index
- `/forum/<slug>/` - Forum detail
- `/forum/<slug>/thread/create/` - Create thread
- `/forum/<slug>/thread/<id>/` - Thread detail
