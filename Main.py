from coinbase.wallet.client import Client
from coinbase.wallet.error import TwoFactorRequiredError
import robin_stocks as r
import time
import requests
from datetime import datetime, timedelta
import os
import yfinance as yf


def marketCheck():
    test = client.get_buy_price(currency_pair = 'BTC-USD')
    print(test)

# login = r.login(os.environ['ROBINHOOD_USER'],os.environ['ROBINHOOD_PASSWORD'])
# test = r.get_current_positions()
msft = yf.Ticker("MSFT")
# print(str(msft.history(period="max")["Open"]))
# for i in msft.history(period="max")["Open"]:
#     print("oopsie: "+str(i))
buy_limit = 20
buy = 0
sell = 0
coin = 0
profit = 0
value = msft.history(period="max")["Open"]
bank = 2000
n = 50
day = 0
total_for_n = 0
days_from_start = 0
while (days_from_start < len(msft.history(period="max")["Open"])):
    price = value[days_from_start]
    if days_from_start >= n:
        front_window_price = value[days_from_start-n]
        print("yikes: "+str(front_window_price))
        average = total_for_n/n
        print("this is n: "+str(n))
        total_for_n  = total_for_n  - front_window_price
        print("running_average_n: "+str(total_for_n))
        print("running average: "+str(average))
        if average > price:
            buy = buy + 1
            profit = profit - buy_limit
            bank = bank - buy_limit
            if profit > 0:
                print("price: "+str(price))
                print("buy profit: "+str(profit))
        elif average < price:
            sell = sell + 1
            profit = profit + buy_limit
            bank = bank + buy_limit
            if profit > 0:
                print("price: "+str(price))
                print("sell profit: "+str(profit))
    total_for_n  = total_for_n  + price
    days_from_start=days_from_start+1
    print("hello?")
print("this is the profit using this algorithm: "+str(profit))
print("shares bought: "+str(coin))
print("coins value: "+str(coin*r.json()['bpi'][str(today-timedelta(days=1))]))
print("total over all value: "+str(profit+(coin*r.json()['bpi'][str(today-timedelta(days=1))])))
print("bank: "+str(bank))
print("sell: "+str(sell))
print("buy: "+str(buy))
#
coinbase_key = os.environ['COINBASE_API_KEY']
coinbase_secret = os.environ['COINBASE_API_SECRET']
print(coinbase_key)
print(coinbase_secret)
client = Client(coinbase_key, coinbase_secret)
account = client.get_primary_account()
total = 0
count = 0
averagePrice = 0
dayEstimate = 0
currentPrice = client.get_buy_price(currency_pair='BTC-USD')
currentPrice = currentPrice.get("amount")
#If this is too large it'll throw 404
time_to_track = 500
today = datetime.today().date()
print("this is today: "+str(today))
end = today - timedelta(days=time_to_track)
print("this is end: "+str(end))
"Coindesk API get request to query legacy information on day scale"
r = requests.get("https://api.coindesk.com/v1/bpi/historical/close.json?start=" + str(end) + "&end=" + str(today) + "")
print("this is response: "+str(r))
dates = r.json()['bpi'][str(end)]
print("this is the date:"+ str(dates))
#
#
buy_limit = 20
buy = 0
sell = 0
coin = 0
profit = 0
bank = 2000
n = 50
total_for_n = 0
days_from_start = 0
while (end != today):
    price = r.json()['bpi'][str(end)]
    if days_from_start >= n:
        front_window_price = r.json()['bpi'][str(end-timedelta(days=n))]
        # print("yikes: "+str(front_window_price))
        average = total_for_n/n
        # print("this is n: "+str(n))
        total_for_n  = total_for_n  - front_window_price
        # print("running_average_n: "+str(total_for_n))
        # print("running average: "+str(average))
        if average > price:
            buy = buy + 1
            coin = coin + price/(price - buy_limit)
            profit = profit - buy_limit
            bank = bank - buy_limit
            if profit > 0:
                print("price: "+str(price))
                print("buy profit: "+str(profit))
        elif average < price and coin > 0:
            sell = sell + 1
            coin = coin - price/(price - buy_limit)
            profit = profit + buy_limit
            bank = bank + buy_limit
            if profit > 0:
                print("price: "+str(price))
                print("sell profit: "+str(profit))
    total_for_n  = total_for_n  + price
    end = end + timedelta(days=1)
    days_from_start=days_from_start+1
print("this is the profit using this algorithm: "+str(profit))
print("coins bought: "+str(coin))
print("coins value: "+str(coin*r.json()['bpi'][str(today-timedelta(days=1))]))
print("total over all value: "+str(profit+(coin*r.json()['bpi'][str(today-timedelta(days=1))])))
print("bank: "+str(bank))
print("sell: "+str(sell))
print("buy: "+str(buy))
#
#
# # averagePrice=total/count
# # print("Average price: "+str(averagePrice))
# # if(float(currentPrice)>averagePrice):
# #     print("Current:"+str(currentPrice)+" > Average:"+str(averagePrice))
# # else:
# #     print("Current:"+str(currentPrice)+" < Average:"+str(averagePrice))
