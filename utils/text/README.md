# Text

## Functions
- **`levenshtein_distance`** (text/algorithms.py) - The Levenshtein distance algorithm that compares two words
- **`get_closest_dict_words`** (text/algorithms.py) - Uses the Levenshtein distance for Word Autocompletion and Autocorrection
- **`html2markdown`** (text/converters.py) - Converts `html` to Markdown-formatted text
- **`markdown2slack`** (text/converters.py) - Converts Markdown-formatted text to Slack-formatted text
- **`oxford_comma`** (text/english.py) - Given a list of items, properly comma and 'and' or 'or' them together
- **`pluralize_noun`** (text/english.py) - Adds 's' to `noun` depending on `count`
- **`pluralize_verb`** (text/english.py) - Adds 's' to `verb` for singular `n_subjects`
- **`replace_many`** (text/general.py) - Allows to perform several string substitutions.
- **`phonenumber`** (text/pretty.py) - Formats a phone number for a country
- **`sanitize_cookie_value`** (text/sanitizers.py) - Sanitize Cookie Value
- **`get_symbols`** (text/transformers.py) - Returns a list of symbols from a sentence
- **`get_sentences`** (text/transformers.py) - Returns a list of sentences from a paragraph
- **`summarize`** (text/transformers.py) - Returns a summary of a paragraph
- **`ellipsize`** (text/transformers.py) - Cut `text` off at `max_len` characters, inserting an ellipsis at the appropriate point so that
- **`seo_tokenize`** (text/transformers.py) - Get SEO-tokenized version of a string, typically a name or title
- **`snake_case_to_camel_case`** (text/transformers.py) - Convert `snake_case` string to `CamelCase`
- **`snake_case_to_lower_camel_case`** (text/transformers.py) - Convert `snake_case` string to `camelCase`
- **`pascal_case_to_snake_case`** (text/transformers.py) - Convert `PascalCase` string to `snake_case`
- **`demojize`** (text/unicode.py) - Strips emojis from a string
- **`unicode_to_ascii`** (text/unicode.py) - Converts a Unicode string to ASCII equivalent if possible
