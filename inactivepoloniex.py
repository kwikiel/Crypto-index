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
kraken_api.load_key('kraken.key') #This needs to be changed
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


# Calculate percent of total investment to tranfer to each exchange
total_coin_number = len(kraken_coins) + len(bittrex_coins) + 1 # + len(extras) = 20 hopefully. The +1 is for bitcoin, which is the left over
print ('We will be investing in ' + total_coin_number + 'coins today. ' + str(len(kraken_coins) + 1) + ' of these coins are on Kraken and ' + len(bittrex_coins) + ' will be on Bittrex.' )
kraken_percent = (len(kraken_coins) + 1)/total_coin_number 
bittrex_percent = len(bittrex_coins)/total_coin_number 


# Function to find out how much was invested
total_investment = float(input('How much (in BTC) have you invested?'))
print('We will transfer ' + str(kraken_percent) + '%% to kraken, and ' + str(bittrex_percent) + '%% to Bittrex')


# Function to transfer from kraken (https://www.kraken.com/help/api#private-user-data)
def transfer_from_kraken(amount, address):
    kraken_api.query_private('Withdraw',
    {'asset' = asset being withdrawn # Need to work out what this is
    'key' = withdrawal key name, # Need to work out what this is
    'amount' = amount to withdraw, including fees})

# Function to transfer B_n/TCN to Bittrex (https://github.com/ndri/python-bittrex)
bittrex_deposit_address = bittrex_api.get_deposit_address('BTC')['result']['Address']
bittrex_amount = '%.8f'%(bittrex_percent*total_investment) # Decimal points needs to be limited here
bittrex_individual_amount = '%.8f'%(bittrex_amount/len(bittrex_invest))
transfer_from_kraken(bittrex_amount,bittrex_deposit_address)

# Function to make Kraken orders (https://www.kraken.com/help/api)
kraken_amount = '%.8f'%(kraken_percent*total_investment)
kraken_individual_amount = '%.8f'%(kraken_amount/len(kraken_invest))


def kraken_orders(amount,currency): # BTC needs to be changed to XBT, Amount = amount in btc
    kraken_api.query_private('AddOrder',
                {'pair': + kraken_dict[currency],
                 'type': 'buy',
                 'ordertype': 'market',
                 'volume': amount})


# Function to make Bittrex orders (https://bittrex.com/home/api)
def bittrex_orders(amount,currency):
    rate = bittrex_api.get_ticker(bittrex_dict[currency])['result']['Ask'] # Should be using the 'ask' field (https://tonyy.in/guide-to-buying-antshares-neo-ans-on-bittrex-exchange/)
    bittrex_api.buy_limit(bittrex_dict[currency], amount, rate)

# Buying Kraken coins
for coin in kraken_coins:
    kraken_orders(kraken_amount,coin)

# Buying Bittrex coins
for coin in kraken_coins:
    bittrex_orders(bittrex_amount,coin)

