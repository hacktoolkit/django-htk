# Python Standard Library Imports
import subprocess

# Django Imports
from django.conf import settings

# HTK Imports
from htk.utils import (
    htk_setting,
    resolve_method_dynamically,
    resolve_model_dynamically,
)
from htk.view_helpers import render_custom as _r


def todos_view(
    request,
    template='admintools/todos.html',
):
    wrap_data = resolve_method_dynamically(
        htk_setting('HTK_VIEW_CONTEXT_GENERATOR')
    )
    data = wrap_data(request)

    def _build_todos_section(todos_config):
        result = subprocess.run(
            [
                'grep',
                '-n',  # display line numbers
                '-R',  # recursive
                '-C 5',  # show context, 5 lines before/after
                f'--group-separator={"~" * 10}',  # a unique string that won't occur in code
                'TODO',
                todos_config.directory,
            ],
            capture_output=True,
        )
        todos_groups = (
            result.stdout.decode()
            .replace(todos_config.exclusion_pattern, '')
            .split('~' * 10)
        )
        todos_section = {
            'key': todos_config.key,
            'name': todos_config.name,
            'groups': todos_groups,
        }
        return todos_section

    todos_configs = htk_setting('HTK_ADMINTOOLS_TODOS_CONFIGS')
    data['todos_sections'] = [
        _build_todos_section(todos_config) for todos_config in todos_configs
    ]
    data['has_dynamic_breadcrumbs'] = True

    response = _r(request, template, data=data)
    return response
