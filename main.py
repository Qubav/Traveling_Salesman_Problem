from solution import Solution
from fi_algorithm import FIAlgorithm


if __name__ == "__main__":

    problem_data = {
        "coordinates_path": "berlin52.txt",
        "correct_order_path": "berlin52.opt.tour.txt"
    }

    sol1 = Solution(problem_data)
    sol1.get_correct_order()
    sol1.get_coordinates()
    sol1.get_distance_matrix()

    fi_alg = FIAlgorithm(sol1)
    print(fi_alg.solution.y)
    fi_alg.algorithm()
    sol1.show_solution()
    sol1.get_tour_distance()
    print(sol1.correct_order_distance)
    print(sol1.starting_distance)
    print(sol1.starting_distance / sol1.correct_order_distance * 100 - 100)
