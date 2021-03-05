#a class to use tables/arrays | une classe pour les array/tableau
from random import *
from math import *
from os import system, name

class Tool:

	def clear(): 
  
	    # for windows 
	    if name == 'nt': 
	        _ = system('cls') 
	  
	    # for mac and linux(here, os.name is 'posix') 
	    else: 
	        _ = system('clear')

	def float(x,n):
		if (n >= 0):
			return round(x*(10**n) )/(10**n)

	def pgcd(a,b):

		r = 1

		if (a < b):
			temp = a
			a = b
			b = temp

		while (r != 0):
			r = a%b
			a = b
			b = r

		return a

	def bezout(a,b):

		if(b == 0):
			return [a,1,0]

		q = a//b
		r = a - q*b

		d,u,v = Tool.bezout(b,r)

		return [d,v,u-q*v]

	def binome(n, k):
		return Tool.factoriel(n) / ( Tool.factoriel(k)*Tool.factoriel(n-k) );

	def factoriel(n):
		r = 1;

		for i in range (1, n+1):
			r = r*i;

		return r;
		
	def bernstein(t, n, i):

		return casteljauPoly(Tool.binome(n,i)*(t**i)*( (1-t)**(n-i) ))

	def casteljau(b, n): #b should be given as a matrice not an array

		if (type(b) == Array):

			m = Matrice.create(1,1)
			m.table.get(0).table = b.table
			return casteljauPoly(Tool.casteljau(m, 0))

		else:

			if (b.table.get(n).length() == 1):
				r = b
				return r

			else:
				b.table.push(Array())
				for i in range (b.table.get(n).length() - 1):
					b.table.get(n+1).push( (b.get(i,n) + b.get(i+1,n) )/2 )

				return casteljauPoly(Tool.casteljau(b, n+1))

	def casteljauPoly(mat):

		d = mat.table.length()
		b0 = Array()
		b1 = Array()

		for i in range (0,d):

			b0.push(mat.get(0,i))
			b1.push(mat.get(i, d - (d-i) ))

		return (b0, b1)




	def dist(a,b):

		if (len(a) == len(b)):

			d = 0

			for i in range (0, len(a)):

				d += (a[i] - b[i])**2

			return sqrt(d)


	def Average(array):

		res = 0

		for i in range (0, len(array)):

			res = res + array[i]

		res = res / len(array)

		return res


	def Quartile(array, n):

		a = Array()
		a.table = array

		res = a.Quartile(n).table

		return res 

				


class Array:

	#constructor
	def __init__( self ):
		self.table = []
		self.startIndex = 0

	#utiliser par un print(type Array)
	def __str__(self):
		text = "["

		for i in range(0,self.length() - 1):
			text += "(" + str(self.startIndex + i) + "): " + str(self.get(i)) + ", "

		text +=  "(" + str(self.startIndex + self.length()-1)  + "): " + str(self.get(self.length()-1)) + "]"

		return text
		del text

	def __eq__(self, other):
		if (self.table == other.table and self.startIndex == other.startIndex):
			return True
		else:
			return False

	def __ne__(self, other):
		if (self == other):
			return False
		else:
			return True

	def __lt__(self, other):
		return False
	def __gt__(self, other):
		return False

	def __le__(self, other):
		if (self == other):
			return True
		else:
			return False

	def __ge__(self, other):
		if (self == other):
			return True
		else:
			return False

	def __add__(self, other):
		ret = Array()
		l = max(self.length(), other.length())

		if (self.length() > other.length()):

			for i in range (other.length() - 1, l-1):
				other.push(0);

		else:

			if (self.length() < other.length()):

				for i in range (self.length() - 1, l-1):
					self.push(0);

		for i in range(0, l):
			ret.push(self.get(i) + other.get(i))

		if (self.length() > other.length()):
			ret.table += self.select(other.length(), self.length()-1).table
		if (self.length() < other.length()):
			ret.table += other.select(self.length(), other.length()-1).table

		return ret
		del ret

	def __sub__(self, other):
		ret = Array()
		l = min(self.length(), other.length() )

		if (self.length() > other.length()):

			for i in range (other.length() - 1, l-1):
				other.push(0);

		else:

			if (self.length() < other.length()):

				for i in range (self.length(), l):
					self.push(0);

		for i in range(0, l):
			ret.push(other.get(i) - self.get(i))

		if (self.length() > other.length()):
			ret += self.select(other.length(), self.length()-1).table
		if (self.length() < other.length()):
			ret += other.select(self.length(), other.length()-1).negative().table

		return ret
		del ret

	def coef(self, k):

		l = self.length()

		for i in range(0, l):
			self.set(i, self.get(i) * k)


	#return length of the array
	def length(self):
		return len(self.table)

	#renvoi la valeur a l'index i
	def get(self, i):
		return self.table[i]

	def set(self, i, v):
		self.table[i] = v

	#add a new value at the end of the array
	def push(self, n):
		temp = [n]
		self.table += temp
		del temp

	#renvoi la liste de valeur comprise entre l'index a et b compris
	def select(self,a,b):

		temp = Array()

		for i in range(a , b+1):
			temp.push(self.get(i))

		return temp

	#return the smallest value of the array
	def min(self):

		mini = self.table[0]

		for i in range(1, self.length()):
			if mini > self.get(i):
				mini = self.get(i)

		return mini
		del mini

	#return the highest value of the array
	def max(self):

		maxi = self.table[0]

		for i in range(1, self.length()):
			if maxi < self.get(i):
				maxi = self.get(i)

		return maxi
		del maxi

	def search(self, n):

		ret = Array()

		for i in range(0, self.length()):
			if (self.get(i) == n):
				ret.push(i)

		return ret
		del ret

	#retire la valeur a l'index i
	def removeAtIndex(self, i):
		del self.table[i]

	#retire une partie de la liste
	def removeSection(self,a,b):
		for i in range(a,b+1):
			del self.table[a]

	#echange les valeurs aux index donné
	def swap(self, i1, i2):

		if(i1 != i2):
			if (i1 > i2):
				temp = i1
				i1 = i2
				i2 = temp
				del temp

			v1 = self.get(i1)
			v2 = self.get(i2)

			self.table = self.select(0,i1-1).table + [v2] + self.select(i1+1,i2-1).table + [v1] + self.select(i2+1 ,self.length()- 1).table

			del v1
			del v2

	#inverse le sens du tableau
	def inverse(self):

		delta = self.length() - 1
		i = 0

		while (delta != 0 and delta != 1):
			self.swap(i,self.length() - 1 - i)
			i += 1
			delta = self.length() - 2*i

		del i
		del delta

	#inverse contained values
	def negative(self):
		ret = Array()

		for i in range(0,self.length()):
			ret.push(-self.get(i))

		return ret
		del ret

	#sort the array from min to max (T(n) = O(n**2))
	def sort(self):

		for a in range(0, self.length()):

			b = 0

			for j in range(0, self.length()):

				if(self.get(a) > self.get(j)):
					b = j
					self.swap(a,b)

		self.inverse()

	#compte le nombre de fois que n apparait dans la table
	def count(self, n):

		ret = 0

		for i in range(0,self.length()):
			if(self.get(i) == n):
				ret += 1

		return ret
		del ret

	#tableau des iterations
	def bucket(self):

		vmin = self.min()
		vmax = self.max()

		ret = Array()

		for i in range(vmin, vmax+1):
			ret.push(self.count(i))

		ret.startIndex = vmin

		return ret

		del ret
		del vmin
		del vmax

	def bucketSort(self):

		bucket = self.bucket()
		tab = []

		for i in range(0, bucket.length()):
			for j in range (0,bucket.get(i)):

				tab += [i + bucket.startIndex]

		self.table = tab

		del tab
		del bucket

	#def fastSort(self):


	#genere un Array randomiser
	def random(l, mini, maxi):

		ret = Array()

		for i in range(0,l):
			r = random() * (maxi - mini) + mini
			ret.push(r)
			del r

		return ret
		del ret

	#renvoi la table des entier
	def integer(self):

		ret = Array()

		for i in range(0,self.length()):
			ret.push(round(self.table[i]))

		return ret
		del ret

	def float(self, n):
		ret = Array()

		for i in range(0,self.length()):
			ret.push(Tool.float(self.get(i), n))

		return ret
		del ret

	def complete(self, n):

		tmp = Array()

		for i in range (0, self.startIndex):
			tmp.push(n)

		self.table = tmp.table + self.table
		self.startIndex = 0;

	def Quartile(self, n):

		if (n >= 2):

			res = Array()

			self.sort()

			for i in range(1, n):

				val = self.get( i*round(self.length()/n) )
				res.push(val) 

			return res


#class Matrice

class Matrice:

	def __init__(self):
		self.table = Array()
		self.cols = 0
		self.lines = 0

	def __str__(self):
		string = ""

		for i in range(0,self.table.length()):
			string += str(self.table.get(i).table) + "\n"

		return string

	def __mul__(self, other):

		if (other.cols == self.lines):
			ret = Matrice.create(other.lines,self.cols)

			for x in range(0, other.lines):
			#on parcours les colones
				for y in range(0, self.cols):
				#on parcours les lignes				
					value = 0
					for n in range(0, other.cols):
						value += other.get(x,n) * self.get(n,y)	
					ret.set(y,x,value)

			return ret

		else:
			if (self.cols == other.lines):
				ret = Matrice.create(self.lines,other.cols)

				for x in range(0, self.lines):
				#on parcours les colones
					for y in range(0, other.cols):
					#on parcours les lignes				
						value = 0
						for n in range(0, self.cols):
							value += self.get(x,n) * other.get(n,y)	
						ret.set(y,x,value)

				return ret

		

		if (self.cols != other.lines):
			return "ERROR"

	def create(c,l):

		tab = Matrice()

		for i in range (0,c):
			row = Array()
			for j in range(0,l):
				row.push(0)
			tab.table.push(row)

		tab.cols = c
		tab.lines = l

		return tab

	def random(c,l):
		tab = Matrice()

		for i in range (0,c):
			row = Array()
			for j in range(0,l):
				row.push(round(random()*100))
			tab.table.push(row)

		tab.cols = c
		tab.lines = l

		return tab


	def get(self, x, y):
		return self.table.get(y).get(x)

	def set(self, x, y, v):
		self.table.get(y).set(x,v)



#class des vecteurs

class Vector(Array):

	def __init__(self):
		Array.__init__(self)

	def size(self):
		ret = 0

		for i in range(0, self.length()):
			ret += self.table[i]**2

		return ret**(1/2)

	def rotate2D(self, deg):

		if (self.length() == 2):
			v = Vector()

			i =	self.get(0)
			j = self.get(1)
			o = ((deg%360)/360)*2*pi

			x =	Tool.float(i*cos(o) - j*sin(o), 2)
			y = Tool.float(j*cos(o) + i*sin(o), 2)

			v.push(x)
			v.push(y)

			return v
		else:
			return Vector()

	def rotate3D(self, degH, degV):

		if (self.length() == 3):
			v = Vector()

			i =	self.get(0)
			j = self.get(1)
			k = self.get(2)

			angH = ((degH%360)/360)*2*pi
			angV = ((degV%360)/360)*2*pi
			
			#rotation autour de l'axe Y
			z = -i*sin(angH) + k*cos(angH)
			x = i*cos(angH) + k*sin(angH)

			#rotation autour de l'axe Z
			y = i*sin(angV) + j*cos(angV)
			

			v.push(x)
			v.push(y)
			v.push(z)

			v.normalize()

			return v

		else:
			return Vector()

	def normalize(self):

		s = self.size()
		self.coef(1/s)

	def scalar(u, v):

		if (u.length() == v.length()):

			l = u.length()
			r = 0;

			for i in range (0,l):

				r += u.get(i) * v.get(i)

			return r

	def fromTo3D(o, e):

		r = Vector()
		r.table = [e[0]-o[0], e[1]-o[1], e[2]-o[2]]
		return r

class Polynome(Array):

	def __init__(self):
		Array.__init__(self)

	def __mul__(self, other):

		d1 = self.length() - 1
		d2 = other.length() - 1

		s = Array()
		o = Array()

		s.table = self.table[:] #[:] sert a eviter d'utiliser la meme addresse mémoire (copie superficielle)
		o.table = other.table[:]

		sm = Matrice.create(s.length(),1)
		om = Matrice.create(1,o.length())

		om.table.set(0, o)

		for i in range(0, s.length()):
			sm.set(0, i, s.get(i))
		
		if(o > s):
			m = om*sm
		else:
			m = sm*om

		r = Polynome()
		for i in range (0, m.cols):
			temp = m.table.get(i)
			temp.startIndex = i
			temp.complete(0)
			r = r + temp

		return r

	def eval(self, t):

		r = 0

		for i in range (0, self.length()):

			r += self.get(i) * t**i

		return r

	def derive(self):

		deg = self.length() - 1
		r = Polynome()

		for i in range(0, deg):
			
			r.push(self.get(deg-i)*i)

		return r


	def cano2bernst(p):

		b = Array()
		n = p.length()

		for i in range(1,n+1):
			bi = 0
			for k in range(0, min(i,n)):

				bi += ( p.get(k) * Tool.binome(i,k) ) / Tool.binome(n,k)

			b.push(bi)
		

		return b