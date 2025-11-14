# Text Utilities

String manipulation, formatting, and text processing.

## Quick Start

```python
from htk.utils.text.algorithms import levenshtein_distance, get_closest_dict_words
from htk.utils.text.converters import html2markdown, markdown2slack
from htk.utils.text.english import oxford_comma, pluralize_noun
from htk.utils.text.transformers import seo_tokenize, snake_case_to_camel_case

# String distance and autocorrect
distance = levenshtein_distance('kitten', 'sitting')  # 3
suggestions = get_closest_dict_words('speling', word_dict)

# Format conversions
markdown = html2markdown('<b>Hello</b> <i>World</i>')
slack_formatted = markdown2slack('**Bold** and *italic*')

# English formatting
items_list = oxford_comma(['apples', 'oranges', 'bananas'])  # "apples, oranges, and bananas"
message = f"You have {pluralize_noun('item', count)}"

# Case conversion
camel = snake_case_to_camel_case('user_name')  # 'userName'
seo_token = seo_tokenize('hello-world_2024')  # Optimized token
```

## Common Patterns

```python
# User input sanitization and formatting
from htk.utils.text.sanitizers import sanitize_cookie_value

cookie_value = sanitize_cookie_value(user_input)

# Formatting phone numbers
from htk.utils.text.pretty import phonenumber

formatted = phonenumber('2025551234', country='US')  # (202) 555-1234

# Text summarization
from htk.utils.text.transformers import ellipsize, summarize

truncated = ellipsize(long_text, max_len=100)
summary = summarize(paragraph, num_sentences=3)

# Unicode handling
from htk.utils.text.unicode import demojize, unicode_to_ascii

text_no_emoji = demojize('Hello 👋 World 🌍')
ascii_text = unicode_to_ascii('café')  # cafe
```
