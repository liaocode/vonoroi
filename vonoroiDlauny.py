#! /urs/bin
# Bowyer-Watson algorithm

import turtle
import math
import random

# reference points
o1 = (0, -1000)
o2 = (0, 0.85*1000)
o3 = (1000, 0)
border = [o1,o2,o3]



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

	return (center, radius)

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

def drawPolygon(polygon, myTurtle, color='black'):
	myTurtle.up()
	myTurtle.pencolor(color)
	begin = polygon[0]
	for point in polygon:
		myTurtle.goto(point[0],point[1])
		myTurtle.down()
	myTurtle.goto(begin[0],begin[1])

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

def sortArroundTriangles(point, triangles, myTurtle):
	"""return a sorted polygon"""
	triangle_pairs = findNeighbourTriangles(triangles)
	for triangle_pair in triangle_pairs:
		circle_1 = find_circumcircle(triangle_pair[0])
		cirlce_2 = find_circumcircle(triangle_pair[1])
		vexter_1 = circle_1[0]
		vexter_2 = cirlce_2[0]
		#drawPoint(vexter_1,myTurtle)
		#drawPoint(vexter_2,myTurtle)
		drawEdge([vexter_1, vexter_2], myTurtle)

def main():
	myTurtle = turtle.Turtle()
	myTurtle.speed('slow')
	myWin = turtle.Screen()
	# save the delaunty triangle
	delaunty_triangles = [(o1, o2, o3)]

	# save the triangle's circumcircle center and radius
	# circumcircles = [circle]
	# circle = [center, radius]
	circumcircles = []
	# initialize
	circle = find_circumcircle(delaunty_triangles[0])
	circumcircles.append(circle)

	# the number of the points
	free_points = []
	# 10 points
	#for n in xrange(1,7):
	#	a = random.uniform(250,750)
	#	b = random.uniform(1,500)
	#	p = (a,b)
	#	if p not in free_points:
	#		free_points.append(p)
	# save the free points
	#k0 = (150,150)
	#k1 = (100,200)
	#k2 = (150,100)
	#k3 = (200,200)
	#free_points = [k0, k1, k2]

	# free points
	p1 = (100, 80)
	p2 = (200, 70)
	p3 = (150, 60)
	p4 = (140,50)
	p5 = (130,90)
	p6 = (130,100)
	p7 = (120, 90)
	p8 = (125,99)
	p9 = (30,319)
	p10 = (1,100)
	free_points = [p1,p2,p3,p4,p5,p6,p7,p8]

	# 1.make a super triangle, contain all free points
	#   join in the triangle list

	# 2.insert one free points,
	#   find triangle in the triangle list that its circumcircle
	#   contain the insert one,
	#   and delete the triangles's public edges,
	#   then connect the free point with the triangle's points
	for point in free_points:
		# find the affected triangles
		affected_triangles = []
		####
		print ''
		print 'point'
		print point
		myTurtle.clear()
#		drawPoint(point, myTurtle)
		print 'delaunty_triangles'
		for t in delaunty_triangles:
			print t
#			drawTriangle(t, myTurtle)
		print 'circumcircles'
		for c in circumcircles:
			print c
#			drawCircle(c, myTurtle)

		####
		for circle in circumcircles:
			center = circle[0]
			radius = circle[1]
			if (distanceOfPoints(center, point) < radius):
				# add the triangles from delaunty triangles by circumcircle
				affected_triangles.append(delaunty_triangles[circumcircles.index(circle)])

		print 'affected_triangle number:'
		print len(affected_triangles)
		# at least one affected triangle
		if (len(affected_triangles) == 1):
			# just one affected triangle
			# connet three points
			affected_triangle = affected_triangles[0]

			# del the triangles from triangle list
			delaunty_triangles.remove(affected_triangle)
			circumcircles.remove(find_circumcircle(affected_triangle))
			# add new triangles to the delaunty triangles
			# add circumcircle when add each delaunty triangles
			delaunty_triangles.append([point, affected_triangle[0], affected_triangle[1]])
			circumcircles.append(find_circumcircle([point, affected_triangle[0], affected_triangle[1]]))

			delaunty_triangles.append([point, affected_triangle[0], affected_triangle[2]])
			circumcircles.append(find_circumcircle([point, affected_triangle[0], affected_triangle[2]]))

			delaunty_triangles.append([point, affected_triangle[2], affected_triangle[1]])
			circumcircles.append(find_circumcircle([point, affected_triangle[2], affected_triangle[1]]))

		else:
			# more than one affected
			# find the public edges between the triangles
			triangle_edges = []
			#print 'delaunty_triangles are:'
			#print delaunty_triangles
			#print 'affected_triangles are :'
			#print affected_triangles
			#print 'point is '
			#print point
			for affected_triangle in affected_triangles:
				# delete all affected triangles from delaunty list and the circumcircles
				del circumcircles[delaunty_triangles.index(affected_triangle)]
				delaunty_triangles.remove(affected_triangle)
				# save all the edges
				for edge in pointsToEdges(affected_triangle):
					triangle_edges.append(edge)
			# delete the public edges
			for edge in triangle_edges:
				if triangle_edges.count(edge) > 1:
					triangle_edges.remove(edge)
					triangle_edges.remove(edge)

			# connect the vertexs with the one and make new triangles
			temp_triangles = []
			for edge in triangle_edges:
				temp_triangles.append(toTriangle(point, edge))
			
			#print 'temp_triangles:'
			for triangle in temp_triangles:
			 	#drawTriangle(triangle,myTurtle)
			 	pass

			# 3.Local Optimization Procedure
			#   make sure it is delaunay triangles
			new_triangles = LOP(temp_triangles)
			#new_triangles = temp_triangles
			# flash circumcirlce list by new tirangles
			for new_triangle in new_triangles:
				circumcircles.append(find_circumcircle(new_triangle))
			delaunty_triangles.extend(new_triangles)
			#for triangle in new_triangles:
			#	circle = find_circumcircle(triangle)
			#	circumcircles.append(circle)

			#print 'new_triangles:'
			for triangle in new_triangles:
			 	#drawTriangle(triangle,myTurtle)
			 	pass

			#new_triangles = None
			#if new_triangles = None:
			#	# fix the delaunay list and circumcirlce list
			#	delaunty_triangles.append(new_triangles)
			#	# fix the circumcircle
			#	for triangle in new_triangles:
			#		circle = find_circumcircle(triangle)
			#		position = new_triangles.index(triangle)
			#		circumcircles.insert(position, circle)


	# 4.connect the center of the free point's circumcircle
	#   then product the voronoi graph

	#graph = [vertex, edges]
	#vertex = point
	#edges = [[point1,point2]...]
	myTurtle.clear()
	delaunty_graph = trianglesToGraph(delaunty_triangles)
#	drawGraph(delaunty_graph, myTurtle)
	#delaunty_graph[1].sort()
	#for edge in delaunty_graph[1]:
	#	print edge

	# delete triangle which content two of o1,o2,o3
	print 'before remove delaunty_triangles are'
	for t in delaunty_triangles:
		print t
	print ''
	print 'remove triangles'
	remove_triangles = []
	for t in delaunty_triangles:
		print 'checking'
		print t
		if (o1 in t and o2 in t) or (o1 in t and o3 in t) or (o2 in t and o3 in t):
			remove_triangles.append(t)
	print ''
	#print 'remove_triangles'
	for t in remove_triangles:
		#print t
		delaunty_triangles.remove(t)
	print ''
	print 'after remove delaunty_triangles'
	for triangle in delaunty_triangles:
		print triangle
#		drawTriangle(triangle, myTurtle, "blue")	
	
	for pp in free_points:
		drawPoint(pp, myTurtle)

	# point's arround triangles
	dP=0
	for point in free_points:
		arround_triangles = []
		for triangle in delaunty_triangles:
			if point in triangle:
				arround_triangles.append(triangle)
		# sort by shunshizhen
#		sorted_vertexs = sortArroundTriangles(point, arround_triangles)
		sortArroundTriangles(point, arround_triangles, myTurtle)
		print ''
		print 'point'
		print point
		print 'arround_triangles'
		for t in arround_triangles:
			print t
#		print 'sorted_vertexs '
#		for st in sorted_vertexs:
#			print st
			#drawTriangle(st, myTurtle, "red")
		#sorted_polygon = []
		# find the tirangle's circumcircle
		#for s_triangle in sorted_arround_triangles:
		#	s_circle = find_circumcircle(s_triangle)
		#	sorted_polygon.append(s_circle[0])
		
		if dP < 1:
#			drawPolygon(sorted_vertexs, myTurtle, 'red')
			dP = 3

	#	voronoi_polygons.append(sorted_polygon)

	for pp in free_points:
		#drawPoint(pp, myTurtle)
		#print pp
		pass
	for triangle in delaunty_triangles:
		#drawTriangle(triangle, myTurtle)
		#print triangle
		pass
	for circle in circumcircles:
		#drawCircle(circle, myTurtle)
		pass

	print 'END'
	myTurtle.up()
	myTurtle.home()
	myWin.exitonclick()

main()

