import numpy as np
from functions import load_instance, get_coords, create_distances_matrix
from steepest import Steepest
from greedy import Greedy
import time
from visualisation import plot_result

pathA = "kroA100.tsp"
pathB = "kroB100.tsp"

def start_solution(coords, n=50):
    idxes = np.arange(len(coords))
    visited = np.random.choice(idxes, n, replace=False)
    not_visited = np.array(list(set(idxes) - set(visited)))
    return visited, not_visited
def prepare_coords_and_matrix(path):
    problem = load_instance(path)
    coords = get_coords(problem)
    return create_distances_matrix(coords), coords
def do(matrix, steep, gre, coords):

    all_visited = []
    all_distance = []
    all_time = []
    for n in range(100):

        start, not_start = start_solution(coords)
        time1 = time.time()
        distanceSum_steep1, visited_steep1 = steep.alghorithm1(matrix, start, not_start) #verts
        resultSteep1 =  time.time() - time1
        time1 = time.time()
        distanceSum_gre1, visited_gre1 = gre.alghorithm1(matrix,  start, not_start) # verts
        resultGreed1 = time.time() - time1
        time1 =  time.time()
        distanceSum_steep2, visited_steep2 = steep.alghorithm2(matrix,  start, not_start) # edges
        resultSteep2 = time.time() - time1
        time1 = time.time()
        distanceSum_gre2, visited_gre2 = gre.alghorithm2(matrix,  start, not_start) #edges
        resultGreed2 = time.time() - time1
        all_time.append([resultSteep1,resultGreed1, resultSteep2, resultGreed2 ])
        all_distance.append([distanceSum_steep1,  distanceSum_gre1, distanceSum_steep2, distanceSum_gre2])
        all_visited.append([visited_steep1, visited_gre1,visited_steep2,visited_gre2])
    return np.array(all_distance), np.array(all_visited), np.array(all_time)

def statistic(all_distance):
    best = all_distance.argmin(axis=0)
    mean = all_distance.mean(axis=0)
    worst = all_distance.max(axis=0)
    return best, worst, mean


matrixA, coordsA = prepare_coords_and_matrix(pathA)

matrixB, coordsB = prepare_coords_and_matrix(pathB)
steep = Steepest()
gre = Greedy()

all_distanceA, all_visitedA, all_timeA = do(matrixA, steep, gre, coordsA)
all_distanceB, all_visitedB, all_timeB = do(matrixB, steep, gre, coordsB)
best, worst, mean = statistic(all_distanceA)
bestT, worstT, meanT  = statistic(all_timeA)
print("Best  distances for korA100:")
print("Steepest Vert | Greedy Vert |  Steepest Edges | Greedy Edges")
print(all_distanceA[best[0]][0], "         ", all_distanceA[best[1]][1], "           ", all_distanceA[best[2]][2],"          ", all_distanceA[best[3]][3])
print("Worst distances for kroA100:")
print("Steepest Vert | Greedy Vert |  Steepest Edges | Greedy Edges")
print(worst[0], "           ", worst[1], "            ", worst[2], "           ", worst[3])
print("Means distances for kroA100:")
print("Steepest Vert | Greedy Vert |  Steepest Edges | Greedy Edges")
print(mean[0], "          ", mean[1], "        ", mean[2], "       ", mean[3])
print("Best  time for korA100:")
print("Steepest Vert | Greedy Vert |  Steepest Edges | Greedy Edges")
print(round(all_timeA[bestT[0]][0], 2), "         ", round(all_timeA[bestT[1]][1], 2), "           ", round(all_timeA[bestT[2]][2],2),"          ", round(all_timeA[bestT[3]][3], 2))
print("Worst time for kroA100:")
print("Steepest Vert | Greedy Vert |  Steepest Edges | Greedy Edges")
print(round(worstT[0],2), "           ", round(worstT[1],2), "            ", round(worstT[2],2), "           ", round(worstT[3],2))
print("Means time for kroA100:")
print("Steepest Vert | Greedy Vert |  Steepest Edges | Greedy Edges")
print(round(meanT[0],2), "        ", round(meanT[1],2), "          ", round(meanT[2],2), "         ", round(meanT[3],2))


plot_result(coordsA, all_visitedA[best[0]][0], "Steepest_Vert_A.png")
plot_result(coordsA, all_visitedA[best[1]][1], "Greedy_Vert_A.png")
plot_result(coordsA, all_visitedA[best[2]][2], "Steepest_Edge_A.png")
plot_result(coordsA, all_visitedA[best[3]][3], "Greedy_Edge_A.png")




best, worst, mean = statistic(all_distanceB)
bestT, worstT, meanT  = statistic(all_timeB)

print("--------------------------------------------------------------------------")
print("Best  distances for korB100:")
print("Steepest Vert | Greedy Vert |  Steepest Edges | Greedy Edges")
print(all_distanceB[best[0]][0], "         ", all_distanceB[best[1]][1], "          ", all_distanceB[best[2]][2],"         ", all_distanceB[best[3]][3])
print("Worst distances for kroB100:")
print("Steepest Vert | Greedy Vert |  Steepest Edges | Greedy Edges")
print(worst[0], "          ", worst[1], "        ", worst[2], "         ", worst[3])
print("Means distances for kroB100:")
print("Steepest Vert | Greedy Vert |  Steepest Edges | Greedy Edges")
print(mean[0], "        ", mean[1], "        ", mean[2], "     ", mean[3])
print("Best  time for korB100:")
print("Steepest Vert | Greedy Vert |  Steepest Edges | Greedy Edges")
print(round(all_timeA[bestT[0]][0], 2), "         ", round(all_timeA[bestT[1]][1],2), "           ",round(all_timeA[bestT[2]][2], 2),"          ", round(all_timeA[bestT[3]][3], 2))
print("Worst time for kroB100:")
print("Steepest Vert | Greedy Vert |  Steepest Edges | Greedy Edges")
print(round(worstT[0],2), "           ", round(worstT[1],2), "            ", round(worstT[2],2), "           ", round(worstT[3],2))
print("Means time for kroB100:")
print("Steepest Vert | Greedy Vert |  Steepest Edges | Greedy Edges")
print(round(meanT[0],2), "           ", round(meanT[1],2), "          ", round(meanT[2],2), "         ", round(meanT[3],2))

plot_result(coordsB, all_visitedB[best[0]][0], "Steepest_Vert_B.png")
plot_result(coordsB, all_visitedB[best[1]][1], "Greedy_Vert_B.png")
plot_result(coordsB, all_visitedB[best[2]][2], "Steepest_Edge_B.png")
plot_result(coordsB, all_visitedB[best[3]][3], "Greedy_Edge_B.png")