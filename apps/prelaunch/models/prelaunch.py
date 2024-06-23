from .base import BasePrelaunchSignup


class PrelaunchSignup(BasePrelaunchSignup):
    class Meta:
        app_label = 'htk'
        verbose_name = 'Prelaunch Signup'
