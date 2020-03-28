from functions import load_instance, get_coords, create_distances_matrix
import random
from nearest_neighbor import NearesNeighbor
from regret import Regret
from greedy_cycle import GreedCycle
import numpy as np
from visualisation import plot_result
pathA = "kroA100.tsp"
pathB = "kroB100.tsp"

def prepare_coords_and_matrix(path):
    problem = load_instance(path)
    coords = get_coords(problem)
    return create_distances_matrix(coords), coords
def do(matrix, reg, gre):

    all_visited = []
    all_distance = []
    num = int(matrix.shape[0] / 2)
    for n in range(10):
        start = random.randint(0, num * 2 - 1)
        distanceSum_reg, visited_reg = reg.alghorithm(matrix, start)
        distanceSum_gre, visited_gre = gre.alghorithm(matrix, start)
        all_distance.append([distanceSum_reg, distanceSum_gre])
        all_visited.append([visited_reg, visited_gre])
    return np.array(all_distance), np.array(all_visited)
def statistic(all_distance):
    best = all_distance.argmin(axis=0)
    mean = all_distance.mean(axis=0)
    worst = all_distance.max(axis=0)
    return best, worst, mean

matrixA, coordsA = prepare_coords_and_matrix(pathA)

matrixB, coordsB = prepare_coords_and_matrix(pathB)
reg = Regret()
gre = GreedCycle()

all_distanceA, all_visitedA = do(matrixA, reg, gre)
all_distanceB, all_visitedB = do(matrixB, reg, gre)
best, worst, mean = statistic(all_distanceA)
print("Best  distances for korA100:")
print("Regret  Greedy")
print(all_distanceA[best[0]][0], " ", all_distanceA[best[1]][1])
print("Worst distances for kroA100:")
print("Regret  Greedy")
print(worst[0], " ", worst[1])
print("Means distances for kroA100:")
print("Regret  Greedy")
print(mean[0], " ", mean[1])
plot_result(coordsA, all_visitedA[best[0]][0], "Regret_A.png", "Algorytm zachłanny z żalem dla kroA100")
plot_result(coordsA, all_visitedA[best[1]][1], "Greedy_A.png", "Algorytm zachłanny dla kroA100")


best, worst, mean = statistic(all_distanceB)

print("Best  distances for korB100:")
print("Regret  Greedy")
print(all_distanceB[best[0]][0], " ", all_distanceB[best[1]][1])
print("Worst distances for kroB100:")
print("Regret  Greedy")
print(worst[0], " ", worst[1])
print("Means distances for kroB100:")
print("Regret  Greedy")
print(mean[0], " ", mean[1])
plot_result(coordsB, all_visitedB[best[0]][0], "Regret_B.png", "Algorytm zachłanny z żalem dla kroB100")
plot_result(coordsB, all_visitedB[best[1]][1], "Greedy_B.png", "Algorytm zachłanny dla kroB100")
