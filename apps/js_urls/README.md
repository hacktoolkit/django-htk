# JavaScript URL Exporter
Works on Django >= 2

## Installation
Add app to `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    ...
    'htk.apps.js_urls',
    ...
]
```


Add `HTK_APPS_JS_URLS_JS_OBJECT_NAME` constant to `settings.py`

```python
HTK_APPS_JS_URLS_JS_OBJECT_NAME = 'window.Site'
```

This value will determine the accessible variable in JavaScript side.

Finally add `HTK_APPS_JS_URLS_ALLOWED` list constant to `settings.py`
```python
HTK_APPS_JS_URLS_ALLOWED = [
    'index',
]
```

List items must be URL Names defined in `urls.py`. If namespace is used it
should also needs to be included. E.G. `admintools:dashboard`

Dynamic paths will be replaced with `{0}`

Example JavaScript util for building URLs is in the `js/build_url.ts` file
