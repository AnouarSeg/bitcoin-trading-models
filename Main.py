from coinbase.wallet.client import Client
from coinbase.wallet.error import TwoFactorRequiredError
import robin_stocks as r
import time
import requests
from datetime import datetime, timedelta
import os
import yfinance as yf
import tkinter
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np
# login = r.login(os.environ['ROBINHOOD_USER'],os.environ['ROBINHOOD_PASSWORD'])
# test = r.get_current_positions()

def get_stock_moving_average():
    msft = yf.Ticker("MSFT")
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
    print("this is the profit using this algorithm: "+str(profit))
    print("shares bought: "+str(coin))
    print("coins value: "+str(coin*r.json()['bpi'][str(today-timedelta(days=1))]))
    print("total over all value: "+str(profit+(coin*r.json()['bpi'][str(today-timedelta(days=1))])))
    print("bank: "+str(bank))
    print("sell: "+str(sell))
    print("buy: "+str(buy))

def bitcoin_moving_average_historical():
    items = {}
    day_to_day_bc_price = []
    day_to_day_bc_sell = []
    day_to_day_bc_buy = []
    buy_day_price = []
    days = []
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
        days.append(end)
        price = r.json()['bpi'][str(end)]
        day_to_day_bc_price.append(price)
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
                day_to_day_bc_buy.append(end)
                buy_day_price.append(price)
                if profit > 0:
                    print("price: "+str(price))
                    print("buy profit: "+str(profit))
            elif average < price and coin > 0:
                sell = sell + 1
                coin = coin - price/(price - buy_limit)
                profit = profit + buy_limit
                bank = bank + buy_limit
                day_to_day_bc_sell.append(end)
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
    items = {"prices":day_to_day_bc_price,"days":days,"buy":day_to_day_bc_buy, "buy_day_prices":buy_day_price,"sell":day_to_day_bc_sell}
    return items


root = tkinter.Tk()
root.wm_title("Embedding in Tk")
data = bitcoin_moving_average_historical()
fig = Figure(figsize=(5, 4), dpi=100)
fig.add_subplot(111).plot(data["days"],data["prices"])
buy = fig.add_subplot(111)
buy.scatter(data["buy"],data["buy_day_prices"],color='green')

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)


canvas.mpl_connect("key_press_event", on_key_press)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


button = tkinter.Button(master=root, text="Quit", command=_quit)
button.pack(side=tkinter.BOTTOM)

tkinter.mainloop()
