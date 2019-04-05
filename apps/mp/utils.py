# Django Imports
from django.apps import apps


_model_name_cache = None


def format_model_name(cls):
	return '{}.{}'.format(cls.__module__, cls.__name__)


def get_model_by_name(clazz):
	global _model_name_cache
	if _model_name_cache is None:
		_model_name_cache = {format_model_name(model): model for model in apps.get_models()}

	model = _model_name_cache.get(clazz)
	if model:
		return model

	raise Exception("Model {} not found".format(clazz))
