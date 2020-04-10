import random
from functions import count_distance
import numpy as np
class Greedy():

    def __init__(self):
        pass

    def find_better_vert(self, visited, not_visited, cost, matrix):
        min_cost = cost
        for idx, vert in enumerate(visited):
            for idx2, vert2 in enumerate(not_visited):
                vis_copy = visited.copy()
                vis_copy[idx] = vert2
                new_cost = count_distance(matrix, vis_copy)
                if new_cost < min_cost:
                    min_cost = new_cost
                    best_visited = vis_copy
                    best_n_vis = not_visited.copy()
                    best_n_vis[idx2] = vert
                    return best_visited, best_n_vis, min_cost
        return visited, not_visited, cost

    def change_2_verts(self, visited, cost, matrix):
        min_cost = cost
        for idx in range(len(visited)):
            for idx2 in range(idx + 1, len(visited)):
                vis_copy = visited.copy()
                vis_copy[idx] = vis_copy[idx2]
                vis_copy[idx2] = visited[idx]
                new_cost = count_distance(matrix, vis_copy)
                if new_cost < min_cost:
                    min_cost = new_cost
                    best_visited = vis_copy
                    return best_visited, min_cost
        return visited, cost

    def change_2_edges(self, visited, cost, matrix):
        min_cost = cost
        cycle = np.append(visited, visited[0])
        for i in range(0, len(visited) - 2):
            for j in range(i + 3, len(visited) - 1):
                cycle_copy = cycle.copy()
                if i == 0 and len(cycle) - 3 > j:
                    chunk = cycle[i + 1:j + 1]
                    chunk = chunk[::-1]
                    cycle_copy[i + 1:j + 1] = chunk
                elif i == 1 and len(cycle) - 2 > j:
                    chunk = cycle[i + 1:j + 1]
                    chunk = chunk[::-1]
                    cycle_copy[i + 1:j + 1] = chunk
                elif i != 0 and i != 1:
                    chunk = cycle[i + 1:j + 1]
                    chunk = chunk[::-1]
                    cycle_copy[i + 1:j + 1] = chunk

                cost_now = count_distance(matrix, cycle_copy[:-1])
                if cost_now < min_cost:
                    min_cost = cost_now
                    best_visited = cycle_copy[:-1]
                    return best_visited, min_cost
        return visited, cost

    def alghorithm1(self, matrix, start, not_start):
        visited = start
        not_visited = not_start
        cost = count_distance(matrix, start)
        found_better = True
        while found_better:
            idx = random.randint(0, len(visited))
            random_visited = list(visited[idx:])+list( visited[:idx])
            best_visited1, best_not_visited, min_cost1 = self.find_better_vert(random_visited, not_visited, cost,
                                                                               matrix)
            idx = random.randint(0, len(visited))
            random_visited = list(visited[idx:]) + list(visited[:idx])
            best_visited2, min_cost2 = self.change_2_verts(random_visited, cost, matrix)
            if min_cost1 < cost and min_cost2 < cost:
                if min_cost1 < min_cost2:
                    cost = min_cost1
                    visited = best_visited1
                    not_visited = best_not_visited
                else:
                    cost = min_cost2
                    visited = best_visited2
            elif min_cost1 < cost:
                cost = min_cost1
                visited = best_visited1
                not_visited = best_not_visited
            elif min_cost2 < cost:
                cost = min_cost2
                visited = best_visited2
            else:
                found_better = False
        return cost, visited

    def alghorithm2(self, matrix, start, not_start):
        visited = start
        not_visited = not_start
        cost = count_distance(matrix, start)
        found_better = True
        while found_better:
            idx = random.randint(0, len(visited))
            random_visited = list(visited[idx:]) + list(visited[:idx])
            best_visited1, best_not_visited, min_cost1 = self.find_better_vert(random_visited, not_visited, cost,
                                                                               matrix)
            idx = random.randint(0, len(visited))
            random_visited = list(visited[idx:]) + list(visited[:idx])
            best_visited2, min_cost2 = self.change_2_edges(random_visited, cost, matrix)
            if min_cost1 < cost and min_cost2 < cost:
                if min_cost1 < min_cost2:
                    cost = min_cost1
                    visited = best_visited1
                    not_visited = best_not_visited
                else:
                    cost = min_cost2
                    visited = best_visited2
            elif min_cost1 < cost:
                cost = min_cost1
                visited = best_visited1
                not_visited = best_not_visited
            elif min_cost2 < cost:
                cost = min_cost2
                visited = best_visited2
            else:
                found_better = False
        return cost, visited