import turtle
import random

def drawPoint(point, myTurtle):
	myTurtle.up()
	myTurtle.goto(point[0], point[1])
	myTurtle.down()
	myTurtle.dot(5)

# the number of the points
free_points = []
# 10 points
for n in xrange(1,100):
	a = random.uniform(1,300)
	b = random.uniform(1,300)
	p = (a,b)
	if p not in free_points:
		free_points.append(p)


myTurtle = turtle.Turtle()
myTurtle.speed('slowest')
myWin = turtle.Screen()

for pp in free_points:
	drawPoint(pp, myTurtle)
	#pass
myWin.exitonclick()