#! /urs/bin
# Bowyer-Watson algorithm

import turtle
import math
import random

# reference points
o1 = (0, 0)
o2 = (500, 0)
o3 = (250, 500)
border = [o1,o2,o3]

# free points
p1 = (10, 10)
p2 = (150, 80)
p3 = (120, 20)
p4 = (50, 50)
p5 = (60,20)
p6 = (69,82)

# save the voronoi graph
#graph = [vertex, edges]
#vertex = point
#edges = [[point1,point2]...]
voronoi_graph = []
# polygon = [point...]
# voronoi_polygons = [polygon]
voronoi_polygons = []

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

	return [center, radius]

def distanceOfPoints(p1,p2):
	x1 = float(p1[0])
	y1 = float(p1[1])
	x2 = float(p2[0])
	y2 = float(p2[1])

	return math.sqrt((x1-x2)**2+(y1-y2)**2)

def drawTriangle(points,myTurtle,color="black"):
    myTurtle.up()
    myTurtle.pencolor(color)
    myTurtle.goto(points[0][0],points[0][1])
    myTurtle.down()
    #myTurtle.begin_fill()
    myTurtle.goto(points[1][0],points[1][1])
    myTurtle.goto(points[2][0],points[2][1])
    myTurtle.goto(points[0][0],points[0][1])
    #myTurtle.end_fill()

def drawCircle(circle,myTurtle):
	center = circle[0]
	radius = circle[1]

	myTurtle.up()
	myTurtle.goto(center[0], center[1]-radius)
	myTurtle.down()
	myTurtle.circle(radius)

def drawPolygon(polygon, myTurtle):
	myTurtle.up()
	for point in polygon:
		myTurtle.goto(point[0],point[1])
		myTurtle.down()

def drawEdge(edge, myTurtle):
	v1 = edge[0]
	v2 = edge[1]
	myTurtle.up()
	myTurtle.goto(v1[0],v1[1])
	myTurtle.down()
	myTurtle.goto(v2[0],v2[1])

def pointsToEdges(points):
	"""make triangle's edges from triangle's three points"""
	edge1 = (points[0], points[1])
	edge2 = (points[0], points[2])
	edge3 = (points[1], points[2])
	return [edge1, edge2, edge3]

def toTriangle(point, edge):
	"""product a new triangle by the given point and edge"""
	return [point, edge[0], edge[1]]

def find_other_points(triangle, triangles):
	"""find the other points except the triangle's point in triangles"""
	triangles.remove(triangle)
	points =[]
	for tri in triangles:
		for point in tri:
			if point not in points:
				points.append(point)
	return points

def isNeighbourTriangles(triangle_1, triangle_2):
	"""if the two triangles are neightbour, reutrn True"""
	num = 0
	for p1 in triangle_1:
		for p2 in triangle_2:
			if p1 == p2:
				num = num + 1
				continue;
	if num == 2:
		#print 'isNeighbourTriangles return True'
		return True
	else:
		#print 'isNeighbourTriangles return False'
		return False

def getFourPoint(triangle_1, triangle_2):
	"""return the point that is not in triangle_2"""
	for point in triangle_1:
		if (point != triangle_2[0]) and (point != triangle_2[1]) and (point != triangle_2[2]):
			return point
	return None

def findNeighbourTriangles(triangles):
	""" find the neightbour triangles pairs from triangles"""
	neighbour_triangles = []
	other_triangles = []
	for triangle in triangles:
		other_triangles = triangles[:]
		other_triangles.remove(triangle)
		for sec_triangle in other_triangles:
			if isNeighbourTriangles(triangle, sec_triangle):
				neighbour_triangle = [triangle, sec_triangle]
				neighbour_triangle.sort()
				if neighbour_triangle not in neighbour_triangles:
					neighbour_triangles.append(neighbour_triangle)
					neighbour_triangles.sort()
	return neighbour_triangles

def getTriangleByPair(triangle_pairs):
	"""get the single triangle from the trinagles pairs"""
	triangles = []
	for triangle_pair in triangle_pairs:
		for t in triangle_pair:
			if t not in triangles:
				triangles.append(t)
	return triangles

def LOP(triangles):
	"""Local Optimization Procedure"""
	# find the neightbour triangles pair
	total = 0
	neighbour_triangles = []
	# then, deal triangle pair one by one
	

	neighbour_triangles = findNeighbourTriangles(triangles)
	while total!=len(neighbour_triangles):
		points = []
		for neightbour_pair in neighbour_triangles:
			pair_1 = neightbour_pair[0]
			pair_2 = neightbour_pair[1]
			# get the point in pair1 and pair2
			for p in pair_1:
				points.append(p)
			for p in pair_2:
				points.append(p)
			# get one triangle's circumcircle
			circle_1 = find_circumcircle(pair_1)
			center_1 = circle_1[0]
			radius_1 = circle_1[1]
			# get the fourth point in neightbour pair
			fourth_point = getFourPoint(pair_2, pair_1)
			fourth_to_center1 = distanceOfPoints(fourth_point, center_1)
			if fourth_to_center1 < radius_1:
				# the point inside of the circle
				# remake the triangles
				# total four points in points, and just need to remove one time
				points.sort()

				print 'before remeve, points are:'
				print points

				points.remove(fourth_point)

				print 'after remove, points are:'
				print points
				print 'pair_1 are'
				print pair_1
				print 'pair_2 are'
				print pair_2

				for p in points:
					if p not in pair_1 or p not in pair_2 :
						first_point = p
						points.remove(p)
						break
				# the 'points' remain the common points that each count is 2
				points.sort()
				# get the common point
				common_point_1 = points.pop(0)
				common_point_2 = points.pop(1)
				# remove the neightbour_pair from neighbour_triangles
				neighbour_triangles.remove(neightbour_pair)
				new_tri_1 = [first_point, fourth_point, common_point_1]
				new_tri_2 = [first_point, fourth_point, common_point_2]
				new_neightbour_pair = [new_tri_1, new_tri_2]
				# add to the neightbour triangles
				neighbour_triangles.append(new_neightbour_pair)
				# go to find the neightbour
				total = 0
				# update the triangles
				triangles = getTriangleByPair(neighbour_triangles)
				break
			else:
				total = total + 1
		neighbour_triangles = findNeighbourTriangles(triangles)

	# get the triangles from the neighbour_triangles
	new_triangles = getTriangleByPair(neighbour_triangles)
	return new_triangles

def drawPoint(point, myTurtle):
	myTurtle.up()
	myTurtle.goto(point[0], point[1])
	myTurtle.down()
	myTurtle.dot(5)

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
		for triangle_1 in triangles:
			if next_point in triangle_1 and triangle_1 not in sorted_triangles:
				sorted_triangles.append(triangle_1)
				for p in triangle_1:
					if p != point and p != next_point:
						next_point = p
						if p == end_point:
							return sorted_triangles
						break
	return sorted_triangles

def main():
	myTurtle = turtle.Turtle()
	myTurtle.speed('slow')
	myWin = turtle.Screen()

	# define the free points
	k0 = (150,150)
	k1 = (100,200)
	k2 = (150,100)
	k3 = (200,200)
	free_points = [k0, k1, k2]

	# define all triangles and their circumcircles
	# triangle = [(a1,a2)...]
	# trinagles = [triangle...]
	all_triangles = [border]
	# center = [(a1, a2),(a3,a4)]
	# radius = a1
	# circumcircle = [center, radius]
	all_circumcircles = []

	"""	1.make a super triangle, contain all free points
	  		join in the triangle list"""

	"""	2. when more than three points, insert one free points,
			find triangle in the triangle list that its circumcircle
			contain the insert one,
			and delete the triangles's public edges,
			then connect the free point with the triangle's points"""
	if len(free_points) < 3:
		return

	print 'length of free_points'
	print len(free_points)

	# if some points on a line, just do nothing

	for free_point in free_points:
		# find the affected triangles
		affected_triangles = []
		for circle in circumcircles:
			center = circle[0]
			radius = circle[1]
			if (distanceOfPoints(center, point) < radius):
				# add the triangles from delaunty triangles by circumcircle
				affected_triangles.append(delaunay_triangles[circumcircles.index(circle)])

	"""	4.connect the center of the free point's circumcircle
			then product the voronoi graph"""


	myWin.exitonclick()

main()