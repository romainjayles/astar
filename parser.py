#! /usr/bin/python
# -*- coding:utf-8 -*-

import array
import numpy
import re

class Parser:
	""" Allow to parse a path file as describe in the exercise """

	# The constant for representing type of node
	FREE = 0
	START = 1
	END = 2
	OBSTACLE = 3

	def __init__(self, input_file):
		""" The initialisation of the parser """
		# The name of the imput file
		self.input_file = input_file
		# The height of the grid
		self.height = None
		# The lenght of the grid
		self.length = None
		# The matrix reprenting the grid
		self.field = {}
		self.start = None
		self.end = None

	def parse(self):
		""" Parse the file in self.input_file """
		in_file = open(self.input_file, "r")
		# The point containing juste two coordinates
		simple_point = re.compile('\([0-9]*,[0-9]*\)')
		# The points representing by four coordinates
		complex_point = re.compile('\([0-9]*,[0-9]*,[0-9]*,[0-9]*\)')
		simple_point_list = []
		complex_point_list = []
		for line in in_file:
			simple_point_result = simple_point.findall(line)
			complex_point_result = complex_point.findall(line)
			simple_point_list.append(simple_point_result)
			complex_point_list.append(complex_point_result)
		self.generate_map(self.clear_list(simple_point_list), self.clear_list(complex_point_list))
		return self.field

	def clear_list(self, list):
		return_list = []
		for member in list:
			for sub_member in member:
				return_list.append(sub_member)
		return return_list

	def coordinate_string_to_array(self, coordinate_string):
		""" Convert a string representing coordinates into an array """
		# input : '(1,1)' -> output : [1,1]
		coordinate_string = coordinate_string[1:-1]
		coordinate_string =  coordinate_string.split(',')
		return_coordinate = []
		for item in coordinate_string:
			return_coordinate.append(int(item))
		return return_coordinate

	def generate_map(self, simple_point_list, complex_point_list):
		""" Create the map with the line parsed from the file """
		# The dimension is contained in the first couple
		dimension = self.coordinate_string_to_array(simple_point_list[0])
		# The starting position is contained in the second couple
		self.start = self.coordinate_string_to_array(simple_point_list[1])
		# The ending position is contained in the last couple
		self.end = self.coordinate_string_to_array(simple_point_list[2])
		self.height = dimension[0]
		self.length = dimension[1]
		# Creation of an empty matrix which represent the map
		self.field = numpy.zeros((self.height,self.length))
		# Positionning the start point
		self.field[self.start[0]][self.start[1]] = Parser.START
		# Positionning the end point
		self.field[self.end[0]][self.end[1]] = Parser.END
		# For each point we now check if it's an obstacle or a free space
		for i in range(0, self.height):
			for j in range(0, self.length):
				for obstacle_string in complex_point_list :
					obstacle = self.coordinate_string_to_array(obstacle_string)
					obstacle_basis = obstacle[0:2]
					obstacle_height = obstacle[2]
					obstacle_length = obstacle[3]
					condition_height = (i < obstacle_basis[0] + obstacle_height) and (i >= obstacle_basis[0])
					condition_length = (j < obstacle_basis[1] + obstacle_length) and (j >= obstacle_basis[1])
					if condition_length and condition_height:
						self.field[i][j] = Parser.OBSTACLE

		self.print_map()

	def print_map(self):
		""" Allow to print the map on the standart output """
		printed_field = numpy.zeros((self.length,self.height))
		transpose_field = self.field.transpose()
		for i in range(0, self.length):
			for j in range(0, self.height):
				printed_field[self.length-i-1][j] = transpose_field[i][j]
		print printed_field
