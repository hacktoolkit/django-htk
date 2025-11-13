# Management

Django management commands for this module.

## Overview

This management module provides Django management commands for administrative tasks, background jobs, data maintenance, and system operations.

## Management Commands

Management commands are executed using `python manage.py [command_name]`:

```bash
# List all management commands for this module
python manage.py help

# Run a specific command
python manage.py [command_name] [options]
```

## Available Commands

Check the `commands/` subdirectory for available management commands. Each command typically provides:

- **Command name** - Identifier for execution
- **Arguments** - Required positional parameters
- **Options** - Optional flags (--flag, -f)
- **Help text** - Run with `--help` for details

```bash
python manage.py [command_name] --help
```

## Running Commands

### Execute Command

```bash
python manage.py [command_name]
```

### With Arguments

```bash
python manage.py [command_name] arg1 arg2
```

### With Options

```bash
python manage.py [command_name] --option value
```

### Scheduled Execution

Commands can be scheduled via cron or task queue:

```python
# Using celery beat
from celery.schedules import crontab

app.conf.beat_schedule = {
    'command-name': {
        'task': 'module.tasks.run_management_command',
        'schedule': crontab(hour=2, minute=0),
        'args': ('command_name',)
    },
}
```

## Best Practices

1. **Keep commands focused** - One responsibility per command
2. **Provide helpful output** - Use `self.stdout.write()` for user feedback
3. **Handle errors gracefully** - Use proper exception handling
4. **Add --dry-run option** - For commands that modify data
5. **Document parameters** - Clear help text and argument descriptions
6. **Make commands idempotent** - Safe to run multiple times
7. **Use verbosity flags** - Support --verbosity for different output levels
