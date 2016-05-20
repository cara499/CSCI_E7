#title           :Currency.py
#description     :Simple currency converter
#author          :Caroline Smith
#date            :05/11/16
#python_version  :3.5.1 
#notes           :converted amount of "money" slightly varies with each query request.
#==============================================================================
import requests 
import re

class Currency(object):
	"""Represent given amount of "money" in a given currency."""
	def __init__(self, amount, typ):
		self.amount = float(amount)
		self.typ = typ
		# Give error if not one of these currencies
		self.currencies = ['USD', 'EUR', 'CAD', 'CNY', 'GBP']
		if self.typ not in self.currencies:
			raise Exception("Invalid currency type.")

	def convert_to(self,Ttyp):
		"""Convert from one currency to another using the current exchange rates via Google API."""
		self.Ttyp = Ttyp
		# Set up API query
		query = {'a': str(self.amount), 'from': self.typ, 'to': self.Ttyp}
		r = requests.get('https://www.google.com/finance/converter', params=query)

		# Search HTML for conversion result
		searchObj = re.search(r'(?:div id=currency_converter_result>\d+\.?\d+ \w+ = <span class=bld>)(\d+\.?\d+)',
								r.text)
		newamt = searchObj.group(1)
	
		return self.__class__(newamt,Ttyp)
	
	def _compare_typs(self,other):
		"""Compare currency types"""
		if isinstance(other, Currency): 
			# if currency types differ, convert to first argument currency type 
			if self.typ != other.typ:
				other_amt = other.convert_to(self.typ).amount
			else:
				other_amt = other.amount

		return other_amt

	def __add__(self, other):
		return self.amount + self._compare_typs(other)

	def __sub__(self, other):
		return self.amount - self._compare_typs(other)
    
	def __lt__(self, other):
		return self.amount < self._compare_typs(other)

	def __gt__(self, other):
		return self.amount > self._compare_typs(other)

	def __str__(self):
		return self.typ + " " + str(self.amount)
