import datetime
from datetime import date

#create class for account and functions to buy and sell
class Account:
    def __init__(self, equity):
        self.equity = equity
        self.equityHist = [] #[equity]
        self.liquidEquity = equity
        self.openTrades = {}  # ticker = [position, entryPrice, self.equity*self.tradeSize]
        self.closedTrades = {}
        #self.tp = 1+tp
        #self.sl = -self.equity*sl#-self.equity*.01
        #self.tradeSize = tradeSizeofAccount
        self.winTally = 0
        self.lossTally = 0

    def openTrade(self,position,ticker, entryPrice, day, percentofAccountToTrade,target,stopLimit): #('long' or 'short', AAPL, entry price, date, price target to tp, price target to sl)
        
        #check if youre already in a trade on this ticker
        if ticker in self.openTrades.keys():
            print('already in a trade on '+ticker)
            return
        
        #if you have enough liquidity then open trade, else print the message
        toTrade = self.equity*percentofAccountToTrade
        numShares = toTrade//entryPrice
        if self.liquidEquity >= numShares*entryPrice:
            self.openTrades[ticker] = [position, entryPrice, numShares, day,target,stopLimit]
            self.liquidEquity -= numShares*entryPrice
            print(position + ' ' + str(numShares*entryPrice) + ' on '+ticker)
        else:
            print('not enough liquid equity to make trade on '+ticker+', liquid is '+ str(self.liquidEquity) + ' and needed is ' + str(self.equity*numShares))

        return

    def closeTrade(self,ticker,currPrice,olhc): #AAPL, current price, 'open' or 'low' or 'high' or 'close'
        
        #first get the entry information from the trade to determine the different aspects of the position
        position,entryPrice,numShares,openDay,target,stopLimit = self.openTrades[ticker][0], self.openTrades[ticker][1], self.openTrades[ticker][2], self.openTrades[ticker][3], self.openTrades[ticker][4],self.openTrades[ticker][5]    
        
        dollarChange = currPrice-entryPrice #dollar change like 5.66
        perChange = currPrice/entryPrice #percent change ex: 1.2 or 0.8
        
        if position == 'short':
            dollarChange*= -1
            
            
            if perChange == 1:
                perChange = 1
            elif perChange < 1:         #if positive on a short
                perChange = 1 + 1-perChange
            else:                    #if negative on a short
                perChange = 1+(1-perChange)
            
        tradeChange = dollarChange*numShares

        if position == 'long' and currPrice <=stopLimit and olhc == 'open':
            self.equity += tradeChange
            self.liquidEquity += numShares*currPrice
            self.openTrades.pop(ticker) #remove ticker from openTrades
        
        elif position == 'long' and currPrice <= stopLimit:
            tradeChange = -(entryPrice - stopLimit)*numShares        #(stopLimit-entryPrice)*numShares
            self.equity += tradeChange
            self.liquidEquity += (numShares*stopLimit)
            self.openTrades.pop(ticker) #remove ticker from openTrades
            
        elif position == 'short' and currPrice >= stopLimit and olhc == 'open':
            self.equity += tradeChange
            self.liquidEquity += numShares*currPrice
            self.openTrades.pop(ticker) #remove ticker from openTrades
        
        elif position == 'short' and currPrice >= stopLimit:
            tradeChange = (entryPrice - stopLimit)*numShares     #-1*(stopLimit-entryPrice)*numShares
            self.equity += tradeChange
            self.liquidEquity += (numShares*stopLimit)
            self.openTrades.pop(ticker) #remove ticker from openTrades
        
        #now for taking profit
        elif position == 'short' and currPrice <= target:
            self.equity += tradeChange
            self.liquidEquity += numShares*target
            self.openTrades.pop(ticker) #remove ticker from openTrades
        
        elif position == 'long' and currPrice >= target:
            self.equity += tradeChange
            self.liquidEquity += numShares*target
            self.openTrades.pop(ticker) #remove ticker from openTrades
            
        
        '''
        if tradeChange < 0 and olhc == 'Open': #if catching negative at open
            self.equity += tradeChange
            self.liquidEquity += numShares*currPrice
            self.openTrades.pop(ticker) #remove ticker from openTrades
        
        elif tradeChange < 0: #if catching negative, just remove SL
            self.equity += self.sl
            self.liquidEquity += numShares*currPrice
            self.openTrades.pop(ticker) #remove ticker from openTrades
        
        else:
            self.equity += tradeChange
            self.liquidEquity += numShares*currPrice
            self.openTrades.pop(ticker) #remove ticker from openTrades
            
        '''
        #add the trade to your closed trades log
        if ticker not in self.closedTrades.keys():
            self.closedTrades[ticker] = [(perChange,tradeChange)]
        else:
            self.closedTrades[ticker].append((perChange,tradeChange))

        #self.equityHist.append(self.equity)
        
        print('equity is now = ' + str(self.equity))
        print(' ')

        return

    def determineIfShouldClose(self,ticker,currPrice,day,olhc): #AAPL, current price, date in datetime timestamp, 'open' or 'low' or 'high' or 'close'
        if ticker not in self.openTrades.keys():
            print('dont have a position in '+ ticker)
            return
        
        #get postion info
        position,entryPrice,numShares,openDay,target,stopLimit = self.openTrades[ticker][0], self.openTrades[ticker][1], self.openTrades[ticker][2], self.openTrades[ticker][3], self.openTrades[ticker][4],self.openTrades[ticker][5]   
        
        dollarChange = currPrice-entryPrice #dollar change like 5.66
        perChange = currPrice/entryPrice #percent change ex: 1.2 or 0.8
        
        if position == 'short':
            dollarChange*= -1
            
            
            if perChange == 1:
                perChange = 1
            elif perChange < 1:         #if positive on a short
                perChange = 1 + 1-perChange
            else:                    #if negative on a short
                perChange = 1+(1-perChange)
            
        
        
        tradeChange = dollarChange*numShares
        

        
        #determine if above tp, below sl, or negative on friday
        
        #first for determining if we hit SL, we have to think about whether its open or not
        if position == 'long' and currPrice <=stopLimit and olhc == 'open':
            print(str(day) + ' taking loss at ' + olhc+ ' on '+ticker)
            print('pos = ' + position +' entry = ' + str(entryPrice) + ' curr = ' +str(currPrice) + ' and change = ' +str(tradeChange))
            self.lossTally +=1
            return True
        
        elif position == 'long' and currPrice <= stopLimit:
            tradeChange = (stopLimit-entryPrice)*numShares
            print(str(day) + ' taking loss at ' + olhc+ ' on '+ticker)
            print('pos = ' + position +' entry = ' + str(entryPrice) + ' curr = ' +str(currPrice) + ' and change = ' +str(tradeChange))
            self.lossTally +=1
            return True
        
        elif position == 'short' and currPrice >= stopLimit and olhc == 'open':
            print(str(day) + ' taking loss at ' + olhc+ ' on '+ticker)
            print('pos = ' + position +' entry = ' + str(entryPrice) + ' curr = ' +str(currPrice) + ' and change = ' +str(tradeChange))
            self.lossTally +=1
            return True
        
        elif position == 'short' and currPrice >= stopLimit:
            tradeChange = -1*(stopLimit-entryPrice)*numShares
            print(str(day) + ' taking loss at ' + olhc+ ' on '+ticker)
            print('pos = ' + position +' entry = ' + str(entryPrice) + ' curr = ' +str(currPrice) + ' and change = ' +str(tradeChange))
            self.lossTally +=1
            return True
        
        #now for taking profit
        elif position == 'short' and currPrice <= target:
            print(str(day) + ' taking profit at' + olhc+ ' on '+ticker)
            print('pos = ' + position +' entry = ' + str(entryPrice) + ' curr = ' +str(currPrice) + ' and change = ' +str(tradeChange))
            self.winTally +=1
            return True
        
        elif position == 'long' and currPrice >= target:
            print(str(day) + ' taking profit at' + olhc+ ' on '+ticker)
            print('pos = ' + position +' entry = ' + str(entryPrice) + ' curr = ' +str(currPrice) + ' and change = ' +str(tradeChange))
            self.winTally +=1
            return True
        
        
        else:
            return False
