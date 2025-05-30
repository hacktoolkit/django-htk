# Python Standard Library Imports
import typing as T
from dataclasses import (
    dataclass,
    fields,
)


@dataclass
class SocialAuth:
    provider: str
    name: str
    bg_color: str = '#000000'
    fa_icon: str = ''
    connected: bool = False

    @property
    def default_icon(self):
        icon = f'fa-brands fa-{self.provider.split("-")[0]}'
        return icon

    @property
    def icon(self):
        icon = self.fa_icon or self.default_icon
        return icon

    def with_status(self, connected):
        values = {
            field.name: getattr(self, field.name) for field in fields(self)
        }
        values['connected'] = connected
        return SocialAuth(**values)


# ordered lists of social auths
SOCIAL_AUTHS = [
    SocialAuth(provider='apple-id', name='Apple', bg_color='#000000'),
    SocialAuth(provider='discord', name='Discord', bg_color='#7289da'),
    SocialAuth(provider='facebook', name='Facebook', bg_color='#3b5998'),
    SocialAuth(provider='fitbit', name='Fitbit', bg_color='#4cc2c4'),
    SocialAuth(provider='github', name='GitHub', bg_color='#333333'),
    SocialAuth(provider='google-oauth2', name='Google', bg_color='#4285f4'),
    SocialAuth(provider='linkedin-oauth2', name='LinkedIn', bg_color='#0077b5'),
    SocialAuth(provider='strava', name='Strava', bg_color='#fc4c02'),
    SocialAuth(provider='twitter', name='Twitter', bg_color='#1da1f2'),
    # https://www.withings.com/us/en/press
    SocialAuth(
        provider='withings',
        name='Withings',
        bg_color='#0f0f0f',
        fa_icon='fa-solid fa-clock-three',
    ),
]
