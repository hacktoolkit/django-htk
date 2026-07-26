# Feedback App

Reusable feedback collection and lightweight feature-request infrastructure.

The app keeps the legacy `Feedback` contact-form model working, while adding a
small product-feedback layer for reviewable requests, votes, and comments.

## Core Concepts

### Legacy `Feedback`

`Feedback` remains a simple contact-form submission model:

```python
from htk.apps.feedback.models import Feedback

feedback = Feedback.objects.create(
    site=site,
    user=user,
    name='Jane',
    email='jane@example.com',
    comment='This page was confusing.',
    uri='/dashboard',
)
```

The legacy API endpoint remains available:

```
POST /feedback/submit
```

### `FeedbackRequest`

A request is the central reviewable item: feature request, bug report, content
issue, support question, or general feedback. New requests default to `private`
and `needs_review=True`; publish them only after staff review.

```python
from htk.apps.feedback.constants import FEEDBACK_REQUEST_TYPE_FEATURE
from htk.apps.feedback.models import FeedbackRequest

feedback = FeedbackRequest.objects.create(
    site=site,
    created_by=user,
    request_type=FEEDBACK_REQUEST_TYPE_FEATURE,
    title='Add saved searches',
    description='I would like to save searches and return to them later.',
    source_uri='/search',
    context={
        'app': 'example-app',
        'surface': 'search-results',
    },
)
```

## Bug Reports: User/Page State

For bug reports, downstream apps should submit structured context that makes the
report reproducible. Keep files/uploads in the consuming app until there is a
clear shared storage policy.

Suggested generic context:

```json
{
  "app": "example-app",
  "surface": "search-results",
  "path": "/search?q=grace",
  "query": "grace",
  "viewport": {"width": 1440, "height": 900},
  "app_version": "2026.07.21"
}
```

## API Endpoints

The app uses plain Django views and HTK JSON helpers, not DRF. Existing URL
style omits trailing slashes.

### List requests

```
GET /feedback/requests?q=search&type=feature_request&status=planned&order=popular
```

Response includes public, non-hidden, non-spam requests for normal users. Staff
users may see private/hidden items.

### Find likely duplicates

```
GET /feedback/requests/matches?q=saved%20searches
```

Use this while a user is typing a title/body so they can find an existing
idea to vote on instead of creating a duplicate.

### Submit a request

```
POST /feedback/requests/submit
Content-Type: application/json

{
  "type": "feature_request",
  "title": "Add saved searches",
  "description": "I would like to save searches and return to them later.",
  "context": {
    "surface": "search-results"
  }
}
```

Form-encoded submissions are also supported. Public-facing submissions default
to `visibility=private` and `needs_review=true`; non-staff users cannot
self-publish by passing `visibility=public`. Staff may intentionally set
`visibility=public` and `needs_review=false` after review.

### Detail

```
GET /feedback/requests/<id>
```

Returns the request plus public comments.

### Vote / unvote

```
POST /feedback/requests/<id>/vote
POST /feedback/requests/<id>/unvote
```

Authenticated users can vote once per request, with `value=1` for an upvote
and `value=-1` for a downvote. Omitting `value` preserves legacy upvote
behavior. Anonymous voting is intentionally not supported; require login so
the vote row only needs a `user` FK.

### Comment

```
POST /feedback/requests/<id>/comment
```

Public comments are available by default. Staff users may pass
`is_internal=true` for staff-only comments.

### Staff status update

```
POST /feedback/requests/<id>/status
```

Staff-only. Changes the request status directly.

### My requests

```
GET /feedback/requests/my
```

Authenticated users can see requests they created or voted for.

## Admin

The feature-request models live in the Django admin under **Htk Feedback** so downstream apps can use the shared HTK feedback infrastructure without making the models look product-owned.

The legacy `Feedback` contact-form model is registered in admin by default for backward compatibility. Downstream apps that only want the request/vote/comment surface can hide it with:

```python
HTK_FEEDBACK_ENABLE_LEGACY_ADMIN = False
```

This setting only controls admin registration for the legacy model; it does not change migrations, tables, or public imports.

## Model File Layout

Feedback uses the standard multi-model app package layout:

```text
models/
├── __init__.py
├── feedback.py
├── feedback_legacy.py
├── vote.py
└── comment.py
```

Import from `htk.apps.feedback.models` unless you specifically need an internal model file. `models/__init__.py` is the stable public surface and imports every model explicitly.

## Model Shape

- `FeedbackRequest` — idea/feature/bug/content/support/general request.
- `FeedbackRequestVote` — one active upvote/downvote row per authenticated user.
- `FeedbackRequestComment` — public or internal discussion.

## Slack Notifications

New `FeedbackRequest` submissions can post to Slack through HTK's existing Slack webhook helper. Configure the downstream app with:

```python
HTK_FEEDBACK_SLACK_ENABLED = True
HTK_FEEDBACK_SLACK_CHANNEL = '#feedback'
HTK_FEEDBACK_SLACK_USERNAME = 'Feedback'  # optional
HTK_FEEDBACK_SLACK_ICON_EMOJI = ':memo:'  # optional
```

Notifications include request type, status, visibility, submitter, source page, and a direct Django admin link built from HTK's shared model admin URL helpers.

## Integration Notes

- Keep new submissions private by default and publish only reviewed, public-safe requests.
- Keep status lightweight; add richer workflow only when a real queue needs it.
- Scope every request by `site`.
- Do not duplicate authenticated identity snapshots; use the `created_by`/`user` FKs.
- Keep anonymous request submission contact-free for now. Add app-local contact capture only when a real follow-up workflow exists.
- Use Slack notifications for quick human triage when the consuming app has a configured Slack webhook/channel.
- Use `context` JSON for app-specific page state and `metadata` JSON for staff/integration-only data.
