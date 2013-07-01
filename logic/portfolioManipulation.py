from gamemodels.models       import *
from django.db.models        import Max

# Logics for byuing a stock
def buyStock(investor,company,amount):

   # find the last time that was entered
   lastTime = company.priceHistory.all().aggregate(Max('time'))
   
   # find a reference to that stock entry
   stockHandle = company.priceHistory.get(time=lastTime['time__max'])

   if investor.cash < stockHandle.price * amount:
      return 'transaction failed'
   else:
      # Create a new TradingRegister entry, of buy type
      entry = TradingRegister()
      entry.investor = investor
      entry.action   = 'buy'
      entry.company  = company
      entry.stock    = stockHandle
      entry.amount   = amount
      entry.save()
   
      # this investor's cash is used to pay the transaction
      investor.cash -= stockHandle.price * amount
      investor.save()
      return 'transaction complete'

def sellStock(investor,company,amount):
   
   # find the last time that was entered
   lastTime = company.priceHistory.all().aggregate(Max('time'))
   
   # find a reference to that stock entry
   stockHandle = company.priceHistory.get(time=lastTime['time__max'])
   
   entry = TradingRegister()
   entry.investor = investor
   entry.action   = 'sell'
   entry.company  = company
   entry.stock    = stockHandle
   entry.amount   = amount
   entry.save()
   
   investor.cash += stockHandle.price * amount
   investor.save()
   
def getCurrentPortfolio(investor):
   
   # Get all transactions this player has created
   allTransactions = TradingRegister.objects.filter(investor=investor)
   
   companiesOwned = {}
   
   # loop through to find what companies are owned
   for transaction in allTransactions:
      
      # if the dict key isn't set yet, set it to 0
      companiesOwned.setdefault(transaction.company.name,0)
      
      # otherwise increase or decrease
      if transaction.action == 'buy':
         companiesOwned[transaction.company.name] += transaction.amount
      elif transaction.action == 'sell':
         companiesOwned[transaction.company.name] -= transaction.amount
      else:
         print 'ERROR: PORTFOLIOMANIPULATION.PY: GET CURRENT PORTFOLIO: WRONG TYPE'
   
   return companiesOwned