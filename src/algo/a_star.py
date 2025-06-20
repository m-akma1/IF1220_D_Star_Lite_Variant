import heapq

class AStar:
    """
    A simple A* planner on an open 2D grid.
    Recomputes the shortest path from start to goal on each call to plan().
    """
    def __init__(self, size, obstacles=None):
        """
        :param size: int, dimension of the square gri   d (size x size)
        :param obstacles: iterable of (x,y) tuples marking blocked cells
        """
        self.size = size
        self.obstacles = set(obstacles) if obstacles else set()

    def heuristic(self, a, b):
        """
        Manhattan distance heuristic.
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def neighbors(self, node):
        """
        Generate traversable neighbor cells (4-connectivity).
        """
        x, y = node
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if (nx, ny) not in self.obstacles:
                    yield (nx, ny)

    def plan(self, start, goal):
        """
        Compute a shortest-path from start to goal, returning a list of moves.
        Each move is a (dx, dy) tuple.
        """
        frontier = []
        # (f_score, g_score, node)
        heapq.heappush(frontier, (self.heuristic(start, goal), 0, start))

        came_from = {start: None}
        g_score = {start: 0}

        while frontier:
            f, current_g, current = heapq.heappop(frontier)
            if current == goal:
                return self._reconstruct_path(came_from, start, goal)

            for neighbor in self.neighbors(current):
                tentative_g = current_g + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    priority = tentative_g + self.heuristic(neighbor, goal)
                    heapq.heappush(frontier, (priority, tentative_g, neighbor))
                    came_from[neighbor] = current

        # No path found
        return []

    def _reconstruct_path(self, came_from, start, goal):
        """
        Reconstruct the list of moves from start to goal.
        """
        path = []
        current = goal
        while current != start:
            prev = came_from[current]
            dx = current[0] - prev[0]
            dy = current[1] - prev[1]
            path.append((dx, dy))
            current = prev
        path.reverse()
        return path
