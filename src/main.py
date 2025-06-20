import ctypes
from sim.environment import Environment
from gui.display import Display

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

def main():
    env = Environment(size=32, max_steps=1000, seed=42)
    disp = Display(env, cell_size=20, fps=5)
    # Random-walk pursuer and evader stationary just for display
    while True:
        # no movement: keep both at start to see colored squares
        disp.render()

if __name__ == '__main__':
    main()
