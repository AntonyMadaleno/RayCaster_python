#Bidemensional matrices

from random import *
from Array import *

class Matrice:


	def __init__(self):
		self.table = Array()

	def __str__(self):

		string = ""

		for i in range(0,self.table.length()):
			string += str(self.table.get(i).table) + "\n"

		return string

	def getLine(self, y):
		return self.table.get(y)

	def getColumn(self, x):
		ret = Array()

		for i in range(0, self.table.length()):
			ret.push(self.table.get(x))

		return ret
		del ret

	def get(self, x, y):
		return self.table.get(y).get(x)

	#cree une matrice NxN
	def matrice(n):

		m = Matrice()
		for i in range(0,n):
			temp = Array()
			for j in range(0,n):
				temp.push(0)

			m.table.push(temp)
			del temp

		return m






