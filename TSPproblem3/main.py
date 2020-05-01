import numpy as np
from functions import load_instance, get_coords, create_distances_matrix
from steepest import Steepest
from fastSteepest import FastSteepest
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
def do(matrix, steep, fastSteep, coords):

    all_visited = []
    all_distance = []
    all_time = []
    for n in range(100):

        start, not_start = start_solution(coords)
        time1 = time.time()
        distanceSum_steep1, visited_steep1 = steep.alghorithm(matrix, start, not_start) #verts
        resultSteep1 =  time.time() - time1
        time1 = time.time()
        distanceSum_steep2, visited_steep2 = fastSteep.alghorithm1(matrix,  start, not_start) # edges
        resultSteep2 = time.time() - time1
        time1 = time.time()
        distanceSum_steep22, visited_steep22 = fastSteep.alghorithm2(matrix, start, not_start)  # edges
        resultSteep22 = time.time() - time1
        all_time.append([resultSteep1, resultSteep2, resultSteep22 ])
        all_distance.append([distanceSum_steep1, distanceSum_steep2,distanceSum_steep22])
        all_visited.append([visited_steep1,visited_steep2,visited_steep2])
    return np.array(all_distance), np.array(all_visited), np.array(all_time)

def statistic(all_distance):
    best = all_distance.argmin(axis=0)
    mean = all_distance.mean(axis=0)
    worst = all_distance.max(axis=0)
    return best, worst, mean


matrixA, coordsA = prepare_coords_and_matrix(pathA)
matrixB, coordsB = prepare_coords_and_matrix(pathB)
steep = Steepest()
fastSteep = FastSteepest()




all_distanceA, all_visitedA, all_timeA = do(matrixA, steep, fastSteep, coordsA)
all_distanceB, all_visitedB, all_timeB = do(matrixB, steep, fastSteep, coordsB)
best, worst, mean = statistic(all_distanceA)
bestT, worstT, meanT  = statistic(all_timeA)
print("Best  distances for korA200:")
print("Steepest Edges | Steepest Edges with candidates  | Steepest Edges with List ")
print(all_distanceA[best[0]][0], "         ", all_distanceA[best[1]][1], "           ", all_distanceA[best[2]][2])
print("Worst distances for kro2100:")
print("Steepest Edges | Steepest Edges with candidates  | Steepest Edges with List ")
print(worst[0], "           ", worst[1], "            ", worst[2])
print("Means distances for kroA200:")
print("Steepest Edges | Steepest Edges with candidates  | Steepest Edges with List ")
print(mean[0], "          ", mean[1], "        ", mean[2])
print("Best  time for korA200:")
print("Steepest Edges | Steepest Edges with candidates  | Steepest Edges with List ")
print(round(all_timeA[bestT[0]][0], 2), "         ", round(all_timeA[bestT[1]][1], 2), "           ", round(all_timeA[bestT[2]][2],2))
print("Worst time for kroA200:")
print("Steepest Edges | Steepest Edges with candidates  | Steepest Edges with List ")
print(round(worstT[0],2), "           ", round(worstT[1],2), "            ", round(worstT[2],2))
print("Means time for kroA200:")
print("Steepest Edges | Steepest Edges with candidates  | Steepest Edges with List ")
print(round(meanT[0],2), "        ", round(meanT[1],2), "          ", round(meanT[2],2))


plot_result(coordsA, all_visitedA[best[0]][0], "Steepest_EdgesA.png")
plot_result(coordsA, all_visitedA[best[1]][1], "Steepest_Edges_with_candidatesA.png")
plot_result(coordsA, all_visitedA[best[2]][2],"Steepest_Edges_List_A.png")




best, worst, mean = statistic(all_distanceB)
bestT, worstT, meanT  = statistic(all_timeB)

print("--------------------------------------------------------------------------")
print("Best  distances for korB200:")
print("Steepest Edges | Steepest Edges with candidates  | Steepest Edges with List ")
print(all_distanceB[best[0]][0], "         ", all_distanceB[best[1]][1], "          ", all_distanceB[best[2]][2])
print("Worst distances for kroB200:")
print("Steepest Edges | Steepest Edges with candidates  | Steepest Edges with List ")
print(worst[0], "          ", worst[1], "        ", worst[2])
print("Means distances for kroB200:")
print("Steepest Edges | Steepest Edges with candidates  | Steepest Edges with List ")
print(mean[0], "        ", mean[1], "        ", mean[2])
print("Best  time for korB200:")
print("Steepest Edges | Steepest Edges with candidates  | Steepest Edges with List ")
print(round(all_timeA[bestT[0]][0], 2), "         ", round(all_timeA[bestT[1]][1],2), "           ",round(all_timeA[bestT[2]][2], 2))
print("Worst time for kroB200:")
print("Steepest Edges | Steepest Edges with candidates  | Steepest Edges with List ")
print(round(worstT[0],2), "           ", round(worstT[1],2), "            ", round(worstT[2],2))
print("Means time for kroB200:")
print("Steepest Edges | Steepest Edges with candidates  | Steepest Edges with List ")
print(round(meanT[0],2), "           ", round(meanT[1],2), "          ", round(meanT[2],2))

plot_result(coordsB, all_visitedB[best[0]][0], "Steepest_EdgesB.png")
plot_result(coordsB, all_visitedB[best[1]][1], "Steepest_Edges_with_candidatesB.png")
plot_result(coordsB, all_visitedA[best[2]][2],"Steepest_Edges_List_B.png")