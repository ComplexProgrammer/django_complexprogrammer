import json
from django.shortcuts import render
import urllib3

def index(request):
    url = "https://tradeogre.com/api/v1/markets"
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    htmlSource = r.data
    btc_markets=[]
    usdt_markets=[]
    ltc_markets=[]
    market_type=''
    for i in json.loads(htmlSource):
        python_obj = {}
        python_obj['coin']=str(list(i)[0]).split('-')[0]
        python_obj['market']=list(i)[0]
        python_obj['initialprice']=i[list(i)[0]]['initialprice']
        python_obj['price']=i[list(i)[0]]['price']
        python_obj['high']=i[list(i)[0]]['high']
        python_obj['low']=i[list(i)[0]]['low']
        python_obj['volume']=i[list(i)[0]]['volume']
        python_obj['bid']=i[list(i)[0]]['bid']
        python_obj['ask']=i[list(i)[0]]['ask']
        market_type=str(list(i)[0]).split('-')[1]
        if market_type=='BTC':
            btc_markets.append(python_obj)
        if market_type=='USDT':
            usdt_markets.append(python_obj)
        if market_type=='LTC':
            ltc_markets.append(python_obj)
                    
    context={
        "btc_markets": btc_markets,
        "usdt_markets": usdt_markets,
        "ltc_markets": ltc_markets,
    }
    return render(request, "cryptomarket/index.html", context=context)
