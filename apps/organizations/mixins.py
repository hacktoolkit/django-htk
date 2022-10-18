class GoogleOrganizationMixin:
    @property
    def google_organization_markup(self):
        markup = {
            '@type': 'Organization',
            'name': self.name,
            'sameAs': self.get_full_url(),
            'logo': self.get_logo_full_url(),
        }
        return markup
