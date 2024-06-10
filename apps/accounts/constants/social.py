# Python Standard Library Imports
from dataclasses import dataclass


@dataclass
class SocialAuth:
    provider: str
    name: str
    bg_color: str = '#000000'
    connected: bool = False

    @property
    def icon(self):
        return f'fa-{self.provider.split("-")[0]}'

    def with_status(self, connected):
        return SocialAuth(
            provider=self.provider,
            name=self.name,
            bg_color=self.bg_color,
            connected=connected,
        )


# ordered lists of social auths
SOCIAL_AUTHS = [
    SocialAuth(provider='discord', name='Discord', bg_color='#7289da'),
    SocialAuth(provider='facebook', name='Facebook', bg_color='#3b5998'),
    SocialAuth(provider='github', name='GitHub', bg_color='#333333'),
    SocialAuth(provider='google-oauth2', name='Google', bg_color='#4285f4'),
    SocialAuth(provider='linkedin-oauth2', name='LinkedIn', bg_color='#0077b5'),
    SocialAuth(provider='strava', name='Strava', bg_color='#fc4c02'),
    SocialAuth(provider='twitter', name='Twitter', bg_color='#1da1f2'),
]
