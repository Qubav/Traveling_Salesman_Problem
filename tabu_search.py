import random
from solution import Solution
from matplotlib import pyplot as plt

class TabuSearch:

    def __init__(self, solution: Solution, tabu_tenure: int, iterations: int) -> None:

        self.solution = solution

        # attributes used in process of Tabu Search algorithm
        self.tabu_list = []
        self.best_solution = self.solution.starting_order[:]
        self.current_solution = self.solution.starting_order[:]
        self.best_solution_distance = self.solution.starting_distance
        self.current_solution_distance = self.solution.starting_distance
        self.tabu_tenure = tabu_tenure      # length of list with forbidden attributes
        self.iterations = iterations

        # attributes to store values of other attributes over algorithm iterations
        self.current_solution_distance_change_list = []
        self.best_solution_distance_change_list = []

        self.tabu_search_algorithm()
        

    def distance_change(self, id_1: int, id_2: int, id_3: int, id_4: int) -> int:
        """Method returns change in tour distance value if cities are connected id_1 - id_3 and id_2 - id_4 instead of id_1 - id_2 and id_3 - id_4."""
        
        return self.solution.distance_matrix[id_1, id_3] + self.solution.distance_matrix[id_2, id_4] - self.solution.distance_matrix[id_1, id_2] - self.solution.distance_matrix[id_3, id_4]

    def check_tabu(self, new_candidate: list) -> bool:
        """Method checks if there is forbidden attribute in new_candidate."""

        # loop through all forbidden attributes - forbidden attribute is two specified cities being next to each other in order
        for tabu in self.tabu_list:
            
            # getting ids of cities that can;t be next to each other in order
            id_1 = tabu[0]
            id_2 = tabu[1]

            # getting position of one of the cities in order and checking if second city is in position before or after in order
            city_id_1_placement = new_candidate.index(id_1)
            if new_candidate[city_id_1_placement - 1] == id_2 or new_candidate[city_id_1_placement + 1] == id_2:

                # if cities are next to each other method returns True
                return True

        # if through loop method didn't return True that means there are no forbidden attributes in order so method returns False  
        return False

    def tabu_search_algorithm(self):
        """Method executes the Tabu Search algorithm."""
        # appending attributes values to lists to see their change over iterations
        self.best_solution_distance_change_list.append(self.best_solution_distance)  
        self.current_solution_distance_change_list.append(self.current_solution_distance)  

        # loop
        # finding new best neighborhood - solution that is possible to achieve with one move - used moves -> 2 opt swap - example. cities order a-b-c-d-e-f -> a-d-c-b-e-f 
        for k in range(self.iterations):

            order = self.current_solution[:]
            base_distance = self.current_solution_distance
            min_dist_change  = self.best_solution_distance
            best_sol_dist = self.best_solution_distance
            tabu_index = -1


            # loop through all possible neighborhoods - solutions that can be achieved with 1 move starting from 1 solution
            # loop goal is to find best possible neighborhood
            for i in range(1, len(order)):
                for j in range(i + 2, len(order)):
                    
                    # calculating distance change for this solution - move is 2 opt swap
                    # new_dist_change = self.distance_change(self.current_solution[i - 1], self.current_solution[i], self.current_solution[j - 1], self.current_solution[j])
                    new_dist_change = self.distance_change(order[i - 1], order[i], order[j - 1], order[j])

                    # if new_dist_change is better than min_dist_change(lowest dist change value achieved -> shortest tour distance)
                    # order for this swap will be checked if it doesn't have tabu
                    if new_dist_change < min_dist_change:
                        new_candidate = order[:]
                        new_candidate[i: j] = new_candidate[j - 1: i - 1: -1]   # swapping cities order between cities i(included) and j - 1(included)
                        tabu_val = self.check_tabu(new_candidate)

                        # if there is no tabu variables are updated
                        if tabu_val is False:
                            min_dist_change = new_dist_change
                            best = new_candidate[:]
                            # setting up tabu_index to know two cities that are next to each other in current solution, but wont be in new that we found
                            # cities being next to each other will be forbidden to not come to this exact solution again in next few iterations - based on tabu_tenure attribute value
                            tabu_index = i

                            # if this solutions distance is better than best solution distance ever get it is updated to this distance in this method, because
                            # it is used to ignore tabu if solution gets tour distance better than any other solution before
                            if new_dist_change + base_distance < best_sol_dist:
                                best_sol_dist = new_dist_change + base_distance
                        
                        # if tabu_val is True but solution distance is better than ever before this solution is accepted
                        elif new_dist_change + base_distance < best_sol_dist:
                            min_dist_change = new_dist_change
                            best = new_candidate[:]
                            best_sol_dist = new_dist_change + base_distance
                            tabu_index = i
            
            if tabu_index == -1:
                self.tabu_list.append([0, 0])
                # no solution found, blank tabu appended to tabu list should make it possible in next iteration
                # no updates
            
            else:
                # updating attributes
                self.tabu_list.append([order[tabu_index - 1], order[tabu_index]])
                self.current_solution = best[:]
                self.current_solution_distance = min_dist_change + base_distance

                if min_dist_change + base_distance < self.best_solution_distance:
                    self.best_solution_distance = min_dist_change + base_distance
                    self.best_solution = best[:]

            # if length of tabu_list attribute has value higher than tabu_tenure attribute oldest tabu is removed from list
            if len(self.tabu_list) > self.tabu_tenure:
                self.tabu_list.pop(0)

            # to make process more random if this condition is met random tabu is removed from tabu_list attribute
            if k % 25 == 0:
                tabu_to_remove = random.choice(self.tabu_list)
                self.tabu_list.remove(tabu_to_remove)

            # attributes update
            self.best_solution_distance_change_list.append(self.best_solution_distance)  
            self.current_solution_distance_change_list.append(self.current_solution_distance)     
        
        # setting up solutions attributes to best order and its distance
        self.solution.final_order = self.best_solution[:]
        self.solution.final_distance = self.best_solution_distance

    def plot_distance_values_change(self):
        """Method shows graph of change of the values of attributes best_solution_distance and current_solution_distance over iterations."""

        plt.figure()
        plt.title("Change of values over the iteration")
        plt.plot(self.best_solution_distance_change_list, color = "royalblue", label = "best solution distance")
        plt.plot(self.current_solution_distance_change_list, color = "darkorange", label = "current solution distance")
        plt.legend()
        plt.xlabel("iterations")
        plt.ylabel("distance value")
        plt.show()
