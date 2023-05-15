# Traveling Salesman Problem

The Traveling Salesman Problem (TSP) is a classic optimization problem in computer science and mathematics. Its goal is to find the shortest possible route that a traveling salesman can take to visit a given set of cities and return to his starting point.\
Project allows to solve TSP using Farthest Insertion algorithm to create initial solution and Tabu Search algorithm to try to find a solution as close to the optimal one as possible.\
Program:
- reads .txt files to get data about cities coordinates and correct cities order(data from http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/)
- allows user to execute FI and TS algorithms,
- allows user to plot graphs showing course of routes for optimal solution, initial solution created with FI algorithm and final solution created with TS algorithm,
- print each solution values - total tour distance

# Demo for Berlin52 dataset:
Values of distances for correct cities order and order determined by FI and TS algorithms:
- Correct order distance value is: 7542
- FI algorithm order distance value is: 8402
- Tabu Search algorithm distance value is: 7542
- The difference between the lengths of the correct order and FI algorithm order is: 11.402810925483964 %
- The difference between the lengths of the correct order and Tabu Search algorithm order is: 0.0 %
- The difference between the lengths of the FI algorithm order and Tabu Search algorithm order is: 11.402810925483964 %
\Routs graphs:\
![Figure_1](https://github.com/Qubav/Traveling_Salesman_Problem/assets/124883831/d8dc9a97-7327-4e35-b30d-5c9464430922)\
Attributes change diruing Tabu Search - algorithm current solution distance and best solution distance change:\
![Figure_2](https://github.com/Qubav/Traveling_Salesman_Problem/assets/124883831/9d7cab7d-260d-487a-b1d4-34b660b250a9)
