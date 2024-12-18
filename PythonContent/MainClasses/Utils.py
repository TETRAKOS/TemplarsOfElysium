import Entities
import heapq
import MapGen

def get_distance_from_actors(actor1, actor2):
    if isinstance(actor1, Entities.Actor) and isinstance(actor2, Entities.Actor):
        distance_x = abs(actor1.pos[0] - actor2.pos[0])
        distance_y = abs(actor1.pos[1] - actor2.pos[1])
        actor_distance = max(distance_x, distance_y)
        return actor_distance


def a_star_search(grid, start, goal, game):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(node):
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x, y = node[0] + dx, node[1] + dy
            if 0 <= x < grid.width and 0 <= y < grid.height:
                cell = grid.get_cell(x, y)
                if not grid.cell_contains(x,y,Entities.Actor): #and not grid.cell_contains(x,y,Entities.Wall):
                    neighbors.append((x, y))
        return neighbors

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for neighbor in get_neighbors(current):
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None