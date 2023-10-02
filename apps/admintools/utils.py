from urllib.parse import urljoin

# Django Imports
from django.urls import (
    get_resolver,
    include,
    re_path,
)
from django.urls.resolvers import (
    URLPattern,
    URLResolver,
)

# HTK Imports
from htk.utils.js_route_serializer import _prepare_url_part


class AdminToolNamespace(object):
    """Admin Tool Namespace

    Being used to store additional data in `namespace` arg of `django.urls.include()`
    Django sees this as a normal string.

    Additional data is being used by `build_admintools_paths` function
    to get needed information like label and icon.
    """

    def __init__(self, label, icon, show_in_menu):
        self.label = label
        self.icon = icon
        self.show_in_menu = show_in_menu

    def __str__(self):
        value = self.label.lower()
        return value


def admintool_path_group(route, label, icon, group, show_in_menu):
    value = re_path(
        route,
        include(group, namespace=AdminToolNamespace(label, icon, show_in_menu)),
    )
    return value


def admintool_path(
    route,
    view,
    name,
    label=None,
    icon=None,
    index=False,
    show_in_menu=False,
    *args,
    **kwargs,
):
    value = re_path(
        route,
        view,
        name=name,
        kwargs={
            'label': label,
            'icon': icon,
            'index': index,
            'show_in_menu': show_in_menu,
        },
        *args,
        **kwargs,
    )
    return value


def build_admintools_paths(
    resolver=None, url_prefix=None, namespace=None, icon=None, label=None
):
    resolver = (
        resolver if resolver else get_resolver('htk.apps.admintools.pages.urls')
    )
    paths = []
    current_namespace = (
        f'{namespace}:{resolver.namespace}' if namespace else resolver.namespace
    )
    for url_pattern in resolver.url_patterns:
        if isinstance(url_pattern, URLResolver):
            # This is only an include path. It does not have an view but loads
            # another `urls.py` file.
            url = _prepare_url_part(url_pattern)
            new_url_prefix = (
                f'/{url}'
                if url_prefix is None
                else urljoin(url_prefix or '/', url)
            )
            # TODO: Convert this to dataclass
            current = {
                'url': new_url_prefix,
                'label': url_pattern.namespace.label,
                'icon': url_pattern.namespace.icon,
                'show_in_menu': url_pattern.namespace.show_in_menu,
                'children': build_admintools_paths(
                    resolver=url_pattern,
                    url_prefix=new_url_prefix,
                    namespace=current_namespace,
                    icon=url_pattern.namespace.icon,
                    label=url_pattern.namespace.label,
                ),
            }
        elif isinstance(url_pattern, URLPattern) and url_pattern.name:
            # Only add url patterns that have a `name` defined.
            is_index = url_pattern.default_args.get('index', False)
            url = urljoin(url_prefix or '/', _prepare_url_part(url_pattern))
            api_url = f'/admintools/pages{url}'
            # TODO: Convert this to dataclass
            current = {
                'url': url_prefix if is_index else url,
                'content_url': api_url,
                'label': url_pattern.default_args.get(
                    'label', label if is_index else None
                ),
                'icon': (
                    icon
                    if is_index
                    else url_pattern.default_args.get('icon', None)
                ),
                'show_in_menu': url_pattern.default_args.get(
                    'show_in_menu', False
                ),
                'index': is_index,
            }
        else:
            current = None

        if current:
            paths.append(current)

    return paths
