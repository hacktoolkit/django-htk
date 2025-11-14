# Conversations App

User-to-user messaging and conversation threads with emoji reactions.

## Overview

The `conversations` app provides:

- Create conversations between users
- Message threads with multiple participants
- Emoji reactions to messages
- Conversation history and management
- Thread participants tracking

## Quick Start

### Create Conversations

```python
from htk.apps.conversations.models import BaseConversation

# Create new conversation
convo = BaseConversation.objects.create(subject='Project Discussion')

# Add participants
convo.add_participant(user1)
convo.add_participants([user2, user3])

# Send message
message = convo.add_message(sender=user1, text='Hello everyone!')
```

### Find Conversations

```python
# Find all conversations for a user
conversations = BaseConversation.find_all_by_user(user)

# Find conversation with specific participants
convo = BaseConversation.find_by_participants([user1, user2])
```

### Message Management

```python
# Get messages in conversation
messages = convo.messages.all()

# Add reaction to message
message.add_reaction(user=user, emoji='👍')

# Remove reaction
message.remove_reaction(user=user, emoji='👍')

# Get reactions
reactions = message.reactions.all()
```

### Participants

```python
# Get conversation participants
participants = convo.participants.all()

# Remove participant
convo.remove_participant(user)

# Check if user is participant
is_participant = convo.participants.filter(user=user).exists()
```

## Models

- **`BaseConversation`** - Main conversation model (extend for custom behavior)
- **`BaseConversationParticipant`** - Tracks conversation participants
- **`BaseConversationMessage`** - Individual messages
- **`BaseConversationMessageReaction`** - Emoji reactions to messages

## Common Patterns

### Direct Message Between Users

```python
from htk.apps.conversations.models import BaseConversation

user1 = User.objects.get(username='alice')
user2 = User.objects.get(username='bob')

# Find or create DM
convo = BaseConversation.find_by_participants([user1, user2])
if not convo:
    convo = BaseConversation.objects.create(subject=f'{user1} & {user2}')
    convo.add_participants([user1, user2])

# Send message
convo.add_message(sender=user1, text='Hey Bob!')
```

### Group Chat

```python
# Create group conversation
group = BaseConversation.objects.create(subject='Engineering Team')
group.add_participants([user1, user2, user3, user4])

# Broadcast message to group
group.add_message(sender=moderator, text='Important announcement')
```

### Mark Messages as Read

```python
# Extend BaseConversationMessage to add read tracking
class Message(BaseConversationMessage):
    read_by = models.ManyToManyField(User, related_name='read_messages')

    def mark_read(self, user):
        self.read_by.add(user)
```

## Best Practices

1. **Validate participants** before creating conversations
2. **Extend base models** to add custom fields (read status, archived, etc.)
3. **Cache conversation lists** for performance
4. **Handle emoji normalization** - `repair_emoji()` called automatically on save
5. **Clean up old conversations** - Archive or delete inactive ones

## Signals

Automatic signal handlers:
- `repair_emoji` - Normalizes emoji shortcodes when message is saved

## Integration with Other Apps

```python
# With Organizations
from htk.apps.organizations.models import Organization

class OrgConversation(BaseConversation):
    organization = ForeignKey(Organization)

# With Notifications
from htk.apps.notifications.utils import notify

def message_created(sender, instance, created, **kwargs):
    if created:
        # Notify participants
        for participant in instance.conversation.participants.all():
            if participant.user != instance.sender:
                notify(participant.user, f'New message in {instance.conversation}')
```
