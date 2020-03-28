from functions import find_min
import random

class NearesNeighbor():

    def __init__(self):
        pass


    def alghorithm(self, matrix, start):

        vertNo = int(matrix.shape[0] / 2)
        #start = random.randint(0, vertNo * 2 - 1)
        visited = []
        visited.append(start)
        nextVert1 = start
        distanceSum = 0
        for i in range(0, vertNo - 1):
            nextVert = find_min(matrix,  visited, nextVert1)
            visited.append(nextVert)
            distanceSum += matrix[nextVert1][nextVert]
            nextVert1 = nextVert
        distanceSum += matrix[ visited[0]][ visited[-1]]
        return distanceSum, visited
