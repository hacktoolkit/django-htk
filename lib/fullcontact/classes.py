class FullContactObject(object):
    def __init__(self, *args, **kwargs):
        pass

class FullContactPerson(FullContactObject):
    def __init__(self, email, person_data, *args, **kwargs):
        self.email = email
        self.data = person_data

    def as_slack(self):
        """Formats this person's data as a Slack string
        """
        from collections import defaultdict
        demographics = self.data.get('demographics', {})
        contact_info = self.data['contactInfo']
        values = defaultdict(lambda: 'N/A')
        values.update(contact_info)
        values.update(demographics)
        values.update(demographics.get('locationDeduced', {}))
        values['websites'] = '\n'.join([website['url'] for website in contact_info['websites']]) if 'websites' in contact_info else 'None'

        basics_rendered = """%(fullName)s (%(familyName)s, %(givenName)s)
Age: %(age)s (%(ageRange)s), Gender: %(gender)s
General Location: %(locationGeneral)s / Deduced Location: %(normalizedLocation)s

Websites:
%(websites)s
""" % values

        photos_rendered = '\n'.join([photo['url'] for photo in self.data['photos']]) if 'photos' in self.data else 'None'
        social_rendered = '\n'.join(['*%(typeName)s*: %(url)s' % social for social in self.data['socialProfiles']]) if 'socialProfiles' in self.data else 'None'

        def format_org(org):
            d_org = defaultdict(lambda: 'N/A')
            d_org.update(org)
            _s = '%(name)s - %(title)s (%(startDate)s - %(endDate)s)' % d_org
            return _s
        orgs_rendered = '\n'.join([format_org(org) for org in self.data['organizations']]) if 'organizations' in self.data else 'None'

        s = """*Basic Information*:
%(basics_rendered)s

*Photos*:
%(photos_rendered)s

*Social Profiles*:
%(social_rendered)s

*Organizations*:
%(orgs_rendered)s
""" % {
    'basics_rendered' : basics_rendered,
    'photos_rendered' : photos_rendered,
    'social_rendered' : social_rendered,
    'orgs_rendered' : orgs_rendered,
 }
        return s
