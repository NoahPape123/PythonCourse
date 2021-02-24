from random import uniform

class Universe():
	def __init__(self):
		self.prices = {}
		self.types = {}

	def prices(self):
		return self.prices

	def updateAsset(self, symbol, price, type):
		self.prices[symbol] = price
		self.types[symbol] = type

	def getPrice(self, symbol, type):
		currentPrice = self.prices[symbol]
		if type == 'stock':
			newPrice = currentPrice*uniform(0.5, 1.5)
		elif type == 'mutual fund':
			newPrice = currentPrice * uniform(0.9, 1.2)
		elif type == 'bond':
			newPrice = currentPrice * uniform(0.98, 1.04)
		self.updateAsset(symbol, newPrice, type)
		return newPrice


class Asset():
	def __init__(self, price, symbol):
		self.price = price
		self.symbol = symbol

	def price(self):
		return self.price

	def symbol(self):
		return self.symbol()

class Stock(Asset):
	def __init__(self, price, symbol):
		super().__init__(price, symbol)

class MutualFund(Asset):
	def __init__(self, symbol):
		super().__init__(1, symbol)

class Bond(Asset):
	def __init__(self, price, symbol):
		super().__init__(price, symbol)

class Portfolio():
	def __init__(self):
		self.cash = 0
		self.portfolio = {'stock':{}, 'mutual fund':{}, 'bond':{}}
		self.txs = []
		self.universe = Universe()

	def __str__(self):
		portfolio = "cash: " + "${:,.2f}".format(self.cash) + "\n"
		for type in self.portfolio:
			if len(self.portfolio[type].keys())>0:
				type_holdings = type + ": "
				for asset in self.portfolio[type].keys():
					type_holdings += asset + "    " + str(self.portfolio[type][asset]) + "\n"
				portfolio += type_holdings
		return portfolio

	def history(self):
		for tx in self.txs:
			print(tx)

	def addCash(self, amount):
		if amount < 0:
			print("Can't add negative amount of cash; please use withdrawCash instead")
		else:
			self.cash += amount
			tx = "Deposited " + "${:,.2f}".format(amount)
			self.txs.append(tx)
			print(tx)

	def withdrawCash(self, amount):
		if amount < 0:
			print("Can't withdraw negative amount of cash; please use addCash instead")
		elif amount > self.cash:
			print("Insufficient cash balance to complete withdraw.")
		else:
			self.cash -= amount
			tx = "Withdrew " + "${:,.2f}".format(amount)
			self.txs.append(tx)
			print(tx)

	def buy(self, shares, asset, type):
		self.universe.updateAsset(asset.symbol, asset.price, type)
		if shares * asset.price > self.cash:
			print("Transaction not completed. Insufficient Cash Balance.")
		else:
			if asset.symbol not in self.portfolio[type].keys():
				self.portfolio[type][asset.symbol] = 0
			self.portfolio[type][asset.symbol] += shares
			self.cash -= shares*asset.price
			tx = "Purchased " + str(shares) + " shares of " + asset.symbol + " at " + "${:,.2f}".format(asset.price) + "."
			self.txs.append(tx)
			print(tx)

	def sell(self, symbol, shares, type):
		if symbol not in self.portfolio[type].keys() or shares > self.portfolio[type][symbol]:
			print("Transaction not completed. Short Selling not enabled.")
		else:
			self.portfolio[type][symbol] -= shares
			if self.portfolio[type][symbol] == 0:
				del self.portfolio[type][symbol]
			price = self.universe.getPrice(symbol, type)
			self.cash += shares*price
			tx = "Sold " + str(shares) + " shares of " + symbol + " at " + "${:,.2f}".format(price) + "."
			self.txs.append(tx)
			print(tx)


	def buyStock(self, shares, stock):
		if isinstance(shares, int) or shares.is_integer() == True:
			self.buy(shares, stock, 'stock')
		else:
			print("Cannot buy fractional stock shares.")

	def sellStock(self, symbol, shares):
		if isinstance(shares, int) or shares.is_integer() == True:
			self.sell(symbol, shares, 'stock')
		else:
			print("Cannot sell fractional stock shares.")

	def buyMutualFund(self, shares, mf):
		self.buy(shares, mf, 'mutual fund')

	def sellMutualFund(self, symbol, shares):
		self.sell(symbol, shares, 'mutual fund')

	def buyBond(self, shares, bond):
		self.buy(shares, bond, 'bond')

	def sellBond(self, symbol, shares):
		self.sell(symbol, shares, 'bond')

if __name__ == '__main__':
	portfolio = Portfolio()
	portfolio.addCash(300.50)
	s = Stock(20, "HFH")
	portfolio.buyStock(5, s)
	mf1 = MutualFund("BRT")
	mf2 = MutualFund("GHT")
	portfolio.buyMutualFund(10.3, mf1)
	portfolio.buyMutualFund(2, mf2)
	print(portfolio)
	portfolio.sellMutualFund("BRT", 3)
	portfolio.sellStock("HFH", 1)
	portfolio.withdrawCash(50)
	portfolio.history()