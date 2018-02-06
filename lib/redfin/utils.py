def get_avm(property_id, listing_id=None):
    from htk.lib.redfin.api import RedfinAPI
    api = RedfinAPI()
    avm = api.get_avm(property_id, listing_id=listing_id)
    return avm

def get_property_value(property_id, listing_id=None):
    avm = get_avm(property_id, listing_id=listing_id)
    return avm.property_value
