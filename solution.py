import numpy as np
from numpy import sqrt, power
from matplotlib import pyplot as plt

class Solution:

    def __init__(self, data: dict) -> None:
        self.coordinates_path = data["coordinates_path"]
        self.correct_order_path = data["correct_order_path"]
        self.correct_order = []
        self.current_solution = []
        self.x = []
        self.y = []

    
    def get_correct_order(self) -> None:
        """Function reads correct locations order from .txt file and updates attribute correct_order with ids of next in order location."""

        with open(self.correct_order_path, "r") as file:
            order = file.read().splitlines()
        
        # -1 because in txt file id of 1st location is 1, but for project purpose it needs to be 0
        for id in order:
            self.correct_order.append(int(id) - 1)

        # appending 1st location to end of order because traveling salesman must comeback to this location
        self.correct_order.append(self.correct_order[0])
    
    def get_coordinates(self) -> None:
        """Function reads coordinates of subsequent locations from .txt file and updates x and y attributes with the corresponding values."""

        with open(self.coordinates_path, "r") as file:
            coordinates = file.read().splitlines()
        
        # cities in txt file are written like this: location number (space) x coordinate (space) y coordinate
        # appending read values into attributes
        for city in coordinates:
            temp = city.split()
            self.x.append(float(temp[1]))
            self.y.append(float(temp[2]))

    def get_distance(self, id1: int, id2: int) -> int:
        """Function returns value of distance in between locations with ids id1 and id2."""

        return int(0.5 + sqrt(power((self.x[id1] - self.x[id2]), 2) + power((self.y[id1] - self.y[id2]), 2)))

    def get_distance_matrix(self) -> None:
        """Function creates matrix with values of distance between each city is database based on coordinates from x and y attributes."""

        # creating matrix
        n = len(self.x)
        distance_matrix = np.zeros((n, n), int)

        # calculating and updating matrix values
        for i in range(0, n, 1):
            for j in range(0, n, 1):
                distance_matrix[i, j] = self.get_distance(i, j)

        self.distance_matrix = distance_matrix

    def get_tour_distance(self, opt: bool = False) -> int:
        
        tour_distance = 0

        # tour distance value is calculated by adding up distance between cities that are after each other in order
        # if opt is False calculated value is calculated based on current solution order, if opt is True tour distance value is calculated based on correct order
        if opt is False:
            for i in range(0, len(self.current_solution) - 1):
                tour_distance += self.distance_matrix[self.current_solution[i], self.current_solution[i + 1]]

        else:
            for i in range(0, len(self.correct_order) - 1):
                tour_distance += self.distance_matrix[self.correct_order[i], self.correct_order[i + 1]]
       
        return tour_distance
    
    def show_solution(self):

        plt.figure()
        plt.title("Solution")
        x = []
        y = []
        for id in self.current_solution:
            x.append(self.x[id])
            y.append(self.y[id])

        plt.plot(x, y, "o-k", linewidth = 1.5, markersize = 3.0)
        plt.show()
