from Forex.Currency import Currency

usd = Currency('USD')
pairs = usd.getPairsList()
print(pairs)