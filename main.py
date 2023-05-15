from solution import Solution
from fi_algorithm import FIAlgorithm
from tabu_search import TabuSearch

TABU_TENURE = 16
ITERATIONS = 2500

BERLIN = {
        "coordinates_path": "berlin52.txt",
        "correct_order_path": "berlin52.opt.tour.txt"
    }

ATT = {
        "coordinates_path": "att48.txt",
        "correct_order_path": "att48.opt.txt"
    }

EIL = {
        "coordinates_path": "eil101.txt",
        "correct_order_path": "eil101.opt.txt"
    }

if __name__ == "__main__":

    sol1 = Solution(BERLIN)
    fi_alg = FIAlgorithm(sol1)
    tabu_search = TabuSearch(sol1, TABU_TENURE, ITERATIONS)
    sol1.print_values()
    sol1.show_solution()
    tabu_search.plot_distance_values_change()
    

    
        