import numpy as np
from functions import load_instance, get_coords, create_distances_matrix
from multiplegreedy import MultipleStartLocalSearch
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
def do(matrix, msls, coords):

    all_visited = []
    all_distance = []
    all_time = []
    min_distnance_multiply_greedy = 30000
    time_greedy = 0
    visited_greedy=[]
    for i in range(2):
        for n in range(3):
            start, not_start = start_solution(coords)
            time1 = time.time()
            best_distance, best_visited, best_not_visited = msls.alghorithm(matrix, start, not_start)
            resutl_time = time.time() - time1
            if min_distnance_multiply_greedy>best_distance:
                min_distnance_multiply_greedy = best_distance
                time_greedy = resutl_time
                visited_greedy = best_visited
        all_time.append([time_greedy])
        all_distance.append([min_distnance_multiply_greedy])
        all_visited.append([visited_greedy])
    return np.array(all_distance), np.array(all_visited), np.array(all_time)

def statistic(all_distance):
    best = all_distance.argmin(axis=0)
    mean = all_distance.mean(axis=0)
    worst = all_distance.max(axis=0)
    return best, worst, mean


matrixA, coordsA = prepare_coords_and_matrix(pathA)
matrixB, coordsB = prepare_coords_and_matrix(pathB)
msls = MultipleStartLocalSearch()





all_distanceA, all_visitedA, all_timeA = do(matrixA,msls, coordsA)
all_distanceB, all_visitedB, all_timeB = do(matrixB, msls, coordsB)
best, worst, mean = statistic(all_distanceA)
bestT, worstT, meanT  = statistic(all_timeA)
print("Best  distances for korA200:")
print(" MultipleStartLocalSearch")
print(all_distanceA[best[0]][0])
print("Worst distances for kro200:")
print(" MultipleStartLocalSearch")
print(worst[0])
print("Means distances for kroA200:")
print(" MultipleStartLocalSearch")
print(mean[0])
print("Best  time for korA200:")
print(" MultipleStartLocalSearch")
print(round(all_timeA[bestT[0]][0], 2))
print("Worst time for kroA200:")
print(" MultipleStartLocalSearch")
print(round(worstT[0],2))
print("Means time for kroA200:")
print(" MultipleStartLocalSearch")
print(round(meanT[0],2))


plot_result(coordsA, all_visitedA[best[0]][0], "MultipleStartLocalSearch_A.png")



best, worst, mean = statistic(all_distanceB)
bestT, worstT, meanT  = statistic(all_timeB)

print("--------------------------------------------------------------------------")
print("Best  distances for korB200:")
print(" MultipleStartLocalSearch")
print(all_distanceB[best[0]][0])
print("Worst distances for kroB200:")
print(" MultipleStartLocalSearch")
print(worst[0])
print("Means distances for kroB200:")
print(" MultipleStartLocalSearch")
print(mean[0])
print("Best  time for korB200:")
print(" MultipleStartLocalSearch")
print(round(all_timeA[bestT[0]][0], 2))
print("Worst time for kroB200:")
print(" MultipleStartLocalSearch")
print(round(worstT[0],2))
print("Means time for kroB200:")
print(" MultipleStartLocalSearch")
print(round(meanT[0],2))

plot_result(coordsB, all_visitedB[best[0]][0], "MultipleStartLocalSearch_B.png")
