import heapq
import math

class DStarLite:
    """
    Vanilla D* Lite implementation for an open 2D grid.
    Replans incrementally as the start (evader) moves.
    """
    def __init__(self, size, start, goal, env, heuristic=None):
        """
        :param size: grid dimension (size x size)
        :param start: tuple (x,y) initial start position
        :param goal: tuple (x,y) goal position
        :param heuristic: function h(a,b) returning estimated cost between cells
        """
        self.size = size
        self.start = start
        self.last = start
        self.goal = goal
        self.env = env
        self.km = 0
        self.heuristic = heuristic or (lambda a, b: max(abs(a[0]-b[0]), abs(a[1]-b[1])))

        # g and rhs values
        self.g = {}
        self.rhs = {}

        # Priority queue and entry tracker
        self.queue = []  # heap of (k1, k2, node)
        self.entry_finder = {}  # node -> (k1, k2)

        self._initialize()

    def _initialize(self):
        """Initialize g, rhs for all nodes, add goal to queue, and compute initial shortest paths."""
        inf = math.inf
        for x in range(self.size):
            for y in range(self.size):
                self.g[(x, y)] = inf
                self.rhs[(x, y)] = inf
        self.rhs[self.goal] = 0
        self.km = 0
        self.last = self.start
        self.queue.clear()
        self.entry_finder.clear()
        self._add_to_queue(self.goal)
        self._compute_shortest_path()

    def _calculate_key(self, node):
        g_rhs = min(self.g[node], self.rhs[node])
        return (g_rhs + self.heuristic(self.start, node) + self.km, g_rhs)

    def _add_to_queue(self, node):
        """Add or update a node's key in the priority queue."""
        if node in self.entry_finder:
            del self.entry_finder[node]
        key = self._calculate_key(node)
        entry = (key[0], key[1], node)
        self.entry_finder[node] = key
        heapq.heappush(self.queue, entry)

    def _pop_queue(self):
        """Pop the smallest valid entry from the queue, skipping outdated ones."""
        while self.queue:
            k1, k2, node = heapq.heappop(self.queue)
            if node in self.entry_finder and self.entry_finder[node] == (k1, k2):
                del self.entry_finder[node]
                return (k1, k2, node)
        return (None, None, None)

    def _peek_queue(self):
        """Return the smallest valid entry without removing it."""
        while self.queue:
            k1, k2, node = self.queue[0]
            if node in self.entry_finder and self.entry_finder[node] == (k1, k2):
                return (k1, k2, node)
            heapq.heappop(self.queue)
        return (None, None, None)

    def _update_vertex(self, u):
        """Update or remove and reinsert vertex u based on its rhs and g values."""
        if u != self.goal:
            self.rhs[u] = min(
                self._cost(u, s) + self.g[s] for s in self._neighbors(u)
            )
        if self.g[u] != self.rhs[u]:
            self._add_to_queue(u)
        elif u in self.entry_finder:
            del self.entry_finder[u]

    def _compute_shortest_path(self):
        """Main loop: process nodes until start is locally consistent."""
        while True:
            top_k1, top_k2, u = self._peek_queue()
            if u is None:
                break
            k_start = self._calculate_key(self.start)
            if (top_k1, top_k2) >= k_start and self.rhs[self.start] == self.g[self.start]:
                break
            _, _, u = self._pop_queue()
            if u is None:
                break
            k_old = (top_k1, top_k2)
            k_new = self._calculate_key(u)
            if k_old < k_new:
                self._add_to_queue(u)
            elif self.g[u] > self.rhs[u]:
                self.g[u] = self.rhs[u]
                for s in self._neighbors(u):
                    self._update_vertex(s)
            else:
                self.g[u] = math.inf
                for s in set(self._neighbors(u)) | {u}:
                    self._update_vertex(s)

    def plan(self, new_start=None):
        """Incrementally replan from new_start to goal; returns move list."""
        if new_start is not None:
            self.start = new_start
        self.km += self.heuristic(self.last, self.start)
        self.last = self.start
        self._update_vertex(self.start)
        self._compute_shortest_path()
        return self._reconstruct_path()

    def _reconstruct_path(self):
        """Follow the shortest-path tree from start to goal."""
        path = []
        curr = self.start
        inf = math.inf
        while curr != self.goal and self.g[curr] < inf:
            succ = min(
                self._neighbors(curr),
                key=lambda s: self._cost(curr, s) + self.g[s]
            )
            dx = succ[0] - curr[0]
            dy = succ[1] - curr[1]
            path.append((dx, dy))
            curr = succ
        return path

    def _neighbors(self, node):
        """Return 8-connected neighbors."""
        x, y = node
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    yield (nx, ny)

    def _cost(self, a, b):
        return self.env.get_cost(b)