import numpy as np
from functions import find_min, cost, count_distance


class Regret():

    def __init__(self):
        pass


    def find_best_vert(self, matrix, visited):
        lowest_cost_for_edges = {}
        best_vert_for_edges = {}
        to_check = list(set(range(len(matrix))) - set(visited))
        for j in range(len(visited) - 1):
            new_vert_cost = {}
            for v in to_check:
                new_vert_cost[v] = cost(visited[j], visited[j + 1], v, matrix)
            min_cost_key = int(min(new_vert_cost, key=new_vert_cost.get))
            lowest_cost_for_edges[(j, j + 1)] = new_vert_cost[min_cost_key]
            best_vert_for_edges[(j, j + 1)] = min_cost_key
        new_vert_cost = {}
        for v in to_check:
            new_vert_cost[v] = cost(visited[-1], visited[0], v, matrix)
        min_cost_key = int(min(new_vert_cost, key=new_vert_cost.get))
        lowest_cost_for_edges[(len(visited) - 1, 0)] = new_vert_cost[min_cost_key]
        best_vert_for_edges[(len(visited) - 1, 0)] = min_cost_key
        best_key = min(lowest_cost_for_edges, key=lowest_cost_for_edges.get)
        del (lowest_cost_for_edges[best_key])
        best_key2 = min(lowest_cost_for_edges, key=lowest_cost_for_edges.get)
        return best_key, best_key2, best_vert_for_edges

    def alghorithm(self, matrix, start):
        vertNo = int(matrix.shape[0] / 2)
        #start = random.randint(0, vertNo * 2 - 1)
        visited = []
        visited.append(start)
        next_min = find_min(matrix, visited, start)
        visited.append(next_min)
        for _ in range(0, vertNo - 2):
            temp_visited = visited.copy()
            temp_visited2 = visited.copy()
            best_key, best_key2, best_vert_for_edges = self.find_best_vert(matrix, visited)
            temp_visited = np.insert(np.array(temp_visited), best_key[1], best_vert_for_edges[best_key])
            temp_visited = np.insert(np.array(temp_visited), best_key2[1], best_vert_for_edges[best_key2])
            cost1 = count_distance(matrix, temp_visited)
            temp_visited2 = np.insert(np.array(temp_visited2), best_key2[1], best_vert_for_edges[best_key2])
            temp_visited2 = np.insert(np.array(temp_visited2), best_key[1], best_vert_for_edges[best_key])
            cost2 = count_distance(matrix, temp_visited2)
            if cost1 < cost2:
                visited = np.insert(np.array(visited), best_key[1], best_vert_for_edges[best_key])
            else:
                visited = np.insert(np.array(visited), best_key2[1], best_vert_for_edges[best_key2])
        distanceSum = count_distance(matrix, visited)
        return distanceSum, visited
