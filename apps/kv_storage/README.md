# Kv_Storage

## Classes
- **`KVStorageCache`** (kv_storage/cachekeys.py) - Cache management object for key-value storage
- **`AbstractKVStorage`** (kv_storage/models.py) - AbstractKVStorage is a simple key-value storage on top of your Django app's default data storage (i.e. most likely MySQL)

## Functions
- **`get_kv_storage_model`** (kv_storage/utils.py) - Gets the key-value storage model class
- **`kv_put`** (kv_storage/utils.py) - PUTs a key-value pair for `key` and `value`
- **`kv_get`** (kv_storage/utils.py) - GETs the value of `key` from key-value storage
- **`kv_get_cached`** (kv_storage/utils.py) - GETs the cached value of `key`
- **`kv_delete`** (kv_storage/utils.py) - DELETEs `key` from key-value storage

## Components
**Models** (`models.py`)
