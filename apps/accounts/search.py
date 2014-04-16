from django.contrib.auth import get_user_model

from htk.apps.accounts.constants.search import *
from htk.apps.accounts.models import UserEmail

"""Various search functions for User objects

TODO: First retrieve from followers and following, then search all users
TODO: order results by distance from query
"""

##################################################
# Aggregating searches

def combined_user_search(query, search_functions, num_results=DEFAULT_NUM_SEARCH_RESULTS):
    """Combines result sets from multiple `search_functions` into one resultant QuerySet
    """
    UserModel = get_user_model()
    result_qs = UserModel.objects.none()
    for search_function in search_functions:
        # don't slice until the end
        result_qs |= search_function(query, num_results=0)
    if num_results:
        result_qs = result_qs[:num_results]
    return result_qs

##################################################
# Searches returning QuerySets

def search_by_username_name(query, num_results=DEFAULT_NUM_SEARCH_RESULTS):
    """Searchs for Users by username and name

    Wrapper combining search_by_username and search_by_name

    Returns a QuerySet of User objects
    """
    result_qs = combined_user_search(
        query,
        (
            search_by_username,
            search_by_name,
        ),
        num_results=num_results
    )
    return result_qs

def search_by_username(query, num_results=DEFAULT_NUM_SEARCH_RESULTS):
    """Searches for Users by username

    Returns a QuerySet of User objects
    """
    UserModel = get_user_model()

    results_by_username = UserModel.objects.filter(
        username__istartswith=query,
        profile__has_username_set=True
    )
    if num_results:
        results_by_username = results_by_username[:num_results]

    return results_by_username

def search_by_name(query, num_results=DEFAULT_NUM_SEARCH_RESULTS):
    """Search for Users by name (first name, last name)

    Returns a list of User objects
    """
    UserModel = get_user_model()

    results_by_first_name = UserModel.objects.filter(
        first_name__istartswith=query
    )

    query_parts = query.split()
    if len(query_parts) > 1:
        # there is a multi-word name or last name component in query
        results_by_last_name = UserModel.objects.filter(
            last_name__istartswith=' '.join(query_parts[1:])
        )
    else:
        results_by_last_name = UserModel.objects.filter(
            last_name__istartswith=query
        )

    results_by_name = (results_by_first_name | results_by_last_name)

    if num_results:
        results_by_name = results_by_name[:num_results]

    return results_by_name

##################################################
# Searches returning lists

def search_by_email(query, num_results=DEFAULT_NUM_SEARCH_RESULTS):
    """Search for Users by email address

    This is just experimental; suggesting users by email is a security breach as it exposes others' email addresses
    Can also be confusing

    NOTE: This function returns a list instead of a QuerySet

    Returns list of User objects
    """
    user_emails = UserEmail.objects.filter(
        is_confirmed=True,
        email__istartswith=query,
        user__profile__has_username_set=True
    )
    if num_results:
        user_emails = user_emails[:num_results]

    results_by_email = [user_email.user for user_email in user_emails]
    return results_by_email
