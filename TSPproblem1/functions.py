import numpy as np
from tsplib95 import distances, load_problem

def load_instance(path):
    """
    :param path:
    :return:
    """
    return load_problem(path)

def get_coords(problem):
    """
    :param problem:
    :return:
    """
    Graph = problem.get_graph()
    coords = []
    for k,v in Graph.nodes.items():
        coords.append(v['coord'])
    return np.array(coords)

def create_distances_matrix(coords):
    """
    :param coords:
    :return:
    """
    n = len(coords)
    matrix = []
    for coord1 in coords:
        row = []
        for coord2 in coords:
          row.append(distances.euclidean(coord1, coord2))
        matrix.append(row)
    return np.array(matrix)

def find_min(matrix, visitied, nextVert1):
    """

    :param matrix:
    :param visitied:
    :param nextVert1:
    :return:
    """
    new_row_matrix = matrix[nextVert1].copy()
    max_value = np.max(new_row_matrix)
    new_row_matrix[nextVert1] +=max_value
    for n in visitied:
        new_row_matrix[n] +=max_value
    return np.argmin(new_row_matrix)

def count_distance(matrix, visitied):
    """
    :param matrix: 
    :param visitied: 
    :return: 
    """""
    distanceSum = 0
    for i in range(len(visitied)-1):
      distanceSum+=matrix[visitied[i]][visitied[i+1]]
    distanceSum+=matrix[visitied[0]][visitied[-1]]
    return distanceSum

def cost(v1,v2,insertV, matrix):
    """

    :param v1:
    :param v2:
    :param insertV:
    :param matrix:
    :return:
    """
    return matrix[v1,insertV] + matrix[insertV,v2] - matrix[v1,v2]

