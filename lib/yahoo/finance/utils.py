import yahoo_finance

def get_stock_info_and_historical_data(symbol):
    """Retrieve stock info and historical data for `symbol`

    Leverages yahoo-finance for Python
    https://github.com/lukaszbanasiak/yahoo-finance
    """
    share = yahoo_finance.Share(symbol)
    info = share.get_info()
    start_date = info['start']
    end_date = info['end']
    historical = share.get_historical(start_date, end_date)
    data = {
        'info' : info,
        'historical' : historical,
    }
    return data
