# script_config.py
# shared settings for standalone scripts hooking into Django

# Python Standard Library Imports
import os
import sys

# Django Imports
import django

import django_settings_module


sys.stdout = sys.stderr

SCRIPTS_DIR = os.path.dirname(__file__)
sys.path.append(os.path.realpath(os.path.join(SCRIPTS_DIR, '..', '..').replace('\\', '/')))
sys.path.append(os.path.realpath(os.path.join(SCRIPTS_DIR, '..', '..', '..').replace('\\', '/')))

# Requires a django_settings_module.py at the project's top-level directory
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'YOURAPP.settings')

django.setup()
