from tkinter import *
from utils import *
from geo import *

master = Tk()

w = Canvas(master, width=600, height=600, bg="#000000")
w.pack()

a1 = Point(100,0)
a2 = Point(0,0)
a3 = Point(50,100)
a4 = Point(50,200)

t1 = Line(a1, a2)
t2 = Line(a3, a4)

arr = Array()

arr.push(a1)
arr.push(a2)
arr.push(a3)
arr.push(a4)

bz = Bezier(arr)


Draw.bezier(bz, "#00ff00", w, 300, 300)


master.mainloop()

