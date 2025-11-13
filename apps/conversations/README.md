# Conversations

## Classes
- **`BaseConversation`** (conversations/models.py) - A base conversation class which is extensible
- **`BaseConversationParticipant`** (conversations/models.py) - A participant in a conversation
- **`BaseConversationMessage`** (conversations/models.py) - A message in a conversation
- **`BaseConversationMessageReaction`** (conversations/models.py) - An emoji reaction to a message in

## Functions
- **`find_all_by_user`** (conversations/models.py) - Finds all conversations that a user is a participant in
- **`find_by_participants`** (conversations/models.py) - Finds a conversation by participants
- **`add_participant`** (conversations/models.py) - Adds a participant to this conversation
- **`add_participants`** (conversations/models.py) - Adds several participants to this conversation
- **`remove_participant`** (conversations/models.py) - Removes a participant from this conversation
- **`remove_participants`** (conversations/models.py) - Removes several participants from this conversation
- **`add_reaction`** (conversations/models.py) - Adds a reaction by `user` to this message.
- **`remove_reaction`** (conversations/models.py) - Removes an existing reaction by `user` to this message.
- **`save`** (conversations/models.py) - Saves this message.
- **`repair_emoji`** (conversations/models.py) - Repairs the emoji shortcode to ensure that it is normalized.

## Components
**Models** (`models.py`)
