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
