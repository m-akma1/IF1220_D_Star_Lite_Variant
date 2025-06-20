import heapq
import math

class AStar:
    """
    A* planner on a 2D grid with dynamic terrain costs and 8-connectivity (King's moves).
    Recomputes the shortest path each call to plan(), taking into account `env.costs`.
    Walls (infinite cost) are treated as impassable.
    """
    def __init__(self, size, env, obstacles=None):
        """
        :param size: Grid dimension (size x size)
        :param env: Environment instance providing `get_cost(a,b)` and `costs` array
        :param obstacles: Iterable of fixed obstacle cells (optional)
        """
        self.size = size
        self.env = env
        self.obstacles = set(obstacles) if obstacles else set()

    def _cost(self, a, b):
        """Return dynamic move cost from cell a to b."""
        return self.env.get_cost(b)

    def heuristic(self, a, b):
        """Chebyshev distance heuristic (admissible if min cost >= 1)."""
        return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

    def neighbors(self, node):
        """Yield 8-connected neighbors with finite cost."""
        x, y = node
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    if (nx, ny) not in self.obstacles:
                        # Skip walls (infinite cost)
                        if not math.isinf(self.env.costs[nx][ny]):
                            yield (nx, ny)

    def plan(self, start, goal):
        """
        Compute a shortest-path from start to goal considering dynamic costs.
        Returns a list of (dx, dy) moves, or empty if unreachable.
        """
        frontier = []
        g_score = {start: 0}
        came_from = {start: None}

        # Push initial node as (f_score, node)
        initial_f = self.heuristic(start, goal)
        heapq.heappush(frontier, (initial_f, start))

        while frontier:
            f, current = heapq.heappop(frontier)
            if current == goal:
                return self._reconstruct_path(came_from, start, goal)

            current_g = g_score[current]
            for neighbor in self.neighbors(current):
                step_cost = self._cost(current, neighbor)
                tentative = current_g + step_cost
                if neighbor not in g_score or tentative < g_score[neighbor]:
                    g_score[neighbor] = tentative
                    priority = tentative + self.heuristic(neighbor, goal)
                    heapq.heappush(frontier, (priority, neighbor))
                    came_from[neighbor] = current

        # No path found
        return []

    def _reconstruct_path(self, came_from, start, goal):
        """
        Reconstruct list of (dx, dy) moves from start to goal.
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
