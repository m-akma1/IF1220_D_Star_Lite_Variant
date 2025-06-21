import pygame
import sys
import math

class Display:
    """
    Pygame-based visualization for the pursuit-evasion environment with padding, overlay text,
    playback controls, terrain shading, interactive cost editing (including walls),
    and dynamic planner updates.

    To support dynamic terrain updates, pass the evader_planner (DStarLite instance)
    into the constructor so we can notify it of cost changes.
    """
    def __init__(self, env, evader_planner, cell_size=10, fps=10, padding=50):
        pygame.init()
        self.env = env
        self.evader_planner = evader_planner
        self.cell_size = cell_size
        self.fps = fps
        self.grid_size = env.size
        self.padding = padding

        # Window dimensions
        self.width = self.grid_size * cell_size + 2 * padding
        self.height = self.grid_size * cell_size + 2 * padding

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pursuit-Evasion Simulation")
        self.clock = pygame.time.Clock()

        # Font for overlay
        self.font = pygame.font.SysFont(None, 24)

        # Control flags
        self.paused = False
        self.step_once = False

    def _notify_planner(self, cell):
        """
        After changing the cost of a cell, update D* Lite planner's queue.
        """
        # Update this cell
        self.evader_planner._update_vertex(cell)
        # Update all neighbors of this cell
        for nbr in self.evader_planner._neighbors(cell):
            self.evader_planner._update_vertex(nbr)

    def render(self):
        ox, oy = self.padding, self.padding
        grid_w = self.grid_size * self.cell_size
        grid_h = self.grid_size * self.cell_size

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_s:
                    self.step_once = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                # Inside grid?
                if ox <= mx < ox + grid_w and oy <= my < oy + grid_h:
                    cx = (mx - ox) // self.cell_size
                    cy = (my - oy) // self.cell_size
                    cell = (cx, cy)
                    # Wall toggle with SHIFT
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        if event.button == 1:
                            self.env.set_cost(cx, cy, math.inf)
                        elif event.button == 3:
                            self.env.set_cost(cx, cy, 1)
                    else:
                        # Increase/decrease cost
                        if event.button == 1:
                            new_cost = self.env.costs[cx][cy] + 1
                            self.env.set_cost(cx, cy, new_cost)
                        elif event.button == 3:
                            new_cost = max(1, self.env.costs[cx][cy] - 1)
                            self.env.set_cost(cx, cy, new_cost)
                    # Notify planner of this change
                    self._notify_planner(cell)

        # Pause logic
        if self.paused and not self.step_once:
            self._draw_frame()
            while True:
                ev = pygame.event.wait()
                if ev.type == pygame.QUIT:
                    self.quit()
                elif ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_SPACE:
                        self.paused = False
                        break
                    elif ev.key == pygame.K_s:
                        self.step_once = True
                        break
                    elif ev.key == pygame.K_q:
                        self.quit()
                elif ev.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = ev.pos
                    if ox <= mx < ox + grid_w and oy <= my < oy + grid_h:
                        cx = (mx - ox) // self.cell_size
                        cy = (my - oy) // self.cell_size
                        cell = (cx, cy)
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            if ev.button == 1:
                                self.env.set_cost(cx, cy, math.inf)
                            elif ev.button == 3:
                                self.env.set_cost(cx, cy, 1)
                        else:
                            if ev.button == 1:
                                new_cost = self.env.costs[cx][cy] + 1
                                self.env.set_cost(cx, cy, new_cost)
                            elif ev.button == 3:
                                new_cost = max(1, self.env.costs[cx][cy] - 1)
                                self.env.set_cost(cx, cy, new_cost)
                        self._notify_planner(cell)
                    if self.step_once:
                        break

        # Draw and advance
        self._draw_frame()
        if self.step_once:
            self.step_once = False
        pygame.display.flip()
        self.clock.tick(self.fps)

    def _draw_frame(self):
        self.screen.fill((255, 255, 255))
        ox, oy = self.padding, self.padding

        # Shade terrain
        finite = [c for row in self.env.costs for c in row if not math.isinf(c)]
        max_c = max(finite) if finite and max(finite) > 1 else 1
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                cost = self.env.costs[x][y]
                if math.isinf(cost): color = (0,0,0)
                else:
                    norm = (cost-1)/(max_c-1) if max_c>1 else 0
                    intensity = 255 - int(norm*254)
                    color = (intensity,)*3
                r = pygame.Rect(ox+x*self.cell_size, oy+y*self.cell_size,
                                self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, color, r)

        # Overlay text
        info = f"Step {self.env.step_count}  Evader: {self.env.evader_pos}  Pursuer: {self.env.pursuer_pos}"
        txt = self.font.render(info, True, (0,0,0))
        self.screen.blit(txt, (self.padding, self.padding//4))

        # Grid lines
        for i in range(self.grid_size+1):
            px = ox + i*self.cell_size
            pygame.draw.line(self.screen, (200,200,200), (px,oy), (px,oy+self.grid_size*self.cell_size))
            py = oy + i*self.cell_size
            pygame.draw.line(self.screen, (200,200,200), (ox,py), (ox+self.grid_size*self.cell_size,py))

        # Goal, Evader, Pursuer
        gx, gy = self.env.evader_goal
        pygame.draw.rect(self.screen, (0,0,200),
                         (ox+gx*self.cell_size, oy+gy*self.cell_size,
                          self.cell_size, self.cell_size))
        ex, ey = self.env.evader_pos
        pygame.draw.rect(self.screen, (0,200,0),
                         (ox+ex*self.cell_size, oy+ey*self.cell_size,
                          self.cell_size, self.cell_size))
        px, py = self.env.pursuer_pos
        pygame.draw.rect(self.screen, (200,0,0),
                         (ox+px*self.cell_size, oy+py*self.cell_size,
                          self.cell_size, self.cell_size))

    def quit(self):
        while True:
                ev = pygame.event.wait()
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_q:
                        break
        pygame.quit()
        sys.exit()
