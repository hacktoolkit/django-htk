def get_property_value(property_id, listing_id=None):
    from htk.lib.redfin.classes import RedfinAPI
    api = RedfinAPI()
    avm = api.get_avm(property_id, listing_id=listing_id)
    value = avm.get('payload', {}).get('predictedValue', 0)
    return value
