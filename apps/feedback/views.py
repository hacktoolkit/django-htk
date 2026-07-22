# Python Standard Library Imports
import json

# Django Imports
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST

# HTK Imports
from htk.api.constants import *
from htk.api.utils import json_response_error
from htk.api.utils import json_response_form_error
from htk.api.utils import json_response_not_found
from htk.api.utils import json_response_okay
from htk.apps.feedback.constants import *
from htk.apps.feedback.forms import FeedbackForm
from htk.apps.feedback.models import FeedbackRequest
from htk.apps.feedback.models import FeedbackRequestComment


@require_POST
def submit(request):
    success = False

    antispam = request.POST.get(HTK_API_KEY_ANTISPAM) == HTK_API_VALUE_ANTISPAM_CHALLENGE_RESPONSE
    feedback_form = FeedbackForm(request.POST)
    if antispam and feedback_form.is_valid():
        site = get_current_site(request)
        success = True
        feedback = feedback_form.save(site, request)
    data = {}
    if success:
        response = json_response_okay()
    else:
        response = json_response_error()
    return response


def _request_user(request):
    user = getattr(request, 'user', None)
    if user is not None and user.is_authenticated:
        return user
    return None


def _value(value):
    return (value or '').strip()


def _json_body(request):
    if not request.body:
        return {}
    try:
        body = json.loads(request.body.decode('utf-8'))
    except (TypeError, ValueError):
        body = {}
    return body


def _payload(request):
    content_type = request.META.get('CONTENT_TYPE', '')
    body = _json_body(request) if content_type.startswith('application/json') else {}
    data = {}
    data.update(request.POST.dict())
    data.update(body)
    return data


def _json_value(value, default=None):
    if default is None:
        default = {}
    if value in (None, ''):
        return default
    if isinstance(value, (dict, list)):
        return value
    try:
        return json.loads(value)
    except (TypeError, ValueError):
        return default


def _bool_value(value, default=False):
    if value in (None, ''):
        return default
    if isinstance(value, bool):
        return value
    return str(value).lower() in ('1', 'true', 'yes', 'on')


def _visibility_value(value, user=None):
    visibility_values = {choice[0] for choice in FEEDBACK_VISIBILITY_CHOICES}
    visibility = value if value in visibility_values else FEEDBACK_VISIBILITY_PRIVATE
    is_staff = user is not None and user.is_staff
    if visibility == FEEDBACK_VISIBILITY_PUBLIC and not is_staff:
        return FEEDBACK_VISIBILITY_PRIVATE
    return visibility


def _needs_review_value(value, user=None):
    is_staff = user is not None and user.is_staff
    if not is_staff:
        return True
    return _bool_value(value, True)


def _int_value(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default




def _vote_value(data):
    direction = (data.get('direction') or data.get('vote') or '').strip().lower()
    if direction in ('down', 'downvote', '-1'):
        return FEEDBACK_VOTE_DOWN
    if direction in ('up', 'upvote', '+1', '1'):
        return FEEDBACK_VOTE_UP
    value = _int_value(data.get('value'), FEEDBACK_VOTE_UP)
    return FEEDBACK_VOTE_DOWN if value < 0 else FEEDBACK_VOTE_UP


def _feedback_queryset(request):
    site = get_current_site(request)
    qs = FeedbackRequest.objects.filter(site=site)
    user = _request_user(request)
    is_staff = user is not None and user.is_staff
    if not is_staff:
        qs = qs.filter(
            visibility=FEEDBACK_VISIBILITY_PUBLIC,
            is_hidden=False,
            is_spam=False,
        )
    return qs


def _serialize_request(feedback_request, include_detail=False):
    data = feedback_request.json_encode()
    if include_detail:
        data.update(
            {
                'comments': [
                    comment.json_encode()
                    for comment in feedback_request.comments.filter(
                        is_hidden=False,
                        is_spam=False,
                        is_internal=False,
                    )
                ],
            }
        )
    return data


@require_GET
def request_list(request):
    qs = _feedback_queryset(request)
    data = request.GET
    request_type = data.get('type') or data.get('request_type')
    status = data.get('status')
    query = data.get('q') or data.get('query')
    order = data.get('order') or data.get('ordering') or 'popular'

    if request_type:
        qs = qs.filter(request_type=request_type)
    if status:
        qs = qs.filter(status=status)
    if query:
        qs = qs.filter(Q(title__icontains=query) | Q(description__icontains=query))

    if order == 'recent':
        qs = qs.order_by('-created_on')
    elif order == 'updated':
        qs = qs.order_by('-updated_on')
    else:
        qs = qs.order_by('-votes_count', '-created_on')

    limit = min(max(_int_value(data.get('limit'), 50), 1), 100)
    offset = max(_int_value(data.get('offset'), 0), 0)
    results = list(qs[offset:offset + limit])
    response = json_response_okay(
        {
            'requests': [_serialize_request(item) for item in results],
            'limit': limit,
            'offset': offset,
            'has_more': qs.count() > offset + limit,
        }
    )
    return response


@require_GET
def request_detail(request, request_id):
    try:
        feedback_request = _feedback_queryset(request).get(id=request_id)
    except FeedbackRequest.DoesNotExist:
        return json_response_not_found()
    return json_response_okay({'request': _serialize_request(feedback_request, include_detail=True)})


@require_GET
def request_matches(request):
    query = request.GET.get('q') or request.GET.get('query') or request.GET.get('title')
    if not query:
        return json_response_okay({'requests': []})
    qs = _feedback_queryset(request).filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    ).order_by('-votes_count', '-created_on')[:10]
    return json_response_okay({'requests': [_serialize_request(item) for item in qs]})


@require_POST
def request_submit(request):
    site = get_current_site(request)
    data = _payload(request)
    title = (data.get('title') or '').strip()
    description = (data.get('description') or data.get('message') or data.get('comment') or '').strip()
    if not title:
        return json_response_error({'error': 'Missing title'})

    user = _request_user(request)
    owner = None
    source_uri = data.get('source_uri') or data.get('uri') or request.META.get('HTTP_REFERER', '')
    user_agent = data.get('user_agent') or request.META.get('HTTP_USER_AGENT', '')
    referrer = data.get('referrer') or request.META.get('HTTP_REFERER', '')
    visibility = _visibility_value(data.get('visibility'), user=user)

    feedback_request = FeedbackRequest.objects.create(
        site=site,
        request_type=data.get('type') or data.get('request_type') or FEEDBACK_REQUEST_TYPE_FEATURE,
        title=title,
        description=description,
        visibility=visibility,
        created_by=user,
        owner=owner,
        source_uri=source_uri,
        user_agent=user_agent,
        referrer=referrer,
        context=_json_value(data.get('context')),
        metadata=_json_value(data.get('metadata')),
        needs_review=_needs_review_value(data.get('needs_review'), user=user),
    )
    if user is not None:
        feedback_request.upvote(user=user)
    return json_response_okay({'request': _serialize_request(feedback_request, include_detail=True)})


@require_POST
def request_vote(request, request_id):
    try:
        feedback_request = _feedback_queryset(request).get(id=request_id)
    except FeedbackRequest.DoesNotExist:
        return json_response_not_found()
    if not feedback_request.is_open_for_voting:
        return json_response_error({'error': 'Request is closed for voting'})
    data = _payload(request)
    user = _request_user(request)
    if user is None:
        return json_response_error({'error': 'Authentication required'}, status=403)
    vote = feedback_request.vote(user=user, value=_vote_value(data))
    return json_response_okay(
        {
            'request': _serialize_request(feedback_request),
            'vote_id': vote.id if vote is not None else None,
        }
    )


@require_POST
def request_unvote(request, request_id):
    try:
        feedback_request = _feedback_queryset(request).get(id=request_id)
    except FeedbackRequest.DoesNotExist:
        return json_response_not_found()
    user = _request_user(request)
    if user is None:
        return json_response_error({'error': 'Authentication required'}, status=403)
    count = feedback_request.unvote(user=user)
    return json_response_okay({'request': _serialize_request(feedback_request), 'removed': count})


@require_POST
def request_comment(request, request_id):
    try:
        feedback_request = _feedback_queryset(request).get(id=request_id)
    except FeedbackRequest.DoesNotExist:
        return json_response_not_found()
    data = _payload(request)
    comment_text = (data.get('comment') or data.get('message') or '').strip()
    if not comment_text:
        return json_response_error({'error': 'Missing comment'})
    user = _request_user(request)
    is_internal = _bool_value(data.get('is_internal'), False)
    if is_internal and not (user is not None and user.is_staff):
        return json_response_error({'error': 'Forbidden'}, status=403)
    comment = FeedbackRequestComment.objects.create(
        feedback=feedback_request,
        user=user,
        comment=comment_text,
        is_internal=is_internal,
    )
    return json_response_okay({'comment': comment.json_encode(), 'request': _serialize_request(feedback_request)})


@require_POST
def request_status_update(request, request_id):
    user = _request_user(request)
    if user is None or not user.is_staff:
        return json_response_error({'error': 'Forbidden'}, status=403)
    try:
        feedback_request = FeedbackRequest.objects.get(id=request_id)
    except FeedbackRequest.DoesNotExist:
        return json_response_not_found()
    data = _payload(request)
    status = data.get('status')
    if status not in dict(FEEDBACK_STATUS_CHOICES):
        return json_response_error({'error': 'Invalid status'})
    feedback_request.status = status
    feedback_request.save(update_fields=('status', 'updated_on'))
    return json_response_okay({'request': _serialize_request(feedback_request)})


@login_required
@require_GET
def request_my(request):
    qs = FeedbackRequest.objects.filter(site=get_current_site(request)).filter(
        Q(created_by=request.user) | Q(votes__user=request.user)
    ).distinct().order_by('-updated_on')
    return json_response_okay({'requests': [_serialize_request(item) for item in qs]})
