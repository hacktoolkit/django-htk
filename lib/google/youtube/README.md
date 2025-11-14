# YouTube API Utilities

Utilities for working with YouTube videos including ID extraction and duration retrieval.

## Functions

**extract_youtube_video_id(youtube_video_url)**
- Extracts YouTube video ID from various URL formats
- Supports multiple URL patterns (youtu.be, youtube.com/watch, youtube.com/shorts, etc.)
- Returns video ID string or None if extraction fails
- Uses regex pattern matching with error handling and rollbar logging

**build_youtube_api_url(youtube_video_id)**
- Builds a complete YouTube Data API v3 request URL
- Uses `settings.HTK_GOOGLE_SERVER_API_KEY` for authentication
- Returns formatted URL with query parameters for content details
- Raises exception if API key is not configured

**get_youtube_video_duration(youtube_video_url)**
- Gets video duration in ISO 8601 format (e.g., "PT5M30S")
- Automatically extracts video ID from URL
- Fetches data from YouTube Data API v3
- Returns duration string or None if unable to retrieve
- Logs errors to rollbar on failure

## Constants

```python
from htk.lib.google.youtube.constants import (
    GOOGLE_APIS_YOUTUBE_BASE_URL,
    GOOGLE_APIS_YOUTUBE_VIDEOS_URL,
)
```

- `GOOGLE_APIS_YOUTUBE_BASE_URL` - Base URL for YouTube Data API v3
- `GOOGLE_APIS_YOUTUBE_VIDEOS_URL` - Videos endpoint URL

## Example Usage

```python
from htk.lib.google.youtube.utils import (
    extract_youtube_video_id,
    get_youtube_video_duration,
)

# Extract video ID from URL
video_id = extract_youtube_video_id('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

# Get video duration
duration = get_youtube_video_duration('https://youtu.be/dQw4w9WgXcQ')
# Returns: "PT3M32S" (3 minutes 32 seconds)
```

## Configuration

```python
# settings.py
HTK_GOOGLE_SERVER_API_KEY = ['your_api_key', ...]
```

- `HTK_GOOGLE_SERVER_API_KEY` - List of Google API keys with YouTube Data API access enabled
