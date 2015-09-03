#! /usr/bin/python
# -*- coding:utf-8 -*-

class Node(object):
	""" A simple implementation for the node of a tree """

	def __init__(self, position_x, position_y):
		""" The initialisation of the object """
		self.position_x = position_x
		self.position_y = position_y
		self.g = None
		self.f = None
		# The parent node
		self.parent = None
		# The list of child node
		self.children = []

	def add_child(self, obj):
		""" Allow to add a child to a parent node """
		self.children.append(obj)

	def __str__(self):
		""" String representation, used for debuging """
		return_string = '(' + str(self.position_x) + ', ' + str(self.position_y) +') ' + str(self.f) + '-> '
		for child in self.children:
			return_string += '(' + str(child.position_x) + ', ' + str(child.position_y) +') -- '
		return return_string

	def __eq__(self, obj):
		""" 
		Equals method based on the position of this node
		A node is equal to an other if they have the same position 
		"""
		return self.position_x == obj.position_x and self.position_y == obj.position_y

	def __ne__(self, obj):
		return not self.__eq__(obj)