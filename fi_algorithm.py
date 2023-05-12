from numpy import sqrt
from random import sample
from solution import Solution

# class allows to build starting order based on Farthest Insertion method
# method explained: https://users.cs.cf.ac.uk/C.L.Mumford/howard/FarthestInsertion.html

class FIAlgorithm:

    def __init__(self, solution: Solution) -> None:
        self.solution = solution
        self.algorithm(randomness = True)
    
    def get_min_distance_from_edge(self, a: list, b: list, e: list) -> float:
        """Method returns value of closest distance from point e to edge between points a and b."""

        ab = [None, None]
        ab[0] = b[0] - a[0]
        ab[1] = b[1] - a[1]

        be = [None, None]
        be[0] = e[0] - b[0]
        be[1] = e[1] - b[1]

        ae = [None, None]
        ae[0] = e[0] - a[0]
        ae[1] = e[1] - a[1]

        ab_be = ab[0] * be[0] + ab[1] * be[1]
        ab_ae = ab[0] * ae[0] + ab[1] * ae[1]
        reqAns = 0

        if ab_be > 0:

            y = e[1] - b[1]
            x = e[0] - b[0]
            reqAns = sqrt(x * x + y * y)

        elif ab_ae < 0:
            y = e[1] - a[1]
            x = e[0] - a[0]
            reqAns = sqrt(x * x + y * y)

        else:
            x1 = ab[0]
            y1 = ab[1]
            x2 = ae[0]
            y2 = ae[1]
            mod = sqrt(x1 * x1 + y1 * y1)
            # if mod == 0:
            #     mod = np.power(0.1, 100)
            reqAns = abs(x1 * y2 - y1 * x2) / mod
        
        return reqAns

    def calculate_distance_change(self, a: int, b: int, p: int) -> int:
        """Method returns value of subtraction edge between cities a-b distance from combined value of edges between cities a-p and p-b."""
        edge_dist = self.solution.get_distance(a, b)
        new_dist = self.solution.get_distance(a, p) + self.solution.get_distance(p, b)

        return new_dist - edge_dist


    def algorithm(self, randomness = False) -> None:
        
        # variables
        order = []      # stores ids of cities in order to be visited
        included = {}    # stores bool value True or False that tells if city with given id was already included in order. Key - str id    Value - bool True/False

        # filling dictionary with string ids as keys and bool False as values
        for id in range(len(self.solution.x)):
            included[str(id)] = False

        if randomness is True:
            # generates 3 random starting locations to start algorithm
            first_3_locations = sample(range(len(self.solution.x)), 3)    
            
            # appending generated locations to order list and changing value in included to True
            for loc in first_3_locations:
                order.append(loc)
                included[str(loc)] = True

            order.append(order[0])

        else:
            a_b_found = False
            a_b_distance  = self.solution.distance_matrix.max()

            for i in range(len(self.solution.x)):
                for j in range(i + 1, len(self.solution.x)):
                    if self.solution.distance_matrix[i, j] == a_b_distance:
                        a_b_found = True
                        city_a = i
                        city_b = j
                    
                    if a_b_found is True:
                        break
                if a_b_found is True:
                    break
            
            c_dist = 0
            a_coordinates = [self.solution.x[city_a], self.solution.y[city_a]]
            b_coordinates = [self.solution.x[city_b], self.solution.y[city_b]]
            for i in range(len(self.solution.x)):

                if i == city_a or i == city_b:
                    continue
                
                else:
                    test_coordinates = [self.solution.x[i], self.solution.y[i]]
                    if self.get_min_distance_from_edge(a_coordinates, b_coordinates, test_coordinates) > c_dist:
                        c_dist = self.get_min_distance_from_edge(a_coordinates, b_coordinates, test_coordinates)
                        city_c = i

            order.append(city_a)
            order.append(city_b)
            order.append(city_c)
            order.append(city_a)

            included[str(city_a)] = True
            included[str(city_b)] = True
            included[str(city_c)] = True

        # main loop in which each od the cities will be included in order    
        for _ in range(len(self.solution.x) - 3):

            # max_val is set to 0 so first higher value will take its place and will be value that is compared to other results
            # max_val is highest value that was received while checking distances between cities
            max_val = 0

            # looping through all combinations of pair of city included and city not included to find not included city with highest distance value to one od included cities
            for i in range(len(order) - 1):
                for j in range(len(self.solution.x)):
                    # only not included cities are checked
                    if included[str(j)] is False:
                        if max_val < self.solution.distance_matrix[order[i], j]:
                            max_val = self.solution.distance_matrix[order[i], j]
                            next_to_append = j      # variable stores id of city to be included next
            
            shortest_distance = max_val         # variable will be used to find edge in tour graph that is closest to city to be included

            for i in range(len(order) - 1):
                # variables are lists with coordinates of cities with specified ids
                # a and b are coordinates of cities already included, that are connected by "edge", p is coordinates of city to be included next 
                # d is closest distance from city to be included to edge between city a and city b
                a = [self.solution.x[order[i]], self.solution.y[order[i]]]
                b = [self.solution.x[order[i + 1]], self.solution.y[order[i + 1]]]
                p = [self.solution.x[next_to_append], self.solution.y[next_to_append]]
                d = self.get_min_distance_from_edge(a, b, p)

                # if distance between city to be added next is lower to different edge it is updated
                if d < shortest_distance:
                    shortest_distance = d
                    p_1 = (order[i], order[i + 1], next_to_append)
                    place = i + 1
                
                # if distance between city to be added next is equal to different edge it is compared byt calculating distance change if it would be added in order between 2 edge-defining cities
                # city will be added between those 2 cities so tour distance change value is lower
                elif d == shortest_distance:
                    p_2 = (order[i], order[i + 1], next_to_append)
                    place_2 = i + 1

                    dist_change_1 = self.calculate_distance_change(p_1[0], p_1[1], p_1[2])
                    dist_change_2 = self.calculate_distance_change(p_2[0], p_2[1], p_2[2])

                    if dist_change_1 > dist_change_2:
                        place = place_2

            # inserting next to be added city to order and changing value for its id in included dict to True
            order.insert(place, next_to_append)
            included[str(next_to_append)] = True
        
        self.solution.starting_order = order
        self.solution.get_tour_distance()

