import pygame
import sys
import math

class Display:
    """
    Pygame-based visualization for the pursuit-evasion environment with padding, overlay text, playback controls, and terrain shading.
    """
    def __init__(self, env, cell_size=10, fps=10, padding=50):
        pygame.init()
        self.env = env
        self.cell_size = cell_size
        self.fps = fps
        self.grid_size = env.size
        self.padding = padding

        # Compute window dimensions including padding border
        self.width = self.grid_size * cell_size + 2 * padding
        self.height = self.grid_size * cell_size + 2 * padding

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pursuit-Evasion Simulation")
        self.clock = pygame.time.Clock()

        # Font for overlay text
        self.font = pygame.font.SysFont(None, 24)

        # Control flags
        self.paused = False
        self.step_once = False

    def render(self):
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_s:
                    self.step_once = True

        # Pause logic
        if self.paused and not self.step_once:
            self._draw_frame()
            while True:
                ev = pygame.event.wait()
                if ev.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_SPACE:
                        self.paused = False
                        break
                    elif ev.key == pygame.K_s:
                        self.step_once = True
                        break

        # Draw frame
        self._draw_frame()

        # Reset step flag
        if self.step_once:
            self.step_once = False

        pygame.display.flip()
        self.clock.tick(self.fps)

    def _draw_frame(self):
        # Clear background
        self.screen.fill((255, 255, 255))

        ox, oy = self.padding, self.padding

        # Shade terrain by cost
        # Determine max finite cost for scaling
        finite_costs = [c for row in self.env.costs for c in row if not math.isinf(c)]
        max_cost = max(finite_costs) if finite_costs else 1
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                cost = self.env.costs[x][y]
                if math.isinf(cost):
                    color = (0, 0, 0)
                else:
                    # lighter for low cost, darker for high
                    intensity = int((cost / max_cost) * 255)
                    color = (intensity, intensity, intensity)
                rect = pygame.Rect(
                    ox + x * self.cell_size,
                    oy + y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(self.screen, color, rect)

        # Draw overlay text
        info = f"Step {self.env.step_count}  Evader: {self.env.evader_pos}  Pursuer: {self.env.pursuer_pos}"
        text_surf = self.font.render(info, True, (0, 0, 0))
        self.screen.blit(text_surf, (self.padding, self.padding // 4))

        # Draw grid lines
        for x in range(self.grid_size + 1):
            px = ox + x * self.cell_size
            pygame.draw.line(
                self.screen, (200, 200, 200),
                (px, oy), (px, oy + self.grid_size * self.cell_size)
            )
        for y in range(self.grid_size + 1):
            py = oy + y * self.cell_size
            pygame.draw.line(
                self.screen, (200, 200, 200),
                (ox, py), (ox + self.grid_size * self.cell_size, py)
            )

        # Draw goal (blue)
        gx, gy = self.env.evader_goal
        pygame.draw.rect(
            self.screen, (0, 0, 200),
            (ox + gx * self.cell_size,
             oy + gy * self.cell_size,
             self.cell_size,
             self.cell_size)
        )

        # Draw evader (green) and pursuer (red)
        ex, ey = self.env.evader_pos
        pygame.draw.rect(
            self.screen, (0, 200, 0),
            (ox + ex * self.cell_size,
             oy + ey * self.cell_size,
             self.cell_size,
             self.cell_size)
        )

        px, py = self.env.pursuer_pos
        pygame.draw.rect(
            self.screen, (200, 0, 0),
            (ox + px * self.cell_size,
             oy + py * self.cell_size,
             self.cell_size,
             self.cell_size)
        )

    def quit(self):
        pygame.quit()
        sys.exit()
