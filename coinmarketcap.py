import requests, bs4
import apikeys
# from bittrex import bittrex
from bittrex.bittrex import Bittrex
import krakenex

# Will use across Kraken, Bittrex, Poloniex
all_kraken_coins = ['XRP', 'ETC', 'DOGE', 'BTC', 'MLN', 'ZEC', 'BCH', 'DASH', 'ICN', 'USDT', 'EOS', 'REP', 'XLM', 'XMR', 'LTC', 'GNO', 'ETH']
all_poloniex_coins = ['NXT', 'STEEM', 'LSK', 'VIA', 'RIC', 'NXC', 'EMC2', 'XPM', 'XEM', 'PINK', 'ARDR', 'PPC', 'ETH', 'LBC', 'BURST', 'DOGE', 'OMNI', 'XVC', 'BLK', 'DASH', 'STR', 'DCR', 'ZRX', 'NEOS', 'NAV', 'DGB', 'XMR', 'RADS', 'GAME', 'LTC', 'NAUT', 'BTS', 'GNO', 'VTC', 'BELA', 'XBC', 'FLDC', 'BTC', 'ZEC', 'BCH', 'FLO', 'VRC', 'NMC', 'SJCX', 'XRP', 'STRAT', 'ETC', 'FCT', 'SYS', 'XCP', 'GRC', 'BCY', 'EXP', 'PASC', 'MAID', 'BTM', 'SC', 'NOTE', 'BTCD', 'SBD', 'POT', 'BCN', 'REP', 'CLAM', 'HUC', 'GNT', 'AMP']
all_bittrex_coins = ['STEEM', 'EDG', 'VIA', 'DYN', 'SNT', 'PART', 'ENRG', 'APX', 'OK', 'RBY', 'HKG', 'IOC', 'QTUM', 'COVAL', 'BURST', 'RDD', 'MONA', 'GRS', 'BAY', 'CANN', 'OMNI', 'LMC', 'MUSIC', 'CPC', 'XAUR', 'PTOY', 'BYC', 'AEON', 'QWARK', 'DGD', 'BITB', 'TRIG', 'TKN', 'EBST', 'PAY', 'XMY', 'VRC', 'VTR', 'LGD', 'DCT', 'GOLOS', 'GRC', 'SYNX', 'FCT', 'NMR', 'XCP', 'FTC', 'IOP', 'XDN', 'EXP', 'MLN', 'MCO', 'KORE', 'NBT', 'DMD', 'ZCL', 'AMP', 'SNRG', 'NXT', 'ZEN', 'TRST', 'NXC', 'GCR', 'SLS', 'HMQ', 'BRK', 'XZC', 'START', 'CLUB', 'LBC', 'THC', 'ADX', 'DOGE', 'EMC', 'DAR', 'UNO', 'CURE', 'BRX', 'TX', 'UBQ', 'NAV', 'DGB', 'XMR', 'NEOS', 'RADS', 'CFI', 'FLDC', 'DRACO', 'XWC', 'GAM', 'GLD', 'UNB', 'RLC', 'VRM', 'ERC', 'XRP', 'STRAT', 'ETC', 'LUN', 'SAFEX', 'PTC', 'MAID', 'SC', 'SBD', 'BTCD', 'XLM', 'SPHR', 'MYST', 'GNT', 'CLAM', 'LSK', 'EMC2', 'CRB', 'SWIFT', 'NXS', 'DOPE', 'TRUST', 'ARK', 'PPC', 'GBG', 'BSD', 'XVC', 'GBYTE', 'MTL', 'NLG', 'BLK', 'DCR', 'BLITZ', 'EXCL', 'GAME', 'FUN', 'BTS', 'PDC', 'CRW', 'BTA', 'PKB', 'BTC', 'WAVES', 'ZEC', 'FLO', 'DTB', 'INCNT', 'SHIFT', 'TIME', 'SYS', 'XMG', 'BAT', 'NEO', 'POT', 'BCC', 'XEL', 'REP', '2GIVE', 'XST', 'VOX', 'CVC', 'RISE', 'CLOAK', 'OMG', 'PIVX', 'XEM', 'PINK', 'ARDR', 'GEO', 'SNGLS', 'ETH', 'WINGS', 'INFX', 'DASH', 'STORJ', '1ST', 'MEME', 'GUP', 'AGRS', 'SLR', 'SWT', 'LTC', 'GNO', 'QRL', 'ABY', 'VTC', 'EGC', 'SEQ', 'AUR', 'XBB', 'TKS', 'KMD', 'BNT', 'SPR', 'XVG', 'BCY', 'ION', 'MUE', 'FAIR', 'ANT', 'EFL', 'ADT', 'SIB', 'BLOCK']

# Get keys from apikeys.py
bittrex_key = apikeys.bittrex_key
bittrex_secret = apikeys.bittrex_secret 
poloniex_key = apikeys.poloniex_key 
poloniex_secret = apikeys.poloniex_secret
kraken_key = apikeys.kraken_key
kraken_secret = apikeys.kraken_secret

# APIs
kraken_api = krakenex.API()
kraken_api.load_key('kraken.key') #This needs to be changed
poloniex_api = poloniex.Poloniex(key=poloniex_key, secret=poloniex_secret)
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
poloniex_coins = []
bittrex_coins = []

top_twenty_codes = list(top_twenty.keys())

for code in top_twenty_codes:
    if code in all_kraken_coins:
        kraken_coins.append(code)
    elif code in all_poloniex_coins:
        poloniex_coins.append(code)
    elif code in all_bittrex_coins:
        bittrex_coins.append(code)
    else:
        print(top_twenty[code] + ' is not in any exchange')

# Calculate percent of total investment to tranfer to each exchange
total_coin_number = len(kraken_coins) + len(poloniex_coins) + len(bittrex_coins) # + len(extras) = 20 hopefully
kraken_percent = len(kraken_coins)/total_coin_number 
poloniex_percent = len(poloniex_coins)/total_coin_number 
bittrex_percent = len(bittrex_coins)/total_coin_number 


# Function to find out how much was invested
total_investment = raw_input('How much (in BTC) have you invested?')
print('We will transfer ' + str(kraken_percent) + '%% to kraken, ' + str(poloniex_percent) + ' to Poloniex, and ' + str(bittrex_percent) + ' to Bittrex')


# Function to transfer from kraken (https://www.kraken.com/help/api#private-user-data)
def transfer(amount, address):
    kraken_api.query_private('Withdraw',
    {'asset' = asset being withdrawn # Need to work out what this is
    'key' = withdrawal key name, # Need to work out what this is
    'amount' = amount to withdraw, including fees})


# Function to transfer P_n/TCN to Poloniex (https://github.com/s4w3d0ff/python-poloniex/blob/4c0f8c865f75b006e2759fc69f3e1c607cc541a7/poloniex/__init__.py)
poloniex_deposit_address = poloniex_api.returnDepositAddresses() # This needs to be finished once we're verified
poloniex_amount = poloniex_percent*total_investment # Decimal points needs to be limited here
transfer(poloniex_amount,deposit_address)


# Function to transfer B_n/TCN to Bittrex (https://github.com/ndri/python-bittrex)
bittrex_deposit_address = bittrex_api.getdepositaddress('BTC')
bittrex_amount = bittrex_percent*total_investment # Decimal points needs to be limited here
transfer(bittrex_amount,deposit_address)


# Function to make Kraken orders (https://www.kraken.com/help/api)
kraken_amount = kraken_percent*total_investment
kraken_individual_amount = kraken_amount/len(kraken_invest)

def kraken_orders(amount,currency): # BTC needs to be changed to XBT, Amount = amount in btc
    kraken_api.query_private('AddOrder',
                {'pair': 'XXBTZ' + currency,
                 'type': 'sell',
                 'ordertype': 'market',
                 'volume': amount})

# Function to make Poloniex orders (https://poloniex.com/support/api/)
poloniex_individual_amount = poloniex_amount/len(poloniex_invest)

def poloniex_orders(amount,currency):
    rate = # suss this
    poloniex_api.buy('BTC' + currency, rate, amount, orderType=False) # Fix the currency pair and rate. Note that this is a limit buy. Make sure amount is correct


# Function to make Bittrex orders (https://bittrex.com/home/api)
bittrex_individual_amount = bittrex_amount/len(bittrex_invest)

def bittrex_orders(amount,currency):
    bittrex_api.buymarket(currency, amount) # Fix currency and amount

# Buying Kraken coins
for coin in kraken_coins:
    kraken_orders(kraken_amount,coin)

# Buying Poloniex coins
for coin in poloniex_coins:
    poloniex_orders(poloniex_amount,coin)

# Buying Bittrex coins
for coin in kraken_coins:
    bittrex_orders(bittrex_amount,coin)

