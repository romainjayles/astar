#! /usr/bin/python
# -*- coding:utf-8 -*-

import parser
import Tkinter
import tkMessageBox
import sys
import path_finding


class Interface(Tkinter.Tk):

    HEIGHT = 600
    WIDTH = 600

    def __init__(self, parent, init_map):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.init_interface()
        self.circle_size = 0
        self.init_map = init_map
        self.map_height = init_map.shape[1]
        self.map_width = init_map.shape[0]
        self.diameter = min(
            self.WIDTH / (2 * self.map_width), self.HEIGHT / (2 * self.map_height))
        self.radius = self.diameter / 2

    def init_interface(self):
        self.grid()
        self.drawing_surface = Tkinter.Canvas(
            self, width=self.WIDTH, height=self.HEIGHT, background='white')
        self.drawing_surface.grid(column=1, row=0, rowspan=20)
        node_count_label = Tkinter.Label(self, text="Number of nodes :")
        lenght_path_label = Tkinter.Label(self, text="Total lenght :")

        self.node_count_area = Tkinter.StringVar()
        self.lenght_path_area = Tkinter.StringVar()

        node_count_area_label = Tkinter.Label(
            self, textvariable=self.node_count_area)
        lenght_path_area_label = Tkinter.Label(
            self, textvariable=self.lenght_path_area)

        self.display_node_created(0)
        self.display_lenght_path(0)

        button_bf = Tkinter.Button(
            self, text=u"Best First", command=self.BEF_click)
        button_df = Tkinter.Button(
            self, text=u"Depth First", command=self.DF_click)
        button_hf = Tkinter.Button(
            self, text=u"Breadth First", command=self.BRF_click)

        button_bf.grid(column=0, row=0)
        button_df.grid(column=0, row=1)
        button_hf.grid(column=0, row=2)
        node_count_label.grid(column=0, row=4)
        lenght_path_label.grid(column=0, row=7)

        node_count_area_label.grid(column=0, row=5)
        lenght_path_area_label.grid(column=0, row=8)

    def display_node_created(self, number_node):
        self.node_count_area.set(number_node)

    def display_lenght_path(self, lenght):
        self.lenght_path_area.set(round(lenght, 2))

    def treat_solution(self, solution):
        """ Handle the return of the solve function """
        if solution:
            self.print_solution(solution[0])
            self.display_node_created(solution[1])
            self.display_lenght_path(solution[2])
        else:
            tkMessageBox.showinfo("Warning", "Impossible to find a path")

    def BEF_click(self):
        """ Called when the Best First button is clicked """
        print "Best first"
        solution = path_solver_instance.solve(
            path_solver_instance.Astar_instance.best_first_list_management, self.display_path)
        self.treat_solution(solution)

    def DF_click(self):
        """ Called when the Depth First button is clicked """
        print "Depth first"
        solution = path_solver_instance.solve(
            path_solver_instance.Astar_instance.depth_first_list_management, self.display_path)
        self.treat_solution(solution)

    def BRF_click(self):
        """ Called when the Breadth First button is clicked """
        print "Breadth first"
        solution = path_solver_instance.solve(
            path_solver_instance.Astar_instance.breadth_first_list_management, self.display_path)
        self.treat_solution(solution)

    def display_path(self, path):
        """ Print the path given in argument on the screen """
        self.drawing_surface.delete("all")
        self.print_map()
        self.print_solution(path)
        self.update()

    def print_map(self):
        """ Print node on by one with the selection of the color """
        for i in range(0, self.map_width):
            for j in range(0, self.map_height):
                color = 'blue'
                if self.init_map[i][j] == 0:
                    color = 'white'
                elif self.init_map[i][j] == 1:
                    color = 'green'
                elif self.init_map[i][j] == 2:
                    color = 'red'
                self.place_node(i, j, color)

    def print_solution(self, solution):
        """ Color in red the node used by the solution """
        for point in solution:
            i = point[0]
            j = point[1]
            self.place_node(i, j, 'red')

    def place_node(self, i, j, color):
        """ Choose the right position for the node """
        self.create_circle(self.radius + (2 * i * self.diameter + self.radius), self.WIDTH - (
            self.radius + 2 * j * self.diameter + self.radius), self.radius, fill=color)

    def create_circle(self, x, y, r, **kwargs):
        """ Print a circle on the screen """
        return self.drawing_surface.create_oval(x - r, y - r, x + r, y + r, **kwargs)


def print_help():
    print "You must specify the scenario in first parameter as follow $ python Astar.py scenario.txt"

if __name__ == "__main__":
    try:
        input_file = sys.argv[1]
        parser_instance = parser.Parser(input_file)
        init_map = parser_instance.parse()
        app = Interface(None, init_map)
        app.title('A*')
        #astar = Astar.Astar(init_map, parser_instance.start, parser_instance.end)
        path_solver_instance = path_finding.PathFinding(
            init_map, parser_instance.start, parser_instance.end)
        app.print_map()
        app.mainloop()
    except IndexError:
        print_help()
