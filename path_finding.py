#! /usr/bin/python
# -*- coding:utf-8 -*-

import Astar
import parser
import node
from math import sqrt


class PathFinding:

    """ This class interface the Astar algorithm with the path finding problem """

    def __init__(self, field, start_position, end_position):
        self.field = field
        start_node = node.Node(start_position[0], start_position[1])
        end_node = node.Node(end_position[0], end_position[1])
        start_node.g = 0
        start_node.f = self.cartesian_distance(start_node, end_node)
        self.Astar_instance = Astar.Astar(
            start_node,
            end_node,
            heuristic_function=self.cartesian_distance,
            generate_sucessors_function=self.generate_sucessors)

    def solve(self, list_management_function, display_function):
        return self.Astar_instance.solve(list_management_function, display_function)

    def cartesian_distance(self, node1, node2):
        """
        Cartesian distance between two points.
        Used as the heuristic
        """
        distance = sqrt((node1.position_y - node2.position_y)
                        ** 2 + (node1.position_x - node2.position_x) ** 2)
        return distance

    def generate_sucessors(self, node):
        """ Generate the next possible position from (node.x, node.y) """
        x = node.position_x
        y = node.position_y
        succ = [
            self.connect_node_to_node(node, x - 1, y - 1),
            self.connect_node_to_node(node, x - 1, y),
            self.connect_node_to_node(node, x - 1, y + 1),
            self.connect_node_to_node(node, x + 1, y - 1),
            self.connect_node_to_node(node, x + 1, y),
            self.connect_node_to_node(node, x + 1, y + 1),
            self.connect_node_to_node(node, x, y - 1),
            self.connect_node_to_node(node, x, y + 1)
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
