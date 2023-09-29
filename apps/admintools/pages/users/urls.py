from htk.apps.admintools.utils import admintool_path
from htk.apps.admintools.pages.users import views

app_name = 'users'
urlpatterns = [
    admintool_path(
        r'^$',
        views.UsersView.as_view(),
        name='index',
        index=True,
    ),
    admintool_path(
        r'(?P<user_id>\d+)$',
        views.UserView.as_view(),
        name='info',
        label='User Detail',
        icon='User',
    ),
]
