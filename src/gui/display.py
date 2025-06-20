import pygame
import sys

class Display:
    """
    Pygame-based visualization for the pursuit-evasion environment.
    """
    def __init__(self, env, cell_size=10, fps=10):
        pygame.init()
        self.env = env
        self.cell_size = cell_size
        self.fps = fps
        self.grid_size = env.size
        self.width = self.grid_size * cell_size
        self.height = self.grid_size * cell_size

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pursuit-Evasion Simulation")
        self.clock = pygame.time.Clock()

    def render(self):
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear screen
        self.screen.fill((255, 255, 255))

        # Draw grid lines
        for x in range(self.grid_size + 1):
            pygame.draw.line(
                self.screen,
                (200, 200, 200),
                (x * self.cell_size, 0),
                (x * self.cell_size, self.height)
            )
        for y in range(self.grid_size + 1):
            pygame.draw.line(
                self.screen,
                (200, 200, 200),
                (0, y * self.cell_size),
                (self.width, y * self.cell_size)
            )

        # Draw evader (green)
        ex, ey = self.env.evader_pos
        ev_rect = pygame.Rect(
            ex * self.cell_size,
            ey * self.cell_size,
            self.cell_size,
            self.cell_size
        )
        pygame.draw.rect(self.screen, (0, 200, 0), ev_rect)

        # Draw pursuer (red)
        px, py = self.env.pursuer_pos
        pu_rect = pygame.Rect(
            px * self.cell_size,
            py * self.cell_size,
            self.cell_size,
            self.cell_size
        )
        pygame.draw.rect(self.screen, (200, 0, 0), pu_rect)

        # Flip display and tick
        pygame.display.flip()
        self.clock.tick(self.fps)

    def quit(self):
        pygame.quit()
        sys.exit()
