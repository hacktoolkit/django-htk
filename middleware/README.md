# Middleware

## Exports
- `AllowedHostsMiddleware`
- `GlobalRequestMiddleware`
- `RequestDataTooBigMiddleware`
- `RequestTimerMiddleware`
- `RewriteJsonResponseContentTypeMiddleware`
- `TimezoneMiddleware`
- `UserAgentMiddleware`

## Classes
- **`GlobalRequestMiddleware`** (middleware/classes.py) - Stores the request object so that it is accessible globally
- **`AllowedHostsMiddleware`** (middleware/classes.py) - Checks that host is inside ALLOWED_HOST_REGEXPS
- **`RequestTimerMiddleware`** (middleware/classes.py) - Timer to observe how long a request takes to process
- **`RewriteJsonResponseContentTypeMiddleware`** (middleware/classes.py) - This middleware exists because IE is a stupid browser and tries to
- **`HttpErrorResponseMiddleware`** (middleware/classes.py) - This middleware allows `HttpErrorResponseError`s to be thrown
- **`UserAgentMiddleware`** (middleware/classes.py) - Middleware to parse the user agent and add it to the request object.
