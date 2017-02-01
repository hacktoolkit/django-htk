def get_daily_energy_summary(egauge_id, unit='kWh'):
    from htk.constants.units import ENERGY_CONVERSION_RATES
    from htk.lib.egauge.classes import EgaugeAPI
    egauge_api = EgaugeAPI('egauge32798')
    data = egauge_api.get_stored_data()
    (used, generated,) = [-delta for delta in data['values'][1][:2]]

    # convert W*s to desired unit
    conversion = '%s_%s' % ('Ws', unit,)
    conversion_rate = ENERGY_CONVERSION_RATES[conversion]
    summary = {
        'egauge_id' : egauge_id,
        'used' : used * conversion_rate,
        'generated' : generated * conversion_rate,
        'net' : (generated - used) * conversion_rate,
    }
    return summary
