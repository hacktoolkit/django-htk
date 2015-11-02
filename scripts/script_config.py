# script_config.py
# shared settings for standalone scripts hooking into Django

import os
import sys

sys.stdout = sys.stderr

SCRIPTS_DIR = os.path.dirname(__file__)
sys.path.append(os.path.realpath(os.path.join(SCRIPTS_DIR, '..', '..').replace('\\', '/')))
sys.path.append(os.path.realpath(os.path.join(SCRIPTS_DIR, '..', '..', '..').replace('\\', '/')))

import django_settings_module
# Requires a django_settings_module.py at the project's top-level directory
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'YOURAPP.settings')

import django
django.setup()

from django.db.models.loading import cache as model_cache
if not model_cache.loaded:
    model_cache.get_models()
