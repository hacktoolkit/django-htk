# Python Standard Library Imports
import subprocess

# Django Imports
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect

# HTK Imports
from htk.admintools.utils import retrieve_migrations
from htk.utils import (
    htk_setting,
    resolve_method_dynamically,
    resolve_model_dynamically,
)
from htk.view_helpers import render_custom as _r


# isort: off


def migrations_view(
    request,
    template='admintools/migrations.html',
    data=None,
    renderer=_r,
):
    if data is None:
        wrap_data = resolve_method_dynamically(
            htk_setting('HTK_VIEW_CONTEXT_GENERATOR')
        )
        data = wrap_data(request)

    data['migrations'] = retrieve_migrations()

    response = _r(request, template, data=data)
    return response


def migration_plan_view(
    request,
    template='admintools/migration_plan.html',
    data=None,
    renderer=_r,
):
    if request.method == 'POST':
        # Run the 'migrate' command
        result = subprocess.run(
            ['venv/bin/python', 'manage.py', 'migrate'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Get the output from the command
        migration_output = result.stdout
        error_message = result.stderr

        messages.info(request, migration_output)
        if error_message:
            messages.error(request, error_message)

        response = redirect(request.path)
    else:
        try:
            # Run the 'showmigrations --plan' command
            result = subprocess.run(
                ['venv/bin/python', 'manage.py', 'showmigrations', '--plan'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )

            # Get the output from the command
            migration_plan = result.stdout
            migrations = migration_plan.split('\n')
            num_migrations_run = len(
                [
                    migration
                    for migration in migrations
                    if migration.startswith('[X]')
                ]
            )
            num_migrations_to_apply = len(
                [
                    migration
                    for migration in migrations
                    if migration.startswith('[ ]')
                ]
            )

            data['migration_plan'] = migration_plan
            data['num_migrations_run'] = num_migrations_run
            data['num_migrations_to_apply'] = num_migrations_to_apply
        except subprocess.CalledProcessError as e:
            # Handle the error case
            error_message = f"An error occurred while fetching the migration plan: {e.stderr}"
            data['error_message'] = error_message

        response = _r(request, template, data=data)

    return response


def todos_view(
    request,
    template='admintools/todos.html',
):
    wrap_data = resolve_method_dynamically(
        htk_setting('HTK_VIEW_CONTEXT_GENERATOR')
    )
    data = wrap_data(request)

    def _build_todos_section(todos_config):
        commands = [
            'grep',
            '-n',  # display line numbers
            '-R',  # recursive
            '-C 5',  # show context, 5 lines before/after
            f'--group-separator={"~" * 10}',  # a unique string that won't occur in code
            'TODO',
        ]
        if todos_config.exclude_dirs:
            for exclude_dir in todos_config.exclude_dirs:
                commands.append(f'--exclude-dir={exclude_dir}')
        if todos_config.exclude_patterns:
            for exclude_pattern in todos_config.exclude_patterns:
                commands.append(f'--exclude={exclude_pattern}')

        commands.append(todos_config.directory)

        result = subprocess.run(commands, capture_output=True)
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

    response = _r(request, template, data=data)
    return response
