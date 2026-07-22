# Python Standard Library Imports
import json

# Django Imports
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse

# HTK Imports
from htk.apps.feedback.constants import FEEDBACK_REQUEST_TYPE_CHOICES
from htk.apps.feedback.constants import FEEDBACK_REQUEST_TYPE_FEATURE
from htk.apps.feedback.constants import FEEDBACK_STATUS_CHOICES
from htk.apps.feedback.constants import FEEDBACK_STATUS_DECLINED
from htk.apps.feedback.constants import FEEDBACK_STATUS_MERGED
from htk.apps.feedback.constants import FEEDBACK_STATUS_SHIPPED
from htk.apps.feedback.constants import FEEDBACK_VISIBILITY_PRIVATE
from htk.apps.feedback.constants import FEEDBACK_VISIBILITY_PUBLIC
from htk.apps.feedback.constants import FEEDBACK_VOTE_DOWN
from htk.apps.feedback.constants import FEEDBACK_VOTE_UP
from htk.apps.feedback.models import FeedbackRequest
from htk.apps.feedback.models import FeedbackRequestVote


DEFAULT_FEEDBACK_APP = 'feedback'
DEFAULT_FEEDBACK_SOURCE = 'feedback-page'
DEFAULT_FEEDBACK_TEAM_NAME = 'the team'


def parse_json_field(value):
    if not value:
        return {}
    try:
        parsed = json.loads(value)
    except (TypeError, ValueError):
        return {}
    return parsed if isinstance(parsed, dict) else {}


def get_request_user(request):
    user = getattr(request, 'user', None)
    if user is not None and user.is_authenticated:
        return user
    return None


def get_user_feedback_identity(user):
    return {
        'is_authenticated': user is not None,
    }


def build_feedback_context_json(app=DEFAULT_FEEDBACK_APP, source=DEFAULT_FEEDBACK_SOURCE, source_uri='', extra=None):
    value = {
        'app': app,
        'source': source,
        'source_uri': source_uri,
        'capture_version': 1,
    }
    if extra:
        value.update(extra)
    return json.dumps(value)


def get_visible_feedback_requests(site, user=None, query='', request_type='', status=''):
    visibility_filter = Q(visibility=FEEDBACK_VISIBILITY_PUBLIC)
    if user is not None:
        visibility_filter |= Q(created_by=user)
    qs = FeedbackRequest.objects.filter(
        visibility_filter,
        site=site,
        is_hidden=False,
        is_spam=False,
    )
    if query:
        qs = qs.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if request_type:
        qs = qs.filter(request_type=request_type)
    if status:
        qs = qs.filter(status=status)
    return qs.order_by('-votes_count', '-created_on')


def create_feedback_request_from_post(
    request,
    app=DEFAULT_FEEDBACK_APP,
    source=DEFAULT_FEEDBACK_SOURCE,
    default_visibility=FEEDBACK_VISIBILITY_PRIVATE,
):
    data = request.POST
    site = get_current_site(request)
    user = get_request_user(request)
    title = (data.get('title') or '').strip()
    description = (data.get('description') or '').strip()
    source_uri = (data.get('source_uri') or request.get_full_path()).strip()
    request_type = data.get('request_type') or FEEDBACK_REQUEST_TYPE_FEATURE

    if not title:
        raise ValueError('Please add a short title for your feedback.')
    if not description:
        raise ValueError('Please add a few details so we know what to improve.')

    context = parse_json_field(data.get('context'))
    context.setdefault('app', app)
    context.setdefault('source', source)

    feedback_request = FeedbackRequest.objects.create(
        site=site,
        request_type=request_type,
        title=title,
        description=description,
        created_by=user,
        source_uri=source_uri,
        visibility=default_visibility,
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        referrer=request.META.get('HTTP_REFERER', ''),
        context=context,
        metadata=parse_json_field(data.get('metadata')),
        needs_review=True,
    )
    if user is not None:
        feedback_request.upvote(user=user)
    return feedback_request


def handle_feedback_post(
    request,
    app=DEFAULT_FEEDBACK_APP,
    source=DEFAULT_FEEDBACK_SOURCE,
    team_name=DEFAULT_FEEDBACK_TEAM_NAME,
):
    if get_request_user(request) is None:
        messages.info(
            request,
            'Log in or create an account to send feedback to %s.' % team_name,
        )
        return None
    try:
        feedback_request = create_feedback_request_from_post(request, app=app, source=source)
    except ValueError as exc:
        messages.error(request, str(exc))
        return None
    messages.success(
        request,
        'Thank you — your feedback was sent to %s for review.' % team_name,
    )
    return feedback_request


def redirect_to_feedback_login(request, login_url_builder, team_name=DEFAULT_FEEDBACK_TEAM_NAME, next_url=None):
    if next_url is None:
        next_url = request.get_full_path()
    messages.info(
        request,
        'Log in or create an account to send feedback to %s.' % team_name,
    )
    return redirect(login_url_builder(request, next_url=next_url))


def redirect_to_feedback_request(feedback_request, feedback_url_name):
    if feedback_request is None or not feedback_request.is_public:
        return redirect(feedback_url_name)
    return redirect('%s#request-%s' % (reverse(feedback_url_name), feedback_request.id))


def decorate_feedback_requests_for_user(feedback_requests, user):
    if user is None:
        for feedback_request in feedback_requests:
            feedback_request.user_has_voted = False
            feedback_request.user_vote_value = None
            feedback_request.user_has_upvoted = False
            feedback_request.user_has_downvoted = False
            feedback_request.user_created_request = False
            feedback_request.user_vote_locked = False
        return feedback_requests

    request_ids = [feedback_request.id for feedback_request in feedback_requests]
    vote_values_by_request_id = dict(
        FeedbackRequestVote.objects.filter(
            feedback_id__in=request_ids,
            user=user,
            is_active=True,
            is_spam=False,
        ).values_list('feedback_id', 'value')
    )
    for feedback_request in feedback_requests:
        user_vote_value = vote_values_by_request_id.get(feedback_request.id)
        feedback_request.user_has_voted = user_vote_value is not None
        feedback_request.user_vote_value = user_vote_value
        feedback_request.user_has_upvoted = user_vote_value == FEEDBACK_VOTE_UP
        feedback_request.user_has_downvoted = user_vote_value == FEEDBACK_VOTE_DOWN
        feedback_request.user_created_request = feedback_request.created_by_id == user.id
        feedback_request.user_vote_locked = feedback_request.user_created_request
    return feedback_requests


def handle_feedback_vote(
    request,
    request_id,
    login_url_builder,
    feedback_url_name,
    remove=False,
    value=FEEDBACK_VOTE_UP,
    team_name=DEFAULT_FEEDBACK_TEAM_NAME,
):
    user = get_request_user(request)
    redirect_url = '%s#request-%s' % (reverse(feedback_url_name), request_id)
    if user is None:
        messages.info(
            request,
            'Log in or create an account to vote on feedback.',
        )
        return redirect(login_url_builder(request, next_url=redirect_url))

    site = get_current_site(request)
    try:
        feedback_request = FeedbackRequest.objects.get(
            id=request_id,
            site=site,
            visibility=FEEDBACK_VISIBILITY_PUBLIC,
            is_hidden=False,
            is_spam=False,
        )
    except FeedbackRequest.DoesNotExist:
        messages.error(request, 'That feedback request is no longer available.')
        return redirect(feedback_url_name)
    if feedback_request.created_by_id == user.id:
        messages.info(
            request,
            'Requests you submit stay automatically upvoted so your feedback keeps its vote signal.',
        )
        return redirect(redirect_url)

    if remove:
        feedback_request.unvote(user=user)
        messages.success(request, 'Your vote was removed.')
    else:
        feedback_request.vote(user=user, value=value)
        if value == FEEDBACK_VOTE_DOWN:
            messages.success(request, 'Your downvote was recorded.')
        else:
            messages.success(request, 'Your upvote was recorded.')
    return redirect(redirect_url)


def get_feedback_context(
    request,
    app=DEFAULT_FEEDBACK_APP,
    source=DEFAULT_FEEDBACK_SOURCE,
    limit=50,
):
    site = get_current_site(request)
    user = get_request_user(request)
    user_identity = get_user_feedback_identity(user)
    query = (request.GET.get('q') or '').strip()
    request_type = request.GET.get('type') or ''
    status = request.GET.get('status') or ''
    source_uri = request.GET.get('source_uri') or request.META.get('HTTP_REFERER', '')
    if not source_uri:
        source_uri = request.get_full_path()
    feedback_requests = list(
        get_visible_feedback_requests(
            site,
            user=user,
            query=query,
            request_type=request_type,
            status=status,
        )[:limit]
    )
    decorate_feedback_requests_for_user(feedback_requests, user)
    return {
        'feedback_requests': feedback_requests,
        'feedback_request_type_choices': FEEDBACK_REQUEST_TYPE_CHOICES,
        'feedback_status_choices': FEEDBACK_STATUS_CHOICES,
        'feedback_query': query,
        'feedback_filter_type': request_type,
        'feedback_filter_status': status,
        'feedback_source_uri': source_uri,
        'feedback_user_is_authenticated': user_identity['is_authenticated'],
        'feedback_context_json': build_feedback_context_json(
            app=app,
            source=source,
            source_uri=source_uri,
        ),
    }


def get_feedback_modal_context(
    request,
    app=DEFAULT_FEEDBACK_APP,
    source='feedback-modal',
):
    source_uri = request.get_full_path() if request is not None else ''
    user_identity = get_user_feedback_identity(get_request_user(request))
    return {
        'feedback_modal_request_type_choices': FEEDBACK_REQUEST_TYPE_CHOICES,
        'feedback_modal_source_uri': source_uri,
        'feedback_user_is_authenticated': user_identity['is_authenticated'],
        'feedback_modal_context_json': build_feedback_context_json(
            app=app,
            source=source,
            source_uri=source_uri,
        ),
    }
