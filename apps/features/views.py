# Django Imports
from django.template.defaultfilters import date

# HTK Imports
from htk.api.utils import (
    json_response_not_found,
    json_response_okay,
)
from htk.apps.features.utils import get_feature_flag_model
from htk.view_helpers import (
    render_custom as _r,
    wrap_data,
)


# isort: off


def features_view(
    request,
    template,
    data=None,
    renderer=_r,
    api_url_name='htk_apps_features_toggle'
):
    FeatureFlag = get_feature_flag_model()

    if data is None:
        data = wrap_data(request)

    data['feature_flags'] = FeatureFlag.objects.all()
    data['api_url_name'] = api_url_name

    response = renderer(request, template, data)
    return response


def features_toggle_view(request, feature_id):
    FeatureFlag = get_feature_flag_model()
    try:
        feature_flag = FeatureFlag.objects.get(id=feature_id)
    except FeatureFlag.DoesNotExist:
        feature_flag = None

    if feature_flag is None:
        response = json_response_not_found()
    else:
        feature_flag.enabled = not feature_flag.enabled
        feature_flag.save()
        response = json_response_okay(
            {
                'enabled': feature_flag.enabled,
                'updated_at': date(feature_flag.updated_at),
            }
        )

    return response
