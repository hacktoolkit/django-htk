# Migrations

Database schema migrations and version control.

## Overview

This directory contains database migration files that track schema changes over time. Migrations are executed in order to evolve the database structure while preserving data.

## Migration Files

Each migration file represents a specific change to the database schema:

```
migrations/
├── 0001_initial.py        # Initial schema creation
├── 0002_add_field.py      # Add new field
├── 0003_remove_field.py   # Remove deprecated field
└── ...
```

## Running Migrations

### Apply All Migrations

```bash
python manage.py migrate
```

### Apply Specific App

```bash
python manage.py migrate [app_name]
```

### Create New Migration

```bash
python manage.py makemigrations [app_name]
```

### Show Migration Status

```bash
python manage.py showmigrations
```

### Rollback Migrations

```bash
# Rollback to specific migration
python manage.py migrate [app_name] [migration_number]

# Rollback all migrations for an app
python manage.py migrate [app_name] zero
```

## Creating Migrations

### From Model Changes

```bash
# After modifying models.py, create a migration
python manage.py makemigrations

# Review the generated migration before applying
python manage.py showmigrations

# Apply the migration
python manage.py migrate
```

### Manual Migrations

For complex operations, create data migrations:

```bash
python manage.py makemigrations --empty [app_name] --name [description]
```

## Best Practices

1. **Create descriptive names** - Use meaningful migration names
2. **Review before applying** - Always check migrations before running
3. **Keep migrations small** - Easier to debug and reverse if needed
4. **Test in development** - Always test migrations locally first
5. **Back up production** - Before applying migrations to production
6. **Use data migrations** - For complex data transformations
7. **Document changes** - Add comments explaining why changes were made

## Related Modules

- Django migrations documentation
- Database schema documentation
