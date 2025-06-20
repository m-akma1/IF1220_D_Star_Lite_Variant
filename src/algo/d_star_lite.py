import heapq
import math

class DStarLite:
    """
    Vanilla D* Lite implementation for an open 2D grid.
    Replans incrementally as the start (evader) moves.
    """
    def __init__(self, size, start, goal, heuristic=None):
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
        self.km = 0
        self.heuristic = heuristic or (lambda a, b: abs(a[0]-b[0]) + abs(a[1]-b[1]))

        # g and rhs values
        self.g = {}
        self.rhs = {}

        # Priority queue of nodes to process
        self.U = []  # list of (k1, k2, node)

        # Initialize
        self._initialize()

    def _initialize(self):
        """Initialize data structures and insert goal into U."""
        for x in range(self.size):
            for y in range(self.size):
                self.g[(x,y)] = math.inf
                self.rhs[(x,y)] = math.inf
        self.rhs[self.goal] = 0
        self.U = []
        heapq.heappush(self.U, (*self._calculate_key(self.goal), self.goal))
        self.km = 0
        self.last = self.start

    def _calculate_key(self, node):
        """Return the key for a node as a tuple (k1, k2)."""
        g_rhs = min(self.g[node], self.rhs[node])
        k1 = g_rhs + self.heuristic(self.start, node) + self.km
        k2 = g_rhs
        return (k1, k2)

    def _update_vertex(self, u):
        """Update or insert node u in the priority queue U."""
        if u != self.goal:
            # compute rhs from successors
            self.rhs[u] = min(
                self._cost(u, s) + self.g[s] for s in self._neighbors(u)
            )
        # remove u from U if present (lazy removal on pop)
        # then if g!=rhs, add with new key
        if self.g[u] != self.rhs[u]:
            heapq.heappush(self.U, (*self._calculate_key(u), u))

    def _compute_shortest_path(self):
        """Core loop of D* Lite until start is locally consistent."""
        while True:
            if not self.U:
                break
            k_old = self.U[0][:2]
            k_start = self._calculate_key(self.start)
            if k_old >= k_start and self.rhs[self.start] == self.g[self.start]:
                break

            _, _, u = heapq.heappop(self.U)
            k_new = self._calculate_key(u)
            if k_old < k_new:
                heapq.heappush(self.U, (*k_new, u))
            elif self.g[u] > self.rhs[u]:
                self.g[u] = self.rhs[u]
                for s in self._neighbors(u):
                    self._update_vertex(s)
            else:
                g_old = self.g[u]
                self.g[u] = math.inf
                for s in self._neighbors(u) | {u}:
                    self._update_vertex(s)

    def plan(self, new_start=None):
        """
        Replan path given new start position. Returns a list of (dx,dy) moves to goal.
        Call at each timestep with current start to replan incrementally.
        """
        if new_start is not None:
            self.start = new_start
        # update km based on moved start
        self.km += self.heuristic(self.last, self.start)
        self.last = self.start
        # update rhs of start
        self._update_vertex(self.start)
        # run main loop
        self._compute_shortest_path()
        # reconstruct path from start to goal
        return self._reconstruct_path()

    def _reconstruct_path(self):
        """Walk from start to goal following min-rhs neighbors."""
        path = []
        curr = self.start
        while curr != self.goal:
            # choose successor that minimizes cost+g
            succ = min(
                self._neighbors(curr),
                key=lambda s: self._cost(curr, s) + self.g[s]
            )
            dx = succ[0] - curr[0]
            dy = succ[1] - curr[1]
            path.append((dx, dy))
            curr = succ
            # safety to prevent infinite loop
            if len(path) > self.size**2:
                break
        return path

    def _neighbors(self, node):
        """Return 4-connected neighbors within grid bounds."""
        x, y = node
        nbrs = set()
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                nbrs.add((nx, ny))
        return nbrs

    def _cost(self, a, b):
        """Uniform cost of 1 for adjacent cells (open field)."""
        return 1
