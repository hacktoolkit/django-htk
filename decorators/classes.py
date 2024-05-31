# Python Standard Library Imports
import copy
from functools import wraps

# Third Party (PyPI) Imports
import rollbar

# Django Imports
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.shortcuts import (
    get_object_or_404,
    redirect,
)

# HTK Imports
from htk.api.utils import json_response_not_found
from htk.decorators.session_keys import DEPRECATED_ROLLBAR_NOTIFIED
from htk.utils.http.errors import HttpErrorResponseError
from htk.utils.request import get_current_request
from htk.utils.text.transformers import pascal_case_to_snake_case


# isort: off


def deprecated(func):
    """Decorator for reporting deprecated function calls

    Use this decorator sparingly, because we'll be charged if we make too many Rollbar notifications
    """

    @wraps(func)
    def wrapped(*args, **kwargs):
        # try to get a request, may not always succeed
        request = get_current_request()
        # notify a maximum of once per function per request/session
        if request:
            if DEPRECATED_ROLLBAR_NOTIFIED not in request.session:
                deprecated_notifications = {}
                request.session[
                    DEPRECATED_ROLLBAR_NOTIFIED
                ] = deprecated_notifications
            deprecated_notifications = request.session[
                DEPRECATED_ROLLBAR_NOTIFIED
            ]
            key = '%s' % func
            # first get it
            already_notified = deprecated_notifications.get(key, False)
            # then mark it
            deprecated_notifications[key] = True
        else:
            already_notified = False

        if not already_notified:
            rollbar.report_message(
                'Deprecated function call warning: %s' % func,
                'warning',
                request,
            )
        return func(*args, **kwargs)

    return wrapped


class restful_obj_seo_redirect(object):
    """Decorator for redirecting a RESTful object view to its SEO canonical URL
    if not already using it
    """

    def __init__(self, cls, obj_id_key):
        self.cls = cls
        self.obj_id_key = obj_id_key

    def __call__(self, view_fn):
        @wraps(view_fn)
        def wrapped(*args, **kwargs):
            obj_id = kwargs.get(self.obj_id_key)
            obj = get_object_or_404(self.cls, id=obj_id)
            seo_title = kwargs.get('seo_title')

            if not obj.has_seo_title_match(seo_title):
                # prevent tampering of URLs
                # redirect to the canonical URL for this object
                response = redirect(obj.get_absolute_url(), permanent=True)
            else:
                # store the retrieved object to avoid re-fetching
                retrieved_key = self.cls.__name__.lower()
                kwargs[retrieved_key] = obj
                response = view_fn(*args, **kwargs)
            return response

        return wrapped


class resolve_records_from_restful_url(object):
    """Resolve Records from URL Patterns

    Decorator for resolving records from URL.

    NOTE: Each following record must be related to the previous model.

    Model Map:
    Model map is a list of tuples, where each tuple is a mapping of:
    - Model if first item, otherwise relation
    - Path Arg Name
    - Field name
    - Extra filters (Optional)

    NOTE: If the first model is being provided from a previous decorator, you should
    only provide kwargs key and nothing else.

    In extra filters if current user must be used, value should be set to
    `__current_user__`.

    Example with standard usage:
    @resolve_records_from_restful_url(
        (Organization, 'id', 'organization_id', {'is_active': True, 'user': '__current_user__'}),
        ('members', 'id', 'member_id'),
    )

    Example paired with another decorator:
    @require_organization_admin()
    @resolve_records_from_restful_url(
        'organization',  # organization is the kwargs key from previous decorator
        ('members', 'id', 'member_id'),
    """

    def __init__(self, model_map, content_type='text/html'):
        self.content_type = content_type
        self.model_map = []
        for index, entry in enumerate(model_map):
            if isinstance(entry, tuple):
                if len(entry) == 3:
                    # add a 4th item, `extra_filters`, to make it conform to the
                    # typical shape of `model_map`
                    # a 3-item model map entry is allowed as syntactic sugar
                    self.model_map.append(entry + ({},))
                if len(entry) == 4:
                    self.model_map.append(entry)
                else:
                    raise ValueError(
                        '[{}] Model map tuple must have 3 or 4 items, got {}'.format(
                            self._get_class_name(),
                            len(entry)
                        )
                    )
            elif isinstance(entry, str):
                if index == 0:
                    self.model_map.append(entry)
                else:
                    raise ValueError(
                        '[{}] Only first entry can be a string, got {}'.format(
                            self._get_class_name(),
                            repr(entry)
                        )
                    )
            else:
                raise ValueError(
                    '[{}] Invalid model map entry type: {}'.format(
                        self._get_class_name(),
                        type(entry)
                    )
                )

    def __call__(self, view_fn):
        @wraps(view_fn)
        def wrapped(request, *args, **kwargs):
            self.user = request.user

            # If first entry is just a string, it means we need to get the object
            # from kwargs
            if isinstance(self.model_map[0], str):
                obj = kwargs.get(self.model_map[0])
                model_map = self.model_map[1:]
            else:
                obj = None
                model_map = self.model_map

            for (
                model_or_relation,
                field,
                path_arg_name,
                extra_filters,
            ) in model_map:
                value = kwargs.get(path_arg_name)

                # Raises exception and breaks loop
                key, obj = self._resolve_object(
                    obj, model_or_relation, field, value, extra_filters
                )

                kwargs[key] = obj

            response = view_fn(request, *args, **kwargs)

            return response

        return wrapped

    def _get_class_name(self, model=None):
        if model is None:
            value = self.__class__.__name__
        elif model.__class__.__name__ == 'RelatedManager':
            value = model.model.__qualname__
        else:
            value = model.__class__.__name__

        return value

    def _resolve_object(
        self, obj, model_or_relation, field, value, extra_filters
    ):
        model = (
            model_or_relation.objects
            if obj is None
            else getattr(obj, model_or_relation)
        )

        # Since extra_filters is a dict, we need to copy it to avoid modifying
        # the original dict.
        filters = copy.deepcopy(extra_filters)
        filters.update({field: value})
        for key, value in filters.items():
            if value == '__current_user__':
                filters[key] = self.user

        try:
            obj = model.get(**filters)
        except ObjectDoesNotExist:
            response = (
                json_response_not_found()
                if self.content_type == 'application/json'
                else HttpResponseNotFound()
            )
            raise HttpErrorResponseError(response)

        key = pascal_case_to_snake_case(self._get_class_name(model))
        return key, obj


def disable_for_loaddata(signal_handler):
    """Decorator that turns off signal handlers when loading fixture data.

    See:
    - https://stackoverflow.com/a/15625121/865091
    - https://code.djangoproject.com/ticket/17880
    - https://stackoverflow.com/questions/3499791/how-do-i-prevent-fixtures-from-conflicting-with-django-post-save-signal-code  # noqa E501
    - https://docs.djangoproject.com/en/dev/ref/signals/#post-save
    """

    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        if kwargs.get('raw'):
            return
        signal_handler(*args, **kwargs)

    return wrapper
