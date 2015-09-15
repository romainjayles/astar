#! /usr/bin/python
# -*- coding:utf-8 -*-


class Astar:

    """ Main class implemented the A* algorithm """

    def __init__(self, start_node, end_node, heuristic_function, generate_sucessors_function):
        """
        Initialisation of the Astar algorithm :
            start_node the node S0
            end_node the goal node
            heuristic_function the heuristic of the problem
            generate_sucessors_function a function which from a given node generate all the possible successors
        """
        self.node_created = {}
        # Creation of the start and end node
        self.start_node = start_node
        self.end_node = end_node
        # Value of f computed for the start node
        self.heuristic = heuristic_function
        self.generate_sucessors = generate_sucessors_function

    def compare_f(self, node1, node2):
        """ Used to compare the f value of two nodes """
        if node1.f > node2.f:
            return -1
        elif node1.f < node2.f:
            return 1
        else:
            return 0

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
        The list management function is the way the OPEN list will be managed.
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
                return (self.get_path(current), len(open_list) + len(closed_list), current.f)
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
                if fetched_from is None:
                    self.attach_and_eval(current, child_node)
                    list_management_function(open_list, child_node)
                elif current.g + self.heuristic(current, child_node) < child_node.g:
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
        child.g = parent.g + self.heuristic(parent, child)
        child.f = child.g + self.heuristic(child, self.end_node)

    def propagate_path_improvements(self, node):
        """ The propagate_path_improvements function """
        for child in node.children:
            if node.g + self.heuristic(node, child) < child.g:
                child.parent = node
                child.g = node.g + self.heuristic(node, child)
                child.f = child.g + \
                    self.heuristic(child, self.end_node)
                self.propagate_path_improvements(child)
