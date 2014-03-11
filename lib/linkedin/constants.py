LINKEDIN_PROFILE_API_BASE_URL = 'https://api.linkedin.com/v1/people/~:(%s)?format=json'

# LinkedIn treasure trove: http://developer.linkedin.com/documents/profile-fields
LINKEDIN_PROFILE_FIELDS = [
    'id',
    'first-name',
    'last-name',
    'summary',
    'picture-url',
    'location:(name)',
    'industry',
    'headline',
    # http://developer.linkedin.com/documents/profile-fields#positions
    'positions:(id,title,summary,start-date,end-date,is-current,company)',
    # http://developer.linkedin.com/documents/profile-fields#publiCations
    'Publications:(id,title,date,url,summary)',
    # http://developer.linkedin.com/documents/profile-fields#patents
    'patents:(id,title,summary,number,date,url)',
    # http://developer.linkedin.com/documents/profile-fields#languages
    #'languages'
    # http://developer.linkedin.com/documents/profile-fields#skills
    'skills:(id,skill:(name))',
    # http://developer.linkedin.com/documents/profile-fields#educations
    'educations:(id,school-name,field-of-study,degree,start-date,end-date)',
]
