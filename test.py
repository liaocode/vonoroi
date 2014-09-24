he
import turtle

def drawEdge(edge, myTurtle):
	v1 = edge[0]
	v2 = edge[1]
	myTurtle.up()
	myTurtle.goto(v1[0],v1[1])
	myTurtle.down()
	myTurtle.goto(v2[0],v2[1])

def drawPoint(point, myTurtle):
	myTurtle.up()
	myTurtle.goto(point[0], point[1])
	myTurtle.down()
	myTurtle.dot(5)
		

def drawTriangle(points,myTurtle):
    myTurtle.up()
    myTurtle.goto(points[0][0],points[0][1])
    myTurtle.down()
    #myTurtle.begin_fill()
    myTurtle.goto(points[1][0],points[1][1])
    myTurtle.goto(points[2][0],points[2][1])
    myTurtle.goto(points[0][0],points[0][1])
    #myTurtle.end_fill()


def drawGraph(graph, myTurtle):
	vertexs = graph[0]
	edges = graph[1]
	for v in vertexs:
		drawPoint(v, myTurtle)
	for edge in edges:
		drawEdge(edge, myTurtle)

def getEdgesByTriangle(triangle):
	"""return the triangle's three edges"""
	edges = []
	v1 = triangle[0]
	v2 = triangle[1]
	v3 = triangle[2]
	edges.append([v1,v2])
	edges.append([v1,v3])
	edges.append([v2,v3])
	return edges

def trianglesToGraph(triangles):
	"""make the triangles to a graph"""
	vertexs = []
	edges = []

	for triangle in triangles:
		t_edges = getEdgesByTriangle(triangle)
		for e in t_edges:
			e.sort()
			if e not in edges:
				edges.append(e)
		for vertex in triangle:
			if vertex not in vertexs:
				vertexs.append(vertex)
	return [vertexs, edges]

a = (0,0)
b = (100,0)
c = (0,100)
d = (100,100)
e = (0,200)
f = (200,0)

t1 = [a,b,c]
t2 = [b,c,d]
t3 = [b,d,f]
t4 = [e,c,d]

triangles = [t1,t2,t3,t4]


myTurtle = turtle.Turtle()
myTurtle.speed('slowest')
myWin = turtle.Screen()

for triangle in triangles:
	#drawTriangle(triangle, myTurtle)
	pass

graph = trianglesToGraph(triangles)
drawGraph(graph,myTurtle)

print 'edges are:'
edges = graph[1]
edges.sort()
for e in edges:
	print e

#drawEdge([a,b],myTurtle)

myWin.exitonclick()
