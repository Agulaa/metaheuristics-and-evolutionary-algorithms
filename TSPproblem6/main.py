import numpy as np

from functions import load_instance, get_coords, create_distances_matrix
from multiplegreedy import MultipleStartLocalSearch
import time
from visualisation import plot_statistic
import matplotlib.pyplot as plt

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
    for i in range(1000):
        print(i)
        start, not_start = start_solution(coords)
        best_distance, best_visited, best_not_visited = msls.alghorithm(matrix, start, not_start)
        all_distance.append([best_distance])
        all_visited.append(best_visited)
    all_distance = np.array(all_distance)
    all_visited = np.array(all_visited)
    np.save('Solutions/all_distance.npy', all_distance)
    np.save('Solutions/all_visited.npy', all_visited)


def statistic(all_distance, all_visited):
    best = all_distance.argmin(axis=0)


    np.save('Solutions/best_all_visited.npy', all_visited[best[0]])

    np.save('Solutions/best_distane.npy', np.array(all_distance[best[0]][0]))

    all_distance = np.delete(all_distance, best[0], axis=0)
    all_visited = np.delete(all_visited, best[0], axis=0)

    np.save('Solutions/update_all_visited.npy', all_visited)
    np.save('Solutions/update_all_distance.npy', all_distance)






def find_vert_to_best(best_distance, distance):
    return len(list(set(best_distance).intersection(distance)))

def create_edge_list(distance):
    all_edges =[]

    for i in range(len(distance)-1):
        all_edges.append(sorted([distance[i],distance[i+1]]))

    all_edges.append(sorted([distance[-1], distance[0]]))
    return np.array(all_edges)

def all_edges_list_for_all_solution(all_distance):
    all_list_edges = []

    for one_distance in all_distance:

        all_list_edges.append(create_edge_list(one_distance))
    return np.array(all_list_edges)

def find_common_egdes(all_edges1, all_edges2):
    #return len(np.intersect1d(all_edges1, all_edges2))
    count = 0
    for j in range(len(all_edges2)):
        if any((all_edges1[:]==all_edges2[j]).all(1)):
            count += 1
    return count


def best_statistic(best_distance, all_solution, all_list_edges, best_egdes):
    statistic_vert = []
    statistic_edges = []
    for solution,edges in zip(all_solution, all_list_edges):
        num_vert = find_vert_to_best(best_distance, solution)
        num_egdes = find_common_egdes(best_egdes, edges)
        statistic_vert.append(num_vert)
        statistic_edges.append(num_egdes)

    return np.array(statistic_edges), np.array(statistic_vert)


def mean_statistic(all_solution, all_list_edges):
    mean_statistic_vert = []
    mean_statistic_edges = []
    for i in range(len(all_solution)):
        statistic_vert = []
        statistic_edges = []
        for j in range(len(all_solution)):
            if i!=j:
                num_vert = find_vert_to_best(all_solution[i], all_solution[j])
                num_egdes = find_common_egdes(all_list_edges[i], all_list_edges[j])
                statistic_vert.append(num_vert)
                statistic_edges.append(num_egdes)
        statistic_vert = np.array(statistic_vert)
        statistic_edges = np.array(statistic_edges)
        mean_statistic_vert.append(statistic_vert.mean(axis=0))
        mean_statistic_edges.append(statistic_edges.mean(axis=0))
    return np.array(mean_statistic_vert), np.array(mean_statistic_edges)


def make_statistic_plot():
    all_distance = np.load('Solutions/all_distance.npy')
    all_visited = np.load('Solutions/all_visited.npy')
    statistic(all_distance,all_visited)
    all_distance = np.load('Solutions/update_all_distance.npy')
    all_visited = np.load('Solutions/update_all_visited.npy')
    best_all_visited = np.load('Solutions/best_all_visited.npy')
    best_distance = np.load('Solutions/best_distane.npy')
    all_edges = all_edges_list_for_all_solution(all_visited)

    best_egdes = create_edge_list(best_all_visited)
    statistic_edges, statistic_vert = best_statistic(best_all_visited, all_visited, all_edges, best_egdes)
    mean_statistic_vert, mean_statistic_edges = mean_statistic(all_visited, all_edges)

    plot_best_solution_edges = np.append(all_distance.reshape(-1, 1), statistic_edges.reshape(-1, 1), axis=1)
    plot_best_solution_vert =  np.append(all_distance.reshape(-1, 1), statistic_vert.reshape(-1, 1), axis=1)


    plot_mean_solution_edges = np.append(all_distance.reshape(-1, 1), mean_statistic_edges.reshape(-1, 1), axis=1)
    plot_mean_solution_vert =  np.append(all_distance.reshape(-1, 1), mean_statistic_vert.reshape(-1, 1), axis=1)


    plot_mean_solution_edges = np.array(sorted(plot_mean_solution_edges, key=lambda x: x[0]))
    plot_mean_solution_vert = np.array(sorted(plot_mean_solution_vert, key=lambda x: x[0]))
    plot_best_solution_edges = np.array(sorted(plot_best_solution_edges, key=lambda x: x[0]))
    plot_best_solution_vert = np.array(sorted(plot_best_solution_vert, key=lambda x: x[0]))

    np.save('Solutions/plot_mean_solution_edges.npy', plot_mean_solution_edges)
    np.save('Solutions/plot_mean_solution_vert.npy', plot_mean_solution_vert)
    np.save('Solutions/plot_best_solution_edges.npy', plot_best_solution_edges)
    np.save('Solutions/plot_best_solution_vert.npy', plot_best_solution_vert)

    plot_mean_solution_edges = np.load('Solutions/plot_mean_solution_edges.npy')
    plot_mean_solution_vert = np.load('Solutions/plot_mean_solution_vert.npy')
    plot_best_solution_edges = np.load('Solutions/plot_best_solution_edges.npy')
    plot_best_solution_vert = np.load('Solutions/plot_best_solution_vert.npy')


    plot_statistic(plot_best_solution_edges, "plot_best_solution_edges.png")
    plot_statistic(plot_best_solution_vert, "plot_best_solution_vert.png")
    plot_statistic(plot_mean_solution_edges, "plot_mean_solution_edges.png")
    plot_statistic(plot_mean_solution_vert, "plot_mean_solution_vert.png")



    print("plot_best_solution_edges")
    print(np.corrcoef(plot_best_solution_edges[:,0], plot_best_solution_edges[:,1]))
    print("plot_best_solution_vert")
    print(np.corrcoef(plot_best_solution_vert[:, 0], plot_best_solution_vert[:, 1]))
    print("plot_mean_solution_edges")
    print(np.corrcoef(plot_mean_solution_edges[:, 0], plot_mean_solution_edges[:, 1]))
    print("plot_mean_solution_vert")
    print(np.corrcoef(plot_mean_solution_vert[:, 0], plot_mean_solution_vert[:, 1]))



matrixA, coordsA = prepare_coords_and_matrix(pathA)
matrixB, coordsB = prepare_coords_and_matrix(pathB)
msls = MultipleStartLocalSearch()
do(matrixA,msls, coordsA)
make_statistic_plot()



do(matrixB, msls, coordsB)

make_statistic_plot()




