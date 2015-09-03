#! /usr/bin/python
# -*- coding:utf-8 -*-

import parser
import node
from math import sqrt

class Algo:
	""" Main class implemented the A* algorithm """

	def __init__(self, field, start, end):
		init_tree = None
		self.node_created = {}
		self.field = field
		# Creation of the start and end node
		self.start_node = node.Node(start[0], start[1])
		self.end_node = node.Node(end[0], end[1])
		# Value of f computed for the start node
		self.start_node.f = self.cartesian_distance(self.start_node, self.end_node)
		self.start_node.g = 0

	def generate_sucessors(self, node):
		""" Generate the next possible position from (node.x, node.y) """
		x = node.position_x
		y = node.position_y
		succ = [
			self.connect_node_to_node(node, x-1, y-1),
			self.connect_node_to_node(node, x-1, y),
			self.connect_node_to_node(node, x-1, y+1),
			self.connect_node_to_node(node, x+1, y-1),
			self.connect_node_to_node(node, x+1, y),
			self.connect_node_to_node(node, x+1, y+1),
			self.connect_node_to_node(node, x, y-1),
			self.connect_node_to_node(node, x, y+1)
		]
		# Delete the None occurence frome the list
		succ = filter(None, succ)
		return succ

	def connect_node_to_node(self, father_node, child_node_x, child_node_y):
		"""
		If the father_node located at (father_node.x, father_node.y)
		can reach (child_node_x, child_node_y) (If this is not an obstacle),
		the child node is created an returned. if not, none is returned
		"""
		if child_node_x < 0 or child_node_y < 0 or child_node_x >= self.field.shape[0] or child_node_y >= self.field.shape[1]:
			return None
		elif self.field[child_node_x][child_node_y] != parser.Parser.OBSTACLE:
			return node.Node(child_node_x, child_node_y)


	def compare_f(self, node1, node2):
		""" Used to compare the f value of two nodes """
		if node1.f > node2.f :
			return -1
		elif node1.f < node2.f :
			return 1
		else:
			return 0

	def cartesian_distance(self, node1, node2):
		""" Cartesian distance between two points.
		Used as the heuristic """
		distance = sqrt((node1.position_y-node2.position_y)**2+(node1.position_x-node2.position_x)**2)
		return distance

	def best_first_list_management(self, open_list, item):
		open_list.insert(0, item)
		open_list.sort(cmp=self.compare_f)

	def breadth_first_list_management(self, open_list, item):
		open_list.insert(0, item)

	def depth_first_list_management(self, open_list, item):
		open_list.insert(len(open_list), item)

	def solve(self, list_management_function, display_function):
		"""
		This function implement the Astar algorithm.
		The list management function the way the OPEN list will be managed.
		It allow to use the same structure to implement best-first, depth-first ...
		The display function if the function used to display the current solution
		"""
		closed_list = []
		open_list = []
		initial_node = self.start_node
		open_list.append(initial_node)
		while True:
			# If the open list is empty
			if not open_list:
				print "No Solution"
				return 
			current = open_list.pop()
			display_function(self.get_path(current))
			closed_list.append(current)
			if current == self.end_node:
				print "Solution Found"
				return (self.get_path(current), len(open_list)+len(closed_list))
			succ_list = self.generate_sucessors(current)
			for succ_node in succ_list:
				fetched_from = None
				child_node = succ_node
				if succ_node in open_list:
					fetched_from = open_list
				elif succ_node in closed_list:
					fetched_from = closed_list
				if fetched_from:
					index = fetched_from.index(succ_node)
					child_node = fetched_from[index]
				current.add_child(child_node)
				if fetched_from == None:
					self.attach_and_eval(current, child_node)
					list_management_function(open_list, child_node)
				elif current.g + self.cartesian_distance(current, child_node) < child_node.g:
					self.attach_and_eval(current, child_node)
					if child_node in closed_list:
						self.propagate_path_improvements(child_node)

	def get_path(self, node):
		""" Create the best path to the position (node.x, node.y) """
		return_list = []
		while node != self.start_node:
			return_list.append([node.position_x, node.position_y])
			node = node.parent
		return return_list
		

	def attach_and_eval(self, parent, child):
		""" The attach_and_eval function """
		child.parent = parent
		child.g = parent.g + self.cartesian_distance(parent, child)
		child.f = child.g + self.cartesian_distance(child, self.end_node)

	def propagate_path_improvements(self, node):
		""" The propagate_path_improvements function """
		for child in node.children:
			if node.g + self.cartesian_distance(node, child) < child.g:
				child.parent = node
				child.g = node.g + self.cartesian_distance(node, child)
				child.f = child.g + self.cartesian_distance(child, self.end_node)
				self.propagate_path_improvements(child)


