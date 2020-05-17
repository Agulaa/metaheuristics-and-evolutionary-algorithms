import random
from functions import count_distance
import numpy as np
import time
from multiplegreedy import MultipleStartLocalSearch
from greedy_cycle import GreedCycle

class IteratedLocalSearchGreedy():

    def __init__(self, mean_time_msls):
        self.msls = MultipleStartLocalSearch()
        self.greedy = GreedCycle()
        self.mean_time_msls = mean_time_msls

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



    def make_small_perturbation_verts(self, visited, not_visited):
        new_visited = visited.copy()
        new_not_visited = not_visited.copy()
        #randomowo wymiara kilku wierzchołków
        for i in range(random.randint(2,5)):
            idx = random.randint(0, len(visited)-1)
            idx2 = random.randint(0, len(not_visited)-1)
            new_visited[idx] = not_visited[idx2]
            new_not_visited[idx2] = visited[idx]
        return new_visited, new_not_visited

    def destroy(self, matrix, best_visited, best_not_visited):
        # print(type(best_not_visited))
        # print(type(best_visited))
        destroy_visited = np.array(best_visited).copy()
        destroy_not_visited = best_not_visited.copy()
        idx = list(range(len(destroy_visited)))
        to_del = np.random.choice(idx, 30, replace=False)
        # verts_to_del = destroy_visited[to_del]
        distances = []
        for i in to_del:
            if i > 0 and i < 99:
                distances.append([i, matrix[destroy_visited[i - 1], destroy_visited[i]] + matrix[
                    destroy_visited[i + 1], destroy_visited[i]]])
            elif i == 0:
                distances.append([i, matrix[destroy_visited[len(destroy_visited) - 1], destroy_visited[i]] + matrix[
                    destroy_visited[i + 1], destroy_visited[i]]])
            elif i == 99:
                distances.append([i, matrix[destroy_visited[i - 1], destroy_visited[i]] + matrix[
                    destroy_visited[0], destroy_visited[i]]])

        distances = np.array(sorted(distances, key=lambda x: x[1], reverse=True))
        # print("NOT VISITED: ")
        # print(destroy_not_visited)
        delete = distances[:20, 0]
        # print("DELETE: ")
        # print(delete)
        # print("VISITED: ")
        # print(destroy_visited)
        # print("VISITED TO DEL: ")
        # print(destroy_visited[delete])
        destroy_not_visited = np.concatenate((destroy_not_visited, destroy_visited[delete]))
        destroy_visited = np.delete(destroy_visited, delete, axis=None)

        return destroy_visited, destroy_not_visited

    def alghorithm1(self, matrix, start, not_start):
        visited = start
        not_visited = not_start
        cost, best_visited, best_not_visited = self.msls.alghorithm(matrix, visited, not_visited)
        time_start = time.time()
        time1=0
        i=1
        while time1<=self.mean_time_msls:
            new_visited, new_not_visited = self.make_small_perturbation_verts(visited, not_visited)
            new_cost, new_best_visited, new_best_not_visited = self.msls.alghorithm(matrix, new_visited, new_not_visited)
            if new_cost<cost:
                visited = new_best_visited
                not_visited = new_best_not_visited
                cost = new_cost
            i+=1
            time1 = time.time() - time_start
        print("Num of iters:",i)
        return cost, visited, not_visited
    def alghorithm2(self, matrix, start, not_start):
        visited = start
        not_visited = not_start
        cost, best_visited, best_not_visited = self.msls.alghorithm(matrix, visited, not_visited)
        time_start = time.time()
        time1=0
        counter = 0
        while time1<=self.mean_time_msls:
            counter += 1
            #destroy
            new_visited, new_not_visited = self.destroy(matrix, best_visited, best_not_visited)
            #repair
            _ , new_visited = self.greedy.alghorithm(matrix, new_visited)
            new_not_visited = np.array(list(set(range(len(matrix))) - set(new_visited)))

            new_cost, new_best_visited, new_best_not_visited = self.msls.alghorithm(matrix, new_visited, new_not_visited)
            if new_cost<cost:
                best_visited = new_best_visited
                best_not_visited = new_best_not_visited
                cost = new_cost
            time1 = time.time() - time_start
        print("While times: ")
        print(counter)
        return cost, best_visited, best_not_visited