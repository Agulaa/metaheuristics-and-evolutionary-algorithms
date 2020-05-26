from functions import find_min, cost, count_distance
import random
import numpy as np

class GreedCycle():

    def __init__(self):
        pass

    def algorithm(self, matrix, start):
        vertNo = int(matrix.shape[0] / 2)
        #start = random.randint(0, vertNo * 2 - 1)
        visited = []
        visited.append(start)
        next_min = find_min(matrix, visited, start)
        visited.append(next_min)

        # for 48 verts
        for _ in range(0, vertNo - 2):
            lowest_cost_for_edges = {}
            best_vert_for_edges = {}
            to_check = list(set(range(len(matrix))) - set(visited)) # all vert not visited
            # for all edges check distances to all free verts and get min cost
            for j in range(len(visited) - 1):
                new_vert_cost = {}
                for v in to_check:  # check all not visited vert
                    new_vert_cost[v] = cost(visited[j], visited[j + 1], v, matrix) # method cost calculate distance between new vert and egdes from visited [j] &[j+1]
                min_cost_key = int(min(new_vert_cost, key=new_vert_cost.get)) #  minimum distance
                lowest_cost_for_edges[(j, j + 1)] = new_vert_cost[min_cost_key] # minimum distance for all edges
                best_vert_for_edges[(j, j + 1)] = min_cost_key # vert
            # final edge cost (last in list and first)
            new_vert_cost = {}
            for v in to_check:
                new_vert_cost[v] = cost(visited[-1], visited[0], v, matrix) # check last and first vert(one edges) from visited
            min_cost_key = int(min(new_vert_cost, key=new_vert_cost.get))
            lowest_cost_for_edges[(len(visited) - 1, 0)] = new_vert_cost[min_cost_key]
            best_vert_for_edges[(len(visited) - 1, 0)] = min_cost_key
            # get best vert to add
            best_key = min(lowest_cost_for_edges, key=lowest_cost_for_edges.get)
            # add it to solution
            visited = np.insert(np.array(visited), best_key[1], best_vert_for_edges[best_key])
        distanceSum = count_distance(matrix, visited)
        return distanceSum, visited