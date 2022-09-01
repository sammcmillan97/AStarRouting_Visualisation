import heapq

from Search import *
import math

class RoutingGraph(Graph):
    def __init__(self, map_str):
        self.map = self.getMap(map_str)
        self.teleport_spots = self.find_on_map(["P"])
        self.goal_spots = self.find_on_map(["G"])
        self.movement = [('N', -1, 0), ('E', 0, 1), ('S', 1, 0), ('W', 0, -1), ]

    def starting_nodes(self):
        drivers = self.find_on_map(["S", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
        starting_nodes = []
        for driver in drivers:
            if self.map[driver[0]][driver[1]].isnumeric():
                starting_nodes.append((driver[0], driver[1], int(self.map[driver[0]][driver[1]])))
            else:
                starting_nodes.append((driver[0], driver[1], math.inf))
        return starting_nodes

    def is_goal(self, node):
        return ((node[0], node[1]) in self.goal_spots)

    def outgoing_arcs(self, tail):
        arcs = []
        row = tail[0]
        col = tail[1]
        fuel = tail[2]

        if fuel == 0:
            if self.map[row][col] == "F":
                arcs.append(Arc(tail, (row, col, 9), "Fuel up", 15))
            return arcs

        else:
            for option in self.movement:
                arcs += (self.out_going_arcs_movement(tail, option))

            if (row, col) in self.teleport_spots:
                for teleport_spot in self.teleport_spots:
                    if (row, col) != teleport_spot:
                        arcs.append(Arc(tail, (teleport_spot[0], teleport_spot[1], fuel), "Teleport to ({}, {})".format(teleport_spot[0], teleport_spot[1]), 10))

            if self.map[row][col] == "F" and fuel < 9:
                arcs.append(Arc(tail, (row, col, 9), "Fuel up", 15))

        return arcs

    def out_going_arcs_movement(self, tail, option):
        arcs = []
        row, col = tail[0] + option[1], tail[1] + option[2]
        if self.map[row][col] not in ["X", "|", "-", "+"]:
            arcs.append(Arc(tail, (row, col, tail[2] - 1), option[0], 5))
        return arcs

    def getMap(self, map_str):
        """Returns a 2d array representation of the map string"""
        map_str = map_str.strip()
        map = []
        row = []
        new_row = True
        for i in range(0, len(map_str)):
            if new_row and (map_str[i] == "+" or map_str[i] == "|"):
                row.append(map_str[i])
                new_row = False
            elif not new_row and (map_str[i] == "\n"):
                map.append(row)
                row = []
                new_row = True
            elif not new_row and (i == len(map_str) - 1):
                row.append(map_str[i])
                map.append(row)
            elif not new_row:
                row.append(map_str[i])
        return map

    def find_on_map(self, characters):
        items = []
        for i in range(0, len(self.map)):
            for j in range(0, len(self.map[i])):
                if self.map[i][j] in characters:
                    items.append((i, j))
        return items

    def estimated_cost_to_goal(self, node):
        """Return the estimated cost to a goal node from the given
        state. This function is usually implemented when there is a
        single goal state. The function is used as a heuristic in
        search. The implementation should make sure that the heuristic
        meets the required criteria for heuristics."""
        head = node.head
        row = head[0]
        col = head[1]
        estimated_cost = []
        for goal in self.goal_spots:
            estimated_cost.append((abs(row - goal[0]) + abs(col - goal[1])) * 5)
        return min(estimated_cost)


class AStarFrontier(Frontier):
    def __init__(self, graph):
        """The constructor takes no argument. It initialises the
        container to an empty stack."""
        self.container = []
        self.index = 0
        self.graph = graph
        self.visited = []

    def add(self, path):
        cost = 0
        for arcs in path:
            cost += arcs.cost
        cost += self.graph.estimated_cost_to_goal(path[-1])
        heapq.heappush(self.container, (cost, self.index, path))
        self.index += 1

    def __iter__(self):
        """The object returns itself because it is implementing a __next__
        method and does not need any additional state for iteration."""
        return self

    def __next__(self):
        while True:
            if len(self.container) > 0:
                x = heapq.heappop(self.container)
                if(x[-1][-1].head not in self.visited):
                    self.visited.append(x[-1][-1].head)
                    return x[-1]
            else:
                raise StopIteration  # don't change this one


def print_map(map_graph, frontier, solution):
    solution_map_list = map_graph.map
    for visited in frontier.visited:
        row = visited[0]
        col = visited[1]
        if solution_map_list[row][col] not in ["G", "S", "X", "F", "P", "|", "+"]:
            solution_map_list[row][col] = "."
    if solution is not None:
        for arcs in solution:
            row = arcs.head[0]
            col = arcs.head[1]
            if solution_map_list[row][col] not in ["G", "S", "X", "F", "P", "|", "+"]:
                solution_map_list[row][col] = "*"

    for lists in solution_map_list:
        lists.append("\n")
    solution_map_list[-1].pop()
    solution_map_string = ''.join(str(item) for innerlist in solution_map_list for item in innerlist)
    print(solution_map_string)





def main():
    map_str = """\
    +----+
    |    |
    | SX |
    | X G|
    +----+
    """

    map_graph = RoutingGraph(map_str)
    frontier = AStarFrontier(map_graph)
    solution = next(generic_search(map_graph, frontier), None)
    print_map(map_graph, frontier, solution)

if __name__ == "__main__":
    main()
