import turtle
import random
import math

def drawPoint(point, myTurtle):
	myTurtle.up()
	myTurtle.goto(point[0], point[1])
	myTurtle.down()
	myTurtle.dot(5)

def drawCircle(circle,myTurtle):
	center = circle[0]
	radius = circle[1]

	myTurtle.up()
	myTurtle.goto(center[0], center[1]-radius)
	myTurtle.down()
	myTurtle.circle(radius)

def find_circumcircle(triangle):
	"""Find a triangle's circumcircle"""
	A = triangle[0]
	B = triangle[1]
	C = triangle[2]

	x1 = float(A[0])
	x2 = float(B[0])
	x3 = float(C[0])
	y1 = float(A[1])
	y2 = float(B[1])
	y3 = float(C[1])
	x=((y2-y1)*(y3*y3-y1*y1+x3*x3-x1*x1)-(y3-y1)*(y2*y2-y1*y1+x2*x2-x1*x1))/(2*(x3-x1)*(y2-y1)-2*((x2-x1)*(y3-y1)))
	y=((x2-x1)*(x3*x3-x1*x1+y3*y3-y1*y1)-(x3-x1)*(x2*x2-x1*x1+y2*y2-y1*y1))/(2*(y3-y1)*(x2-x1)-2*((y2-y1)*(x3-x1)))

	center = (x, y)
	radius = math.sqrt((x1-x)**2 + (y1-y)**2)

	return (center, radius)
	
def drawPolygon(polygon, myTurtle):
	myTurtle.up()
	for point in polygon:
		myTurtle.goto(point[0],point[1])
		myTurtle.down()

def drawTriangle(points,myTurtle):
    myTurtle.up()
    myTurtle.goto(points[0][0],points[0][1])
    myTurtle.down()
    #myTurtle.begin_fill()
    myTurtle.goto(points[1][0],points[1][1])
    myTurtle.goto(points[2][0],points[2][1])
    myTurtle.goto(points[0][0],points[0][1])
    #myTurtle.end_fill()

def sortArroundTriangles(point, triangles):
	total = len(triangles)
	sorted_triangles = []
	triangle = triangles.pop()
	sorted_triangles.append(triangle)
	for next_point in triangle:
		if next_point != point:
			break
	for end_point in triangle:
		if end_point != point and end_point != next_point:
			break
	while len(sorted_triangles) != total:
		for triangle in triangles:
			if next_point in triangle:
				sorted_triangles.append(triangle)
				for p in triangle:
					if p != point and p != next_point:
						next_point = p
						break
				triangles.remove(triangle)
	return sorted_triangles

myTurtle = turtle.Turtle()
myTurtle.speed('slowest')
myWin = turtle.Screen()

a = (100,0)
b = (0,100)
c = (-100, 0)
d = (0, -100)
o = (0,0)

t1 = [o,a,b]
t2 = [o,c,b]
t3 = [o,c,d]
t4 = [o,d,a]

t = [t1,t2,t3,t4]

new_t = sortArroundTriangles(o, t)
print 'new t is :'
for nt in new_t:
	print nt

# the number of the points
free_points = []
# 10 points
for n in xrange(1,100):
	#a1 = random.uniform(1,300)
	#b1 = random.uniform(1,300)
	#a2 = random.uniform(1,300)
	#b2 = random.uniform(1,300)
	#a3 = random.uniform(1,300)
	#b3 = random.uniform(1,300)
	#p1 = (a1,b1)
	#p2 = (a2,b2)
	#p3 = (a3,b3)
	#t = [p1, p2, p3]
	#circle = find_circumcircle(t)
	#myTurtle.clear()
	#drawTriangle(t, myTurtle)
	#drawCircle(circle, myTurtle)
	pass

for pp in free_points:
	#drawPoint(pp, myTurtle)
	pass
myWin.exitonclick()