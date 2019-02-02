# HTK Imports
from htk.utils import resolve_model_dynamically


class HtkBaseService(object):
    def __init__(self, *args, **kwargs):
        pass

    def init_model(self, module_str):
        model = resolve_model_dynamically(module_str)

        assert model is not None

        self.model = model
