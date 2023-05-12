import numpy as np
from numpy import sqrt, power
from matplotlib import pyplot as plt

class Solution:

    def __init__(self, data: dict) -> None:

        # attributes that stores paths to data
        self.coordinates_path = data["coordinates_path"]
        self.correct_order_path = data["correct_order_path"]

        # attributes that stores cities order and tours distance
        self.correct_order = []
        self.correct_order_distance = 0
        self.final_order = []
        self.final_distance = 0
        self.starting_order = []
        self.starting_distance = 0

        # coordinates of cities in ids order
        self.x = []
        self.y = []

        self.get_correct_order()
        self.get_coordinates()
        self.get_distance_matrix()

    
    def get_correct_order(self) -> None:
        """Method reads correct locations order from .txt file and updates attribute correct_order with ids of next in order location."""

        with open(self.correct_order_path, "r") as file:
            order = file.read().splitlines()
        
        # -1 because in txt file id of 1st location is 1, but for project purpose it needs to be 0
        for id in order:
            self.correct_order.append(int(id) - 1)

        # appending 1st location to end of order because traveling salesman must comeback to this location
        self.correct_order.append(self.correct_order[0])

    
    def get_coordinates(self) -> None:
        """Method reads coordinates of subsequent locations from .txt file and updates x and y attributes with the corresponding values."""

        with open(self.coordinates_path, "r") as file:
            coordinates = file.read().splitlines()
        
        # cities in txt file are written like this: location number (space) x coordinate (space) y coordinate
        # appending read values into attributes
        for city in coordinates:
            temp = city.split()
            self.x.append(float(temp[1]))
            self.y.append(float(temp[2]))

    def get_distance(self, id1: int, id2: int) -> int:
        """Method returns value of distance in between locations with ids id1 and id2."""

        return int(0.5 + sqrt(power((self.x[id1] - self.x[id2]), 2) + power((self.y[id1] - self.y[id2]), 2)))

    def get_distance_matrix(self) -> None:
        """Method creates matrix with values of distance between each city is database based on coordinates from x and y attributes."""

        # creating matrix that will store values of distance from city to city
        n = len(self.x)
        distance_matrix = np.zeros((n, n), int)

        # calculating and updating matrix values
        for i in range(0, n, 1):
            for j in range(0, n, 1):
                distance_matrix[i, j] = self.get_distance(i, j)

        self.distance_matrix = distance_matrix

    def get_tour_distance(self) -> None:
        
        # tour distance value is calculated by adding up distance between cities that are after each other in order
        if len(self.final_order) > 0:
            tour_distance = 0
            for i in range(0, len(self.final_order) - 1):
                tour_distance += self.distance_matrix[self.final_order[i], self.final_order[i + 1]]

            self.final_distance = tour_distance

        if len(self.starting_order) > 0:
            tour_distance = 0
            for i in range(0, len(self.starting_order) - 1):
                tour_distance += self.distance_matrix[self.starting_order[i], self.starting_order[i + 1]]
            
            self.starting_distance = tour_distance

        if len(self.correct_order) > 0 and self.correct_order_distance == 0:
            tour_distance = 0
            for i in range(0, len(self.correct_order) - 1):
                tour_distance += self.distance_matrix[self.correct_order[i], self.correct_order[i + 1]]
            
            self.correct_order_distance = tour_distance
       
    
    def show_solution(self):

        fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(6, 9))
        plt.subplots_adjust(top=0.959,bottom=0.065,left=0.132,right=0.975,hspace=0.376,wspace=0.225)

        axs[0].set_title("Optimal solution")
        axs[0].set_xlabel("x coordinates")
        axs[0].set_ylabel("y coordinates")

        x_0 = []
        y_0 = []

        for id in self.correct_order:
            x_0.append(self.x[id])
            y_0.append(self.y[id])

        axs[0].plot(x_0, y_0, "o-", linewidth = 1.5, markersize = 3.0, color = "royalblue")

        axs[1].set_title("FI algorithm solution")
        axs[1].set_xlabel("x coordinates")
        axs[1].set_ylabel("y coordinates")

        x_1 = []
        y_1 = []

        for id in self.starting_order:
            x_1.append(self.x[id])
            y_1.append(self.y[id])

        axs[1].plot(x_1, y_1, "o-", linewidth = 1.5, markersize = 3.0, color = "darkorange")

        axs[2].set_title("Tabu Search algorithm solution")
        axs[2].set_xlabel("x coordinates")
        axs[2].set_ylabel("y coordinates")

        x_2 = []
        y_2 = []

        for id in self.final_order:
            x_2.append(self.x[id])
            y_2.append(self.y[id])

        axs[2].plot(x_2, y_2, "o-", linewidth = 1.5, markersize = 3.0, color = "limegreen")

        plt.show()

    def print_values(self):

        print(f"Correct order distance value is: {self.correct_order_distance}")
        print(f"FI algorithm order distance value is: {self.starting_distance}")
        print(f"Tabu Search algorithm distance value is: {self.final_distance}")
        fi_c_diff = (self.starting_distance / self.correct_order_distance - 1) * 100
        ts_c_diff = (self.final_distance / self.correct_order_distance - 1) * 100
        ts_fi_diff = (self.starting_distance / self.final_distance - 1) * 100
        print(f"The difference between the lengths of the correct order and FI algorithm order is: {fi_c_diff} %")
        print(f"The difference between the lengths of the correct order and Tabu Search algorithm order is: {ts_c_diff} %")
        print(f"The difference between the lengths of the FI algorithm order and Tabu Search algorithm order is: {ts_fi_diff} %")
