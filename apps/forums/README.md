# Forums

## Classes
- **`Forum`** (forums/models.py) - Forum represents a message forum
- **`ForumTag`** (forums/models.py) - ForumTag can either apply to ForumThread or ForumMessage

## Functions
- **`recent_thread`** (forums/models.py) - Retrieves the most recent ForumThread
- **`recent_message`** (forums/models.py) - Retrieves the most recent message in ForumThread
- **`save`** (forums/models.py) - Any customizations,  like updating cache, etc
- **`test_basic_addition`** (forums/tests.py) - Tests that 1 + 1 always equals 2.

## Components
**Models** (`models.py`), **Views** (`views.py`), **Forms** (`forms.py`)

## URL Patterns
- `forum_index`
- `forum`
- `forum_thread_create`
- `forum_thread`
- `forum_message_create`
