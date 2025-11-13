# MongoDB Constants

Configuration constants for MongoDB database connections.

## Configuration Settings

```python
from htk.lib.mongodb.constants import HTK_MONGODB_CONNECTION, HTK_MONGODB_NAME
```

## Database Configuration

Configure MongoDB connection in Django settings:

```python
# settings.py
HTK_MONGODB_CONNECTION = 'mongodb://localhost:27017/'
HTK_MONGODB_NAME = 'your_database_name'
```

## Usage Example

```python
from htk.lib.mongodb.constants import HTK_MONGODB_CONNECTION, HTK_MONGODB_NAME
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient(HTK_MONGODB_CONNECTION)
db = client[HTK_MONGODB_NAME]
```
