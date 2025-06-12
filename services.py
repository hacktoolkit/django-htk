# HTK Imports
from htk.utils import resolve_model_dynamically


class HtkBaseService(object):
    def __init__(self, *args, **kwargs):
        pass

    def init_model(self, module_str):
        self.init_models([module_str])

    def init_models(self, module_strs):
        self.models = [resolve_model_dynamically(module_str) for module_str in module_strs]
        assert all(self.models)

        # Backwards compatibility for single model implementations
        if len(self.models) == 1:
            self.model = self.models[0]
