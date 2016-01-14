from enum import Enum

class OrganizationType(Enum):
    UNKNOWN = 0
    COMPANY = 1
    CORPORATION = 2
    CITY = 10
    COUNTY = 11
    STATE = 12
    GOVERNMENT_AGENCY = 20
    GROUP = 30
    HOA = 40
    HOA_CONDOS = 41
    HOA_SFH = 42
    HOA_TOWNHOUSES = 43
    NONPROFIT_ORG = 50
    SCHOOL_DISTRICT = 60
    SCHOOL = 61
    UNIVERSITY = 62
    RELIGIOUS_INSTITUTION = 70
    CHURCH = 71
    OTHER = 90
