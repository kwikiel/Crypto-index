import requests, bs4
import apikeys
from bittrex.bittrex import Bittrex
import krakenex
import marketDictionaries

# Will use across Kraken, Bittrex
kraken_dict = marketDictionaries.kraken
bittrex_dict = marketDictionaries.bittrex
all_kraken_coins = list(kraken_dict.keys())
all_bittrex_coins = list(bittrex_dict.keys())

# Get keys from apikeys.py
bittrex_key = apikeys.bittrex_key
bittrex_secret = apikeys.bittrex_secret 
kraken_key = apikeys.kraken_key
kraken_secret = apikeys.kraken_secret

# APIs
kraken_api = krakenex.API()
kraken_api.load_key('kraken.key')
bittrex_api = Bittrex(bittrex_key, bittrex_secret)

# Generate list of top twenty coins
url = 'https://coinmarketcap.com/all/views/all/'
print('Downloading page %s...' % url)
res = requests.get(url)
res.raise_for_status()
elements = bs4.BeautifulSoup(res.text,'html.parser')
name = elements.select('td.no-wrap.currency-name a')
symbol = elements.select('td.text-left')
top_twenty = {symbol[i].getText():name[i].getText() for i in range(20)}

# List of which coin is in which exchange
kraken_coins = []
bittrex_coins = []

top_twenty_codes = list(top_twenty.keys())

for code in top_twenty_codes:
    if code != 'BTC':
        if code in all_kraken_coins:
            kraken_coins.append(code)
        elif code in all_bittrex_coins:
            bittrex_coins.append(code)
        else:
            print(top_twenty[code] + ' is not in any exchange')

# Ignore IOTA, Tether, USDT

# Calculate percent of total investment to tranfer to each exchange
total_coin_number = len(kraken_coins) + len(bittrex_coins) + 1 # + len(extras) = 20 hopefully. The +1 is for bitcoin, which is the left over
print ('We will be investing in ' + str(total_coin_number) + ' coins today. ' + str(len(kraken_coins) + 1) + ' of these coins are on Kraken and ' + str(len(bittrex_coins)) + ' will be on Bittrex.' )
print('The coins on Kraken are: \n' )
for coin in kraken_coins:
    print(coin)

print('The coins on Bittrex are: \n' )
for coin in bittrex_coins:
    print(coin)

kraken_percent = (len(kraken_coins) + 1)/total_coin_number 
bittrex_percent = len(bittrex_coins)/total_coin_number 


# Function to find out how much was invested
total_investment = float(input('How much (in BTC) have you invested?'))
print('We will transfer ' + str(kraken_percent) + '%% to kraken, and ' + str(bittrex_percent) + '%% to Bittrex')


# # Function to transfer from kraken (https://www.kraken.com/help/api#private-user-data)
def transfer_from_kraken(asset, amount, address):
    return kraken_api.query_private('Withdraw',
    {'asset':asset, # 'XBT'
    'key':address, # 'bittrex'
    'amount':amount}) # str(bittrex_amount) Including fees


# Function to transfer B_n/TCN to Bittrex (https://github.com/ndri/python-bittrex)
bittrex_deposit_address = bittrex_api.get_deposit_address('BTC')['result']['Address']
bittrex_amount = float('%.8f'%(bittrex_percent*total_investment)) # Decimal points needs to be limited here
bittrex_individual_amount = '%.8f'%(bittrex_amount/len(bittrex_coins))
# transfer_from_kraken(bittrex_amount,bittrex_deposit_address)


# Function to make Kraken orders (https://www.kraken.com/help/api)
kraken_amount = float('%.8f'%(kraken_percent*total_investment))
kraken_individual_amount = '%.8f'%(kraken_amount/(len(kraken_coins)+1))

# If 1ETH  = 0.5XBT, then kraken_ticker('XETHXXBT') will return 0.5
def kraken_ticker(pair):
    return kraken_api.query_public('Ticker',
    {'pair':pair 
    })['result'][pair]['a'][0]

# If we want to spend kraken_amount in XBT to buy ETH, then we buy kraken_amount/kraken_ticker('XETHXXBT')
def kraken_base_amount(amount_in_xbt,ask_price):
    result = '%.8f'%(float(amount_in_xbt)/float(ask_price))
    return result

def kraken_orders(amount_in_xbt,currency_to_buy): # BTC needs to be changed to XBT, Amount = amount in btc
    pair = kraken_dict[currency_to_buy]
    ask_price = kraken_ticker(pair)
    amount = float(kraken_base_amount(amount_in_xbt,ask_price))
    return 'We are now buying ' + str(amount) + ' of ' + currency_to_buy, kraken_api.query_private('AddOrder',
                {'pair': pair,
                 'type': 'buy',
                 'ordertype': 'market',
                 'volume': amount})


# Function to make Bittrex orders (https://bittrex.com/home/api)
def bittrex_orders(amount,currency):
    rate = bittrex_api.get_ticker(bittrex_dict[currency])['result']['Ask'] # Should be using the 'ask' field (https://tonyy.in/guide-to-buying-antshares-neo-ans-on-bittrex-exchange/)
    return bittrex_api.buy_limit(bittrex_dict[currency], amount, rate)

# Need to wait for coins to be transferred before ordering
def kraken_orders_test(amount_in_xbt,currency_to_buy): # BTC needs to be changed to XBT, Amount = amount in btc
    pair = kraken_dict[currency_to_buy]
    ask_price = kraken_ticker(pair)
    amount = float(kraken_base_amount(amount_in_xbt,ask_price))
    return 'We are now buying ' + str(amount) + ' of ' + currency_to_buy, pair, amount


# Buying Kraken coins
for coin in kraken_coins:
    kraken_orders_test(kraken_individual_amount,coin)

for coin in kraken_coins[2:]:
    try:
        kraken_orders(kraken_individual_amount,coin)
    except:
        continue
# Buying Bittrex coins
# for coin in kraken_coins:
#     bittrex_orders(bittrex_amount,coin)

def kraken_info(asset):
    return kraken_api.query_private('TradeBalance',
    {'asset':asset # Need to work out what this is
    })

kraken_api.query_private('AddOrder',
                {'pair': 'XETHXXBT',
                 'type': 'buy',
                 'ordertype': 'market',
                 'volume': 0.04})



"""
Minimum volume on trades:
=========================
Augur (REP): 0.3
Bitcoin (XBT): 0.002
Bitcoin Cash (BCH): 0.002
Dash (DASH): 0.03
Dogecoin (DOGE): 3000
EOS (EOS): 3
Ethereum (ETH): 0.02
Ethereum Classic (ETC): 0.3
Gnosis (GNO): 0.03
Iconomi (ICN): 2
Litecoin (LTC): 0.1
Melon (MLN): 0.1
Monero (XMR): 0.1
Ripple (XRP): 30
Stellar Lumens (XLM): 300
Zcash (ZEC): 0.03
Tether (USDT): 5
"""