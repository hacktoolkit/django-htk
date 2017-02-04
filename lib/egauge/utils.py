def get_daily_energy_usage_data(egauge_id, unit='kWh', unit_cost=0.13):
    from htk.constants.units import ENERGY_CONVERSION_RATES
    from htk.lib.egauge.classes import EgaugeAPI
    from htk.utils.currency import moneyfmt
    egauge_api = EgaugeAPI('egauge32798')
    data = egauge_api.get_stored_data()
    (used, generated,) = [-delta for delta in data['values'][1][:2]]

    # convert W*s, watt-second, to desired unit
    conversion = '%s_%s' % ('Ws', unit,)
    conversion_rate = ENERGY_CONVERSION_RATES[conversion]
    net = generated - used
    was_profitable = net > 0
    usage_data = {
        'egauge_id' : egauge_id,
        'used' : used * conversion_rate,
        'generated' : generated * conversion_rate,
        'unit' : unit,
        'net' : net * conversion_rate,
        'was_profitable' : was_profitable,
        'used_cost' : moneyfmt(used * conversion_rate * unit_cost, curr='$'),
        'saved_cost' : moneyfmt(generated * conversion_rate * unit_cost, curr='$'),
        'net_cost' : moneyfmt(net * conversion_rate * unit_cost, curr='$', neg=''),
    }
    
    return usage_data
