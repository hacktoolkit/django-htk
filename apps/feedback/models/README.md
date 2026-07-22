# Feedback Models

This package contains one Django model per file for the feedback app.

## Contents

- `feedback_legacy.py` — legacy `Feedback` contact-form model that remains under the `htk` app label.
- `feedback.py` — `FeedbackRequest`, the central reviewable feature/bug/content/support item.
- `vote.py` — `FeedbackRequestVote`, authenticated user upvote/downvote records.
- `comment.py` — `FeedbackRequestComment`, public or internal request discussion.
- `__init__.py` — explicit public imports so Django and downstream callers can import from `htk.apps.feedback.models`.

## Convention

For new Django apps/modules in `django-htk`, prefer a `models/` package with focused files when there is more than one model or when the model set is expected to grow. Keep `__init__.py` explicit and stable; do not rely on wildcard filesystem imports.
