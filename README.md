# A D\*-Lite Variant for Dynamic Pursuit–Evasion Scenario on Grid Graphs

This repository contains a minimal Python/Pygame simulation of a pursuit–evasion scenario on an open 2D grid.  
The **Evader** uses a Risk-Aware D\*-Lite planner to replan its path at each time step, knowing the current pursuer location.  
The **Pursuer** follows a (possibly adversarial) trajectory.  

## Features

- Discrete-time simulation on an $N\times N$ grid  
- Evader path-planning with vanilla and risk-aware D\*-Lite  
- Metrics logged per run:  
  - **Path cost** (weighted steps)  
  - **Planning runtime** (per step)  
  - **Capture rate** (fraction of trials caught)  
- Simple Pygame GUI to visualize agents and metrics overlay  
- Configurable grid size, seed, algorithm choice via YAML/CLI  

## Getting Started

1. **Clone** this repo  
   ```bash
   git clone https://github.com/yourusername/dstar-lite-pursuit-evade.git
   cd dstar-lite-pursuit-evade
   ```
2. **Create & activate** a virtualenv
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run** the demo GUI
   ```bash
   python -m src.main --grid-size 64 --steps 500
   ```

## License

Created by Muhammad Akmal (13524099) for IF1220 Discrete Mathematics Paper Assignment.

[MIT LICENSE &copy; 2025 Muhammad Akmal](LICENSE).

