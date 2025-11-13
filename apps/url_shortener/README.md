# Url_Shortener

## Classes
- **`HTKShortUrl`** (url_shortener/models.py) - Short URL code is traditionally duosexagesimal (base 62)

## Functions
- **`pre_encode`** (url_shortener/utils.py) - Compute the pre-encoded value
- **`resolve_raw_id`** (url_shortener/utils.py) - Resolve `prepared_id` into `raw_id`
- **`generate_short_url_code`** (url_shortener/utils.py) - Generate the short url code for a `raw_id`
- **`get_recently_shortened`** (url_shortener/utils.py) - Get recently shortened URLs

## Components
**Models** (`models.py`), **Views** (`views.py`)

## URL Patterns
- `shorturl`
