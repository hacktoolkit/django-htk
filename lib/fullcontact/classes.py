from collections import defaultdict


class FullContactObject(object):
    def __init__(self, *args, **kwargs):
        pass


class FullContactPerson(FullContactObject):
    def __init__(self, email, person_data, version='v3', *args, **kwargs):
        self.email = email.strip().lower()
        self.data = person_data
        self.version = version

    def as_slack(self):
        if self.version == 'v2':
            result = self.as_slack_v2()
        elif self.version == 'v3':
            result = self.as_slack_v3()
        else:
            raise Exception('Unknown FullContactPerson version')
        return result

    def as_slack_v3(self):
        """Formats this person's FullContact V3 data as a Slack string
        """
        values = defaultdict(lambda: 'N/A')
        values.update(self.data)

        details = defaultdict(lambda: 'N/A')
        details.update(self.data.get('details', {}))

        name = defaultdict(lambda: 'N/A')
        name.update(details.get('name') or {})

        values['age'] = details['age'] or 'N/A'
        values['ageRange'] = values['ageRange'] or 'N/A'
        values['organization'] = values['organization'] or 'N/A'

        values['fullName'] = name['full']
        values['familyName'] = name['family']
        values['givenName'] = name['given']

        photos = self.data.get('details', {}).get('photos', [])
        photos_rendered = '\n'.join([photo['value'] for photo in photos]) if photos else 'None'
        values['photos_rendered'] = photos_rendered

        social_profiles = details.get('profiles', {}).values()
        social_rendered = '\n'.join([
            '*{service}*: {url}'.format(**social)
            for social
            in social_profiles
        ])
        values['social_rendered'] = social_rendered

        s = """*Basic Information*:
{fullName} ({familyName}, {givenName})
Age: {age} ({ageRange}), Gender: {gender}
Location: {location}

Website: {website}

*Photos*:
{photos_rendered}

*Social Profiles*:
{social_rendered}

*Organization*: {organization}
""".format(**values)
        return s

    def as_slack_v2(self):
        """Formats this person's FullContact V2 data as a Slack string
        """
        demographics = self.data.get('demographics', {})
        contact_info = self.data.get('contactInfo', {})
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
