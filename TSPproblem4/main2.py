import numpy as np
from functions import load_instance, get_coords, create_distances_matrix
from iteratedlocalgreedy import IteratedLocalSearchGreedy
import time
from visualisation import plot_result

pathA = "kroA200.tsp"
pathB = "kroB200.tsp"

def start_solution(coords, n=100):
    idxes = np.arange(len(coords))
    visited = np.random.choice(idxes, n, replace=False)
    not_visited = np.array(list(set(idxes) - set(visited)))
    return visited, not_visited
def prepare_coords_and_matrix(path):
    problem = load_instance(path)
    coords = get_coords(problem)
    return create_distances_matrix(coords), coords
def do(matrix, iter, coords):

    all_visited = []
    all_distance = []
    all_time = []
    for i in range(1):
        start, not_start = start_solution(coords)
        time1 = time.time()
        best_distance, best_visited, best_not_visited = iter.alghorithm1(matrix, start, not_start)
        resutl_time = time.time() - time1
        all_time.append([resutl_time])
        all_distance.append([best_distance])
        all_visited.append([best_visited])
    return np.array(all_distance), np.array(all_visited), np.array(all_time)

def statistic(all_distance):
    best = all_distance.argmin(axis=0)
    mean = all_distance.mean(axis=0)
    worst = all_distance.max(axis=0)
    return best, worst, mean


#matrixA, coordsA = prepare_coords_and_matrix(pathA)
matrixB, coordsB = prepare_coords_and_matrix(pathB)





# iter = IteratedLocalSearchGreedy(mean_time_msls=3200.22)
# all_distanceA, all_visitedA, all_timeA = do(matrixA,iter, coordsA)
iter = IteratedLocalSearchGreedy(mean_time_msls=3100.6)
all_distanceB, all_visitedB, all_timeB = do(matrixB, iter, coordsB)
# best, worst, mean = statistic(all_distanceA)
# bestT, worstT, meanT  = statistic(all_timeA)
# print("Best  distances for korA200:")
# print(" Iterated local search 1")
# print(all_distanceA[best[0]][0])
# print("Worst distances for kro200:")
# print(" Iterated local search 1")
# print(worst[0])
# print("Means distances for kroA200:")
# print(" Iterated local search 1")
# print(mean[0])
# print("Best  time for korA200:")
# print(" Iterated local search 1")
# print(round(all_timeA[bestT[0]][0], 2))
# print("Worst time for kroA200:")
# print(" Iterated local search 1")
# print(round(worstT[0],2))
# print("Means time for kroA200:")
# print(" Iterated local search 1")
# print(round(meanT[0],2))
#
#
# plot_result(coordsA, all_visitedA[best[0]][0], "Iteratedlocalsearch1_A.png")

#
#
best, worst, mean = statistic(all_distanceB)
bestT, worstT, meanT  = statistic(all_timeB)

print("--------------------------------------------------------------------------")
print("Best  distances for korB200:")
print(" Iterated local search 1")
print(all_distanceB[best[0]][0])
print("Worst distances for kroB200:")
print(" Iterated local search 1")
print(worst[0])
print("Means distances for kroB200:")
print(" Iterated local search 1")
print(mean[0])
print("Best  time for korB200:")
print(" Iterated local search 1")
print(round(all_timeB[bestT[0]][0], 2))
print("Worst time for kroB200:")
print(" Iterated local search 1")
print(round(worstT[0],2))
print("Means time for kroB200:")
print(" Iterated local search 1")
print(round(meanT[0],2))

plot_result(coordsB, all_visitedB[best[0]][0], "Iteratedlocalsearch1_B.png")
