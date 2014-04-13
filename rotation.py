import math 
from Tkinter import *
import cmath

def rotation (rotation_z):
	theta = rotation_z * math.pi/180
	
	x = [50, 50, 250, 250]
	y = [50, 100, 100, 50]
	xc = 150
	yc = 75
	canvas.create_polygon(x[0], y[0], x[1], y[1], x[2], y[2], x[3], y[3])
	X = [0,0,0,0]
	Y = [0,0,0,0]
	for i in xrange(3):
		X[i] = 2 * ((x[i]-xc) * math.cos(theta) - (y[i]-yc) * math.sin(theta)) + xc
		Y[i] = 2 * ((x[i]-xc) * math.sin(theta) + (y[i]-yc) * math.cos(theta)) + yc
	print X, Y
	canvas.create_polygon(X[0], Y[0], X[1], Y[1], X[2], Y[2], X[3], Y[3])


def complexRot(rotation_z):
	xoffset = 150
	yoffset = 75
	newCoordinates = []
	coordinates = [(50,50), (50,100), (250, 100),(250, 50)]
	polygon_item = canvas.create_polygon(coordinates)

	cangle = cmath.exp(rotation_z*1j) # angle in radians
	center = complex(xoffset, yoffset)
	for x, y in coordinates:
	    v = cangle * (complex(x, y) - center) + center
	    newCoordinates.append(v.real)
	    print "real: ", v.real
	    # if v.imag == None: v.imag = 0
	    if len(v == 1): 
	    	newCoordinates.append(0)
	    else: newCoordinates.append(v.imag)
        

    	print newCoordinates
	canvas.coords(polygon_item, *newCoordinates)
	# canvas.create_polygon(X, Y[0], X[1], Y[1], X[2], Y[2], X[3], Y[3])

root = Tk()
canvas = Canvas(root, width = 1000, height = 1000)
canvas.pack()
complexRot(30)
canvas.mainloop()