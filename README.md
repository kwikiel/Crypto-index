Crypto-index
================

This is a basic python script which allows you to automatically divide your cryptocurrency investment across the top twenty crypto-currencies by market cap, in a similar fashion to an index fund.
It works in the following fashion:
* The user purchases the total amount they wish to invest in Bitcoin on Kraken
* Crypto-index obtains the top twenty crypto-currencies by market cap from [CoinMarketCap](https://github.com/betfair) using the BeautifulSoup module
* Lists are made of which of the top twenty coins are available on the Kraken and Bittrex exchanges
* The correct share of the initial investment is automatically transferred to Bittrex
* The top twenty cryptocurrencies are then purchased in equal shares at market price using the Bittrex and Kraken APIs

This project aims to reproduce the results achieved by [BitTwenty (BTWTY)](http://www.bittwenty.com/), but offers much more customizability, and has the advoids the need for a third party service, or third party coin which requires a liquid market.

How to use the script?
----------------------

To use the script, you will first have to fill in the apikeys.py and kraken.key files with the appropriate API keys. These can be obtained from
[Kraken](https://www.kraken.com/help/api) and [Bittrex](https://bittrex.com/home/api) respectively.

Once this is done, dependencies can be installed with

`pip3 install -r requirements.txt`

(Note that Python 3+ is required)

After this, an investment in Bitcoin needs to be made to [Kraken](https://www.kraken.com/). Once this is done, line 7 of main.py can be changed to read `real_money=True`.
The script can then be run with 

`python main.py`

Disclaimer
----------
This is intended purely as an experiment and it is not recommended that anyone pursue this for financial gain. I will not be devoting any time to maintaining this bot, and as such bugs can creep in.

This work is completely open sourced for anyone to use for any purpose they see fit. I greatly welcome any contributions to the project. If implementing my work somewhere else I simply ask that you accredit me.
