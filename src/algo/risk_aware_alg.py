import math
from algo.d_star_lite import DStarLite

class RiskAwareDStar(DStarLite):
    """
    Risk-Aware D* Lite: adds a dynamic repulsive penalty around the pursuer position,
    scaled by distance remaining to the goal.
    """
    def __init__(self, size, start, goal, env, r, lambda_):
        self.r = r
        self.lambda_ = lambda_
        self.risk = {(x, y): 0.0 for x in range(size) for y in range(size)}
        super().__init__(size=size, start=start, goal=goal, env=env, heuristic=None)

    def _update_risk(self, pursuer_pos):
        """
        Compute the time-varying risk penalty:
        rho _t(v) = lambda . d_cheb(e_t, g) . max(0, r - d_cheb(v, c_t))
        for all v within radius r of pursuer c_t, reset others to zero.
        Enqueue affected vertices in the D* Lite queue.
        """
        # Distance remaining for evader to goal
        ev_to_goal = self.heuristic(self.start, self.goal)
        cx, cy = pursuer_pos
        for v in list(self.risk.keys()):
            # Compute Chebyshev distance to pursuer
            dv = max(abs(v[0] - cx), abs(v[1] - cy))
            # Calculate risk penalty
            if dv <= self.r:
                self.risk[v] = self.lambda_ * ev_to_goal * (self.r - dv)
            else:
                self.risk[v] = 0.0
            # Mark this cell and its neighbors as inconsistent
            self._update_vertex(v)
            for u in self._neighbors(v):
                self._update_vertex(u)

    def _cost(self, a, b):
        """
        Augmented weight: base terrain cost + risk penalty at target cell b.
        Overrides the parent _cost.
        """
        base = super()._cost(a, b)
        return base + self.risk.get(b, 0.0)

    def plan(self, new_start=None, pursuer_pos=None):
        """
        Replan path with risk-aware costs. Requires current pursuer_pos.
        Returns list of (dx, dy) moves.
        """
        if pursuer_pos is None:
            raise ValueError("RiskAwareDStar.plan requires pursuer_pos argument")
        # Update current start (evader) if moved
        if new_start is not None:
            self.start = new_start
        # Update risk penalties and enqueue
        self._update_risk(pursuer_pos)
        # Proceed with standard D* Lite incremental replanning
        return super().plan(new_start)
