# HTK Imports
from htk.apps.admintools.utils import admintool_path_group


app_name = 'admintools'
urlpatterns = [
    admintool_path_group(
        r'^users/',
        'Users',
        'users',
        'htk.apps.admintools.pages.users.urls',
        show_in_menu=True,
    ),
]
