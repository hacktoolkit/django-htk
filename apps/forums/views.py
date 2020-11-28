# Django Imports
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template.context_processors import csrf
from django.urls import reverse

# HTK Imports
from htk.apps.forums.forms import MessageCreationForm
from htk.apps.forums.forms import ThreadCreationForm
from htk.apps.forums.helpers import wrap_data_forum
from htk.apps.forums.models import Forum
from htk.apps.forums.models import ForumThread
from htk.view_helpers import render_custom as _r


@login_required
def index(request):
    data = wrap_data_forum(request)
    site = data['site']
    forums = site.forums.all()
    data['forums'] = forums
    response = _r(request, 'forum/index.html', data)
    return response


@login_required
def forum(request, fid):
    data = wrap_data_forum(request)
    forum = get_object_or_404(Forum, id=fid)
    data.update(csrf(request))
    data['forum'] = forum
    thread_creation_form = ThreadCreationForm()
    data['thread_creation_form'] = thread_creation_form
    data['threads'] = forum.threads.order_by('sticky', '-updated')
    response = _r(request, 'forum/forum.html', data)
    return response


@login_required
def thread(request, tid=None):
    thread = get_object_or_404(ForumThread, id=tid)
    data = wrap_data_forum(request)
    data.update(csrf(request))
    message_creation_form = MessageCreationForm()
    data['message_creation_form'] = message_creation_form
    data['thread'] = thread
    response = _r(request, 'forum/thread.html', data)
    return response


@login_required
def thread_create(request, fid=None):
    forum = get_object_or_404(Forum, id=fid)
    data = wrap_data_forum(request)
    user = data['user']
    data.update(csrf(request))
    data['forum'] = forum
    success = False
    if request.method == 'POST':
        thread_creation_form = ThreadCreationForm(request.POST)
        if thread_creation_form.is_valid():
            thread = thread_creation_form.save(author=user, forum=forum)
            success = True
        else:
            for error in thread_creation_form.non_field_errors():
                data['errors'].append(error)
    else:
        thread_creation_form = ThreadCreationForm(None)
    if success:
        response = redirect(reverse('forum_thread', args=(thread.id,)))
    else:
        data['forms'].append(thread_creation_form)
        data['thread_creation_form'] = thread_creation_form
        response = _r(request, 'forum/thread_create.html', data)
    return response


@login_required
def message_create(request, tid=None):
    thread = get_object_or_404(ForumThread, id=tid)
    data = wrap_data_forum(request)
    data['thread'] = thread
    user = data['user']
    data.update(csrf(request))
    success = False
    if request.method == 'POST':
        message_creation_form = MessageCreationForm(request.POST)
        if message_creation_form.is_valid():
            message = message_creation_form.save(author=user, thread=thread)
            success = True
        else:
            for error in auth_form.non_field_errors():
                data['errors'].append(error)
    else:
        message_creation_form = MessageCreationForm(None)
    if success:
        response = redirect(reverse('forum_thread', args=(thread.id,)))
    else:
        data['message_creation_form'] = message_creation_form
        response = _r(request, 'forum/message_create.html', data)

    return response
