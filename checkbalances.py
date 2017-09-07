import requests, bs4
import apikeys
from bittrex.bittrex import Bittrex
import krakenex
import json, requests


kraken_dict = {'XXBT': 'Btc', 'XXRP': 'xrp', 'XETH':'Eth', 'XZEC':'Zec', 'XICN':'Icn', 'XXMR':'xmr', 'DASH':'Dash', 'BCH':'bch'}


# Get keys from apikeys.py
bittrex_key = apikeys.bittrex_key
bittrex_secret = apikeys.bittrex_secret 
kraken_key = apikeys.kraken_key
kraken_secret = apikeys.kraken_secret

# APIs
kraken_api = krakenex.API()
kraken_api.load_key('kraken.key')
bittrex_api = Bittrex(bittrex_key, bittrex_secret)

def euro_price(currency,amount):
    url = 'https://api.cryptonator.com/api/ticker/' + currency +'-eur'
    resp = requests.get(url=url)
    data = json.loads(resp.text)
    price = data['ticker']['price']
    return float(amount)*float(price)

bittrex_balances_list = bittrex_api.get_balances()['result']
bittrex_balances = {item['Currency'] : item['Balance'] for item in bittrex_balances_list}
del bittrex_balances['BCC'] #BCC is missing from cryptonator

kraken_balances = kraken_api.query_private('Balance')['result']
kraken_euro_balances = {kraken_dict[item] :euro_price(kraken_dict[item],float(kraken_balances[item])) for item in kraken_balances}
bittrex_euro_balances = {item :euro_price(item,float(bittrex_balances[item])) for item in bittrex_balances}



all_euro = list(bittrex_euro_balances.values()) + list(kraken_euro_balances.values())

print('You have ' + str(sum(all_euro)) + ' euro')