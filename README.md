# TradeBackTester.py
Easy to use stock strategy backtester for python users. Just import into a script with your data and 


How to use:
```
account = TradeBacktester.Account(50000)
```
this indicates that you are starting an account with $50,000

```
account.openTrade('long','AAPL',200, 0.2, datetime-Timestamp, 210, 195)
```

this is telling the account to open a trade. We tell it that we waant a long position, on AAPL at the current price (which for this example is 200 dollars).
We also have to enter the datetime timestamp, the size of the trade as a percentage of the account (20% for this example), and then the price at which we want to take profit, and price for stop loss

to close a trade, use this:

```
 if account.determineIfShouldClose(ticker, currentPrice, datetime-Timestamp, 'open'):
            account.closeTrade(ticker,currentPrice,'Open')
```

```determineIfShouldClose``` is a function that was made to determine if the current price hits the criteria for your take profit price or stop loss. It returns bool True if you should and False if not
```closeTrade``` will close the trade.

Note:
if you use closeTrade while you are beyond your stop loss price at 'open', you will lose more than your stop loss (just like in real life). Instead you will close your trade at the price of the open.

To see what trades you have open, you can look in ```account.openTrades.keys()```

You can plot your equity after running through all your data with matplotlib like this since your equity history is saved per candle you look at:
```
fig, ax = plt.subplots(figsize=(12, 8))

ax.plot(dates, account.equityHist)
ax.set(xlabel = 'Date',ylabel = 'Equity',title = 'Equity vs Time')

fig.autofmt_xdate()
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=16))

plt.show()

print('wins = '+ str(account.winTally))
print('')
print('losses = '+ str(account.lossTally))
print('')
print('percent win = '+str(100*account.winTally/(account.winTally+account.lossTally))+'%')
print('')
print('ROI is '+ str(100*account.equity/50000))
```
![image](https://github.com/xemadhaquex/TradeBackTester.py/assets/38025253/8137f009-5918-456f-9569-dee82ef4818f)

