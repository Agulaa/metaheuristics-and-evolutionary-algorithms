import random
from functions import count_distance
import numpy as np
import time
from multiplegreedy import MultipleStartLocalSearch
from greedy_cycle import GreedCycle

class EvolutionHybrid():

    def __init__(self, coords, mean_time_msls, matrix, size = 100, population_size = 20):
        self.msls = MultipleStartLocalSearch()
        self.population = []
        self.coords = coords
        self.mean_time_msls = mean_time_msls
        self.size = size
        self.population_size = population_size
        self.population_costs = []
        self.matrix = matrix

    def start_solution(self):
        idxes = np.arange(len(self.coords))
        visited = np.random.choice(idxes, self.size, replace=False)
        return visited

    def init_random_population(self):
        i = 0
        while i < self.population_size:
            visited = list(self.start_solution())
            if visited not in self.population:
                self.population.append(visited)
                self.population_costs.append(count_distance(self.matrix, visited))
                i += 1

    def init_greedy_population(self):
        i = 0
        num = int(self.matrix.shape[0])
        greedy = GreedCycle()
        while i < self.population_size:
            start = random.randint(0, num - 1)
            cost, visited = greedy.algorithm(self.matrix, start)
            visited = list(visited)
            if visited not in self.population:
                self.population.append(visited)
                self.population_costs.append(cost)
                i += 1


    def cross(self, solution1, solution2):
        new_visited = list(set(solution1).intersection(solution2))
        parent1 = list(set(solution1).difference(set(new_visited)))
        parent2 = list(set(solution2).difference(set(new_visited)))
        parent1.extend(parent2)
        parents = parent1.copy()
        while len(new_visited) < self.size:
            idx = random.randint(0, len(parents)-1)
            new_visited.append(parents[idx])
            del(parents[idx])
        return new_visited

    def cross2(self, solution1, solution2, cost1, cost2):
        common = list(set(solution1).intersection(solution2))
        parent1 = list(set(solution1).difference(set(common)))
        parent2 = list(set(solution2).difference(set(common)))
        parent1.extend(parent2)
        parents = parent1.copy()
        new_visited = []
        if cost1< cost2:
            for vert in solution1:
                if vert in common:
                    new_visited.append(vert)
                else:
                    idx = random.randint(0, len(parents)-1)
                    new_visited.append(parents[idx])
                    del(parents[idx])
        else:
            for vert in solution2:
                if vert in common:
                    new_visited.append(vert)
                else:
                    idx = random.randint(0, len(parents)-1)
                    new_visited.append(parents[idx])
                    del(parents[idx])
        return new_visited

    def cross3(self, solution1, solution2):
        new_visited = list(set(solution1).intersection(solution2))
        parent1 = list(set(solution1).difference(set(new_visited)))
        parent2 = list(set(solution2).difference(set(new_visited)))
        parent1.extend(parent2)
        parents = parent1.copy()
        while len(new_visited) < self.size:
            idx = random.randint(0, len(parents)-1)
            new_visited.append(parents[idx])
            del(parents[idx])
        random.shuffle(new_visited)
        return new_visited

    def cross4(self, solution1, solution2, cost1, cost2):
        common = list(set(solution1).intersection(solution2))
        # parent1 = list(set(solution1).difference(set(common)))
        # parent2 = list(set(solution2).difference(set(common)))
        # parent1.extend(parent2)
        # parents = parent1.copy()
        new_visited = []
        if cost1< cost2:
            for idx in range(len(solution1)):
                if solution1[idx] in common:
                    new_visited.append(solution1[idx])
                else:
                    choice = random.randint(0, 1)
                    if choice == 0 and solution2[idx] not in common:
                        new_visited.append(solution2[idx])
                    else:
                        new_visited.append(solution1[idx])
        else:
            for idx in range(len(solution2)):
                if solution2[idx] in common:
                    new_visited.append(solution2[idx])
                else:
                    choice = random.randint(0, 1)
                    if choice == 0 and solution1[idx] not in common:
                        new_visited.append(solution1[idx])
                    else:
                        new_visited.append(solution2[idx])
        return new_visited

    def algorithm(self):
        self.init_greedy_population()
        print("POPULATION OK")
        time_start = time.time()
        time1=0
        counter = 0
        while time1<=self.mean_time_msls:
            counter += 1

            idx1 = random.randint(0, self.population_size-1)
            idx2 = random.randint(0, self.population_size-1)
            while idx1 == idx2:
                idx2 = random.randint(0, self.population_size-1)

            new_visited = self.cross4(self.population[idx1], self.population[idx2], self.population_costs[idx1], self.population_costs[idx2])
            #new_visited = self.cross3(self.population[idx1], self.population[idx2])
            new_not_visited = np.array(list(set(range(len(self.matrix))) - set(new_visited)))

            new_cost, new_best_visited, _ = self.msls.alghorithm(self.matrix, new_visited, new_not_visited)
            new_best_visited = list(new_best_visited)
            max_cost = max(self.population_costs)
            if (new_cost < max_cost) and (new_best_visited not in self.population):
                # print("ADDED NEW SOL TO POP ", new_cost)
                max_idx = self.population_costs.index(max_cost)
                del(self.population[max_idx])
                del(self.population_costs[max_idx])
                self.population.append(new_best_visited)
                self.population_costs.append(new_cost)

            time1 = time.time() - time_start

        min_idx = self.population_costs.index(min(self.population_costs))
        cost = self.population_costs[min_idx]
        best_visited = self.population[min_idx]
        best_not_visited = np.array(list(set(range(len(self.matrix))) - set(best_visited)))

        print("While times: ")
        print(counter)
        print("Score: ")
        print(cost)
        print("_____________________________________")
        return cost, best_visited, best_not_visited