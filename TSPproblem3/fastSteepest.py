from functions import count_distance
import numpy as np
import heapq
class FastSteepest():

    def __init__(self):
        pass

    def find_better_vert(self, visited, not_visited, cost, matrix):
        min_cost = cost
        best_visited = []
        best_n_vis = []
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
        if len(best_visited)>0:
            return best_visited, best_n_vis, min_cost
        else:
            return visited, not_visited, cost

    def find_verts(self, visited, not_visited, cost, matrix, moveList):
        for idx, vert in enumerate(visited):
            for idx2, vert2 in enumerate(not_visited):
                vis_copy = visited.copy()
                vis_copy[idx] = vert2
                new_cost = count_distance(matrix, vis_copy)
                if new_cost < cost:
                    moveList.append([new_cost, [vert, vert2]])
        return moveList

    def find_verts_for_new(self, visited, not_visited, cost, matrix, moveList, idx, vert):
        for idx2, vert2 in enumerate(not_visited):
            vis_copy = visited.copy()
            vis_copy[idx] = vert2
            new_cost = count_distance(matrix, vis_copy)
            if new_cost < cost:
                moveList.append([new_cost, [vert, vert2]])
        return moveList

    def check_vert_move(self, visited, not_visited, vert1, vert2):
        try:
            idx1 = np.where(visited == vert1)[0][0]
        except:
            idx1 = None
        try:
            idx2 = np.where(visited == vert2)[0][0]
        except:
            idx2 = None
        if idx1 == None and idx2 == None:
            return False, None, None
        elif idx1 != None and idx2 != None:
            return False, None, None
        elif idx1 == None and idx2 != None:
            idx1 = np.where(not_visited == vert1)[0][0]
            return True, [vert2,idx2], [vert1,idx1]
        elif idx1 != None and idx2 == None:
            idx2 = np.where(not_visited == vert2)[0][0]
            return True, [vert1,idx1], [vert2,idx2]

    def change_verts(self, visited, not_visited, vert1, idx1, vert2, idx2):
        best_visited = visited.copy()
        best_not_visited = not_visited.copy()

        best_visited[idx1] = vert2

        best_not_visited[idx2] = vert1

        return best_visited, best_not_visited

    def find_edges(self, visited, cost, matrix, moveList):
        cycle = np.append(visited, visited[0])

        for i in range(0, len(visited) - 2):
            for j in range(i + 3, len(visited) - 1):
                cycle_copy = cycle.copy()
                cycle_copy1 = cycle.copy()
                chunk = cycle[i + 1:j + 1]
                chunk = chunk[::-1]
                cycle_copy[i + 1:j + 1] = chunk

                cost_now = count_distance(matrix, cycle_copy[:-1])
                if cost_now < cost:
                    moveList.append([cost_now, [cycle_copy1[i], cycle_copy1[i + 1], cycle_copy1[j], cycle_copy1[j + 1]]])
        return moveList

    def find_edges_for_vert(self, visited, cost, matrix, moveList, idx_in):
        cycle = np.append(visited, visited[0])
        if idx_in == 0:
            tab = [len(visited)-1, idx_in]
        else:
            tab = [idx_in-1, idx_in]
        for idx in tab:
            for idx2, vert2 in enumerate(visited):
                if idx2 in [idx-1, idx, idx+1]:
                    pass
                elif abs((idx2 + 1) - idx) == 1 or abs(idx2 - (idx+1)) == 1:
                    pass
                elif abs(idx2 - (idx +1)) >= len(visited)-1:
                    pass
                elif abs(idx2+ 1 - idx) >= len(visited)-1:
                    pass
                else:
                    if idx2 < idx:
                        cycle_copy = cycle.copy()
                        cycle_copy1 = cycle.copy()
                        chunk = cycle[idx2 + 1:idx + 1]
                        chunk = chunk[::-1]
                        cycle_copy[idx2 + 1:idx + 1] = chunk
                    else:
                        cycle_copy = cycle.copy()
                        cycle_copy1 = cycle.copy()
                        chunk = cycle[idx + 1:idx2 + 1]
                        chunk = chunk[::-1]
                        cycle_copy[idx + 1:idx2 + 1] = chunk

                    cost_now = count_distance(matrix, cycle_copy[:-1])
                    if cost_now < cost:
                        if idx2 < idx:
                            moveList.append([cost_now,[cycle_copy1[idx2],cycle_copy1[idx2+1],cycle_copy1[idx],cycle_copy1[idx+1]]])
                        elif idx2 > idx:
                            moveList.append(
                                [cost_now, [cycle_copy1[idx], cycle_copy1[idx + 1], cycle_copy1[idx2], cycle_copy1[idx2 + 1]]])
        return moveList

    def find_edges_for_edge(self, visited, cost, matrix, moveList, idx_in1, idx_in2):
        cycle = np.append(visited, visited[0])
        tab = [idx_in1, idx_in2]
        for idx in tab:
            # print(idx, idx+1)
            for idx2, vert2 in enumerate(visited):
                if idx2 in [idx - 1, idx, idx + 1]:
                    pass
                elif abs((idx2 + 1) - idx) == 1 or abs(idx2 - (idx + 1)) == 1:
                    pass
                elif abs(idx2 - (idx + 1)) >= len(visited) - 1:
                    pass
                elif abs(idx2 + 1 - idx) >= len(visited) - 1:
                    pass
                else:
                    # print(idx2, idx2+1)
                    if idx2 < idx:
                        cycle_copy = cycle.copy()
                        cycle_copy1 = cycle.copy()
                        chunk = cycle[idx2 + 1:idx + 1]
                        chunk = chunk[::-1]
                        cycle_copy[idx2 + 1:idx + 1] = chunk
                    else:
                        cycle_copy = cycle.copy()
                        cycle_copy1 = cycle.copy()
                        chunk = cycle[idx + 1:idx2 + 1]
                        chunk = chunk[::-1]
                        cycle_copy[idx + 1:idx2 + 1] = chunk

                    cost_now = count_distance(matrix, cycle_copy[:-1])
                    if cost_now < cost:
                        if idx2 < idx:
                            moveList.append([cost_now, [cycle_copy1[idx2], cycle_copy1[idx2 + 1], cycle_copy1[idx],
                                                        cycle_copy1[idx + 1]]])
                        elif idx2 > idx:
                            moveList.append([
                                cost_now,
                                 [cycle_copy1[idx], cycle_copy1[idx + 1], cycle_copy1[idx2], cycle_copy1[idx2 + 1]]])
        return moveList
    def check_edges(self, visited, vert1, vert2, vert3, vert4):
        try:
            idx1 = np.where(visited == vert1)[0][0]
            idx2 = np.where(visited == vert2)[0][0]
            idx3 = np.where(visited == vert3)[0][0]
            idx4 = np.where(visited == vert4)[0][0]
            if abs(idx1 - idx2) == 1 and abs(idx3- idx4) == 1:
                if abs(idx3 - idx2) == 1:
                    return False, None, None, None, None
                elif abs(idx4 - idx1) == len(visited)-1:
                    return False, None, None, None, None
                else:
                    list_of_index = [idx1,idx2,idx3,idx4]
                    list_of_index = sorted(list_of_index)
                    return True, list_of_index[0], list_of_index[1],list_of_index[2],list_of_index[3]

            else:
                return False, None, None, None, None
        except:
            return False, None, None, None, None

    def change_2_edges(self, visited, idx1, idx2, idx3, idx4):
        cycle = np.append(visited, visited[0])
        cycle_copy = cycle.copy()
        chunk = cycle[idx2:idx4]
        chunk = chunk[::-1]
        cycle_copy[idx2:idx4] = chunk
        best_visited = cycle_copy[:-1]
        return best_visited

    def first_move(self, visited, not_visited, cost, matrix, moveList):
        moveList = self.find_verts(visited, not_visited, cost, matrix, moveList)
        moveList = self.find_edges(visited, cost, matrix, moveList)
        moveList = sorted(moveList, key=lambda x: x[0])
        if len(moveList[0][1]) == 2:
            vert1, vert2 = moveList[0][1]
            idx1 = np.where(visited == vert1)[0][0]
            idx2 = np.where(not_visited == vert2)[0][0]
            best_visited, best_not_visited = self.change_verts(visited, not_visited, vert1, idx1, vert2, idx2)
            return best_visited, best_not_visited, moveList[0][0], moveList[1:]
        else:
            vert1, vert2, vert3, vert4 = moveList[0][1]
            idx1 = np.where(visited == vert1)[0][0]
            idx2 = np.where(visited == vert2)[0][0]
            idx3 = np.where(visited == vert3)[0][0]
            idx4 = np.where(visited == vert4)[0][0]
            best_visited = self.change_2_edges(visited, idx1, idx2, idx3, idx4)
            return best_visited, not_visited, moveList[0][0], moveList[1:]

    def find_new_moves(self, visited, best_visited,not_visited,  cost, matrix, moveList):
        diff = visited - best_visited
        if sum((diff != 0).astype(int)) == 1:
            idx = np.where((diff != 0).astype(int) != 0)[0][0]

            moveList = self.find_verts_for_new(best_visited, not_visited, cost, matrix, moveList, idx, best_visited[idx])
            moveList = self.find_edges_for_vert(best_visited, cost, matrix, moveList, idx)
        else:
            first_idx = np.where(diff != 0)[0][0]
            last_idx = np.where(diff != 0)[0][-1]
            moveList = self.find_edges_for_edge(best_visited, cost, matrix, moveList, first_idx - 1, last_idx)
        return sorted(moveList, key=lambda x: x[0])

    def find_candidates(self, visited, vert, matrix):
        row = matrix[visited[vert]][visited].copy()
        # row = row[visited]
        idx = np.array(heapq.nsmallest(8, range(len(row)), row.take))

        idx = idx[1:]
        if visited[vert - 1] in idx:
            idx = np.delete(idx, np.where(idx == visited[vert - 1]))
        if vert + 1 == len(visited) and visited[0] in idx:
            idx = np.delete(idx, np.where(idx == visited[0]))
        if vert + 1 != len(visited) and visited[vert + 1] in idx:
            idx = np.delete(idx, np.where(idx == visited[vert + 1]))
        return visited[idx[:5]]

    def change_2_edges_candidates(self, visited, cost, matrix):
        min_cost = cost
        best_visited = []
        cycle = np.append(visited, visited[0])

        for i in range(0, len(visited)):
            candidates = self.find_candidates(visited, i, matrix)
            for j in range(0, len(candidates)):
                idx = np.where(visited == candidates[j])[0][0]
                cycle_copy = cycle.copy()
                chunk = cycle[i + 1:idx + 1]
                chunk = chunk[::-1]
                cycle_copy[i + 1:idx + 1] = chunk

                cost_now = count_distance(matrix, cycle_copy[:-1])
                if cost_now < min_cost:
                    min_cost = cost_now
                    best_visited = cycle_copy[:-1]
        if len(best_visited) > 0:
            return best_visited, min_cost
        else:
            return visited, cost

    def alghorithm1(self, matrix, start, not_start):
        visited = start
        not_visited = not_start
        cost = count_distance(matrix, start)
        found_better = True
        while found_better:
            best_visited1, best_not_visited, min_cost1 = self.find_better_vert(visited, not_visited, cost, matrix)
            best_visited2, min_cost2 = self.change_2_edges_candidates(visited, cost, matrix)
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
        moveList = []  # [cost,[v1,v2]] or [cost,[v1,v2,v3,v4]]
        new_visited, new_not_visited, cost, moveList = self.first_move(visited, not_visited, cost, matrix, moveList)
        found_better = True
        while found_better:
            found_better = False
            moveList = self.find_new_moves(visited, new_visited, new_not_visited, cost, matrix, moveList)
            idx_to_del = []
            for move_idx, move in enumerate(moveList):
                if len(move[1]) == 2:
                    vert1, vert2 = move[1]
                    check, vertList1, vertList2 = self.check_vert_move(new_visited, new_not_visited, vert1, vert2)
                    if check == True:
                        best_visited, best_new_not_visited = self.change_verts(new_visited, new_not_visited, vertList1[0], vertList1[1], vertList2[0], vertList2[1])
                        new_cost = count_distance(matrix, best_visited)
                        if new_cost<cost:
                            idx_to_del.append(move_idx)
                            cost = new_cost
                            visited = new_visited
                            new_visited = best_visited
                            new_not_visited = best_new_not_visited
                            found_better = True
                            break
                    idx_to_del.append(move_idx)
                else:
                    vert1, vert2, vert3, vert4 = move[1]
                    check, idx1, idx2, idx3, idx4 = self.check_edges(new_visited, vert1, vert2, vert3, vert4)
                    if check == True:
                        best_visited = self.change_2_edges(new_visited, idx1, idx2, idx3, idx4)
                        new_cost = count_distance(matrix, best_visited)
                        if new_cost < cost:
                            idx_to_del.append(move_idx)
                            cost = new_cost
                            visited = new_visited
                            new_visited = best_visited
                            found_better = True
                            break
                    idx_to_del.append(move_idx)
            idx_to_del.reverse()
            for idx in idx_to_del:
                del (moveList[idx])

        cost = count_distance(matrix, new_visited)
        return cost, new_visited