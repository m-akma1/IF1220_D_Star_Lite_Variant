import numpy as np

class Environment:
    """
    Simulation environment for a pursuit-evasion scenario on a 2D grid.
    """
    def __init__(self, size=64, max_steps=500, seed=None):
        self.size = size
        self.max_steps = max_steps
        self.step_count = 0
        self.done = False
        self.caught = False
        self.reached_goal = False

        if seed is not None:
            np.random.seed(seed)

        self._init_positions()

    def _init_positions(self):
        # Starting positions: evader at top-left, goal at bottom-right, pursuer at bottom-left
        self.evader_start = (0, 0)
        self.evader_goal = (self.size - 1, self.size - 1)
        self.pursuer_start = (self.size - 1, 0)

        # Current positions initialized to start
        self.evader_pos = self.evader_start
        self.pursuer_pos = self.pursuer_start

    def get_state(self):
        """
        Returns the current state:
          - evader_pos: (x, y)
          - pursuer_pos: (x, y)
          - goal: (x, y)
          - step: current timestep
        """
        return {
            'evader_pos': self.evader_pos,
            'pursuer_pos': self.pursuer_pos,
            'goal': self.evader_goal,
            'step': self.step_count
        }

    def step(self, evader_move, pursuer_move=None):
        """
        Advance the simulation by one timestep.

        - evader_move: tuple (dx, dy)
        - pursuer_move: tuple (dx, dy), optional (if None, pursuer can be controlled externally)
        """
        if self.done:
            return

        # Move evader
        self.evader_pos = self._apply_move(self.evader_pos, evader_move)

        # Move pursuer if provided
        if pursuer_move is not None:
            self.pursuer_pos = self._apply_move(self.pursuer_pos, pursuer_move)

        self.step_count += 1

        # Check capture
        if self.evader_pos == self.pursuer_pos:
            self.caught = True
            self.done = True
            return

        # Check goal reached
        if self.evader_pos == self.evader_goal:
            self.reached_goal = True
            self.done = True
            return

        # Check for max steps
        if self.step_count >= self.max_steps:
            self.done = True

    def _apply_move(self, position, move):
        """
        Apply a move to a position, clamped within grid bounds.
        """
        x, y = position
        dx, dy = move
        new_x = np.clip(x + dx, 0, self.size - 1)
        new_y = np.clip(y + dy, 0, self.size - 1)
        return (int(new_x), int(new_y))
