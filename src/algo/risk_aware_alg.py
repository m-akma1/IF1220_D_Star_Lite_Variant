import math
from algo.d_star_lite import DStarLite

class RiskAwareDStar(DStarLite):
    """
    Risk-Aware D* Lite: adds a dynamic repulsive penalty around the pursuer position.

    @param size: grid dimension
    @param start: initial evader position (x,y)
    @param goal: goal position (x,y)
    @param env: Environment instance with terrain costs
    @param r: risk radius threshold (cells)
    @param lambda_: penalty scaling factor
    """
    def __init__(self, size, start, goal, env, r, lambda_):
        self.r = r
        self.lambda_ = lambda_
        self.risk = { (x,y): 0.0 for x in range(size) for y in range(size) }
        super().__init__(size=size, start=start, goal=goal, env=env, heuristic=None)

    def _update_risk(self, pursuer_pos):
        """
        Compute rho_t(v) for all v within risk radius, reset others to zero.
        """
        cx, cy = pursuer_pos
        for v in list(self.risk.keys()):
            dx = abs(v[0] - cx)
            dy = abs(v[1] - cy)
            d_cheb = max(dx, dy)
            if d_cheb <= self.r:
                self.risk[v] = self.lambda_ * (self.r - d_cheb)
            else:
                self.risk[v] = 0.0
            # mark affected nodes inconsistent
            self._update_vertex(v)
            for u in self._neighbors(v):
                self._update_vertex(u)

    def _cost(self, a, b):
        """
        Augmented weight: base terrain cost + risk penalty at target cell b.
        Overrides parent _cost.
        """
        base = super()._cost(a, b)
        risk_pen = self.risk.get(b, 0.0)
        return base + risk_pen

    def plan(self, new_start=None, pursuer_pos=None):
        """
        Replan path with risk-aware costs. Must pass current pursuer_pos.
        Returns list of (dx, dy) moves.
        """
        if pursuer_pos is None:
            raise ValueError("RiskAwareDStar.plan requires pursuer_pos argument")
        # first, compute new risk penalties and enqueue affected vertices
        self._update_risk(pursuer_pos)
        # then proceed with standard D* Lite incremental replanning
        return super().plan(new_start)
