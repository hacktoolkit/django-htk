# File Storage Constants

## Overview

This module defines configuration for the file storage system, including security keys for protecting file access.

## Constants

### Security Configuration

- **`HTK_FILE_STORAGE_SECRET`** - Default: `'CHANGE_ME_TO_A_RANDOM_STRING'` - Secret key for signing file storage tokens

## Usage Examples

### Configure Secret Key

```python
# In Django settings.py
# IMPORTANT: Change this to a secure random value in production
HTK_FILE_STORAGE_SECRET = 'your-super-secret-random-key-here'
```

### Generate Secure Secret

```python
# Generate a strong random secret
import secrets
HTK_FILE_STORAGE_SECRET = secrets.token_urlsafe(64)
```
