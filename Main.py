from coinbase.wallet.client import Client
from coinbase.wallet.error import TwoFactorRequiredError
import time
import requests
from datetime import datetime, timedelta
import os

def marketCheck():
    test = client.get_buy_price(currency_pair = 'BTC-USD')
    print(test)
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
time_to_track = 1000
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
coin = 1
coin_value = 0
profit = 0
n = 200
running_average_n = 0
days_from_start = 0
while (end != today):
    price = r.json()['bpi'][str(end)]
    if days_from_start >= n:
        front_window_price = r.json()['bpi'][str(end-timedelta(days=n))]
        average = running_average_n/n
        print("this is n: "+str(n))
        running_average_n = running_average_n - front_window_price
        print("running_average_n: "+str(running_average_n))
        print("running average: "+str(average))
        if average > price:
            print("buy")
            coin = coin + 1
            profit = profit - price
            print("price: "+str(price))
            print("buy profit: "+str(profit))
        elif coin > 0:
            print("sell")
            coin = coin - 1
            profit = profit + price
            print("price: "+str(price))
            print("sell profit: "+str(profit))
    else:
        print("oof: "+str(days_from_start))
    running_average_n = running_average_n + price
    total = total+price
    end = end + timedelta(days=1)
    days_from_start=days_from_start+1
print("this is the profit using this algorithm: "+str(profit))
print("coins bought: "+str(coin))


# averagePrice=total/count
# print("Average price: "+str(averagePrice))
# if(float(currentPrice)>averagePrice):
#     print("Current:"+str(currentPrice)+" > Average:"+str(averagePrice))
# else:
#     print("Current:"+str(currentPrice)+" < Average:"+str(averagePrice))
