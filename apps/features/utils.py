# HTK Imports
from htk.utils import htk_setting
from htk.utils import resolve_model_dynamically


def get_feature_flag_model():
    FeatureFlag = resolve_model_dynamically(htk_setting('HTK_FEATURE_FLAG_MODEL'))
    return FeatureFlag


def _get_cache():
    from htk.apps.features.cachekeys import FeatureFlagCache
    c = FeatureFlagCache()
    return c


def clear_cache():
    c = _get_cache()
    c.invalidate_cache()


def get_feature_flags_map():
    c = _get_cache()

    feature_flags_map = c.get()
    if feature_flags_map is None:
        FeatureFlag = get_feature_flag_model()

        feature_flags_map = {
            feature_flag.name: True
            for feature_flag
            in FeatureFlag.objects.all()
            if feature_flag.is_enabled
        }

        c.cache_store(feature_flags_map)
    else:
        pass

    return feature_flags_map


def is_feature_enabled(feature_name):
    feature_flags_map = get_feature_flags_map()
    is_enabled = feature_flags_map.get(feature_name, False) is True
    return is_enabled
