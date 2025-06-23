# A D\*-Lite Variant for Dynamic Pursuit–Evasion Scenario on Grid Graphs

This repository contains a Python simulation of a pursuit–evasion scenario on an open 2D grid. 
The **Evader** uses a Risk-Aware D\*-Lite planner to replan its path at each time step, knowing the current pursuer location.  
The **Pursuer** follows a modified A\* Algorithm to intercept and chase the evader.  

## Features
- Discrete-time simulation on an $N\times N$ grid  
- Evader path-planning with vanilla and risk-aware D\*-Lite  
- Metrics logged per run:
  - **Path cost**
  - **Planning runtime**
  - **Win and capture rate**
- Simple Pygame GUI to visualize agents and metrics overlay  
- Configurable grid size, seed, and radius in CLI


## Getting Started

1. **Clone** this repo  
   ```bash
   git clone https://github.com/m-akma1/IF1220_D_Star_Lite_Variant.git
   cd IF1220_D_Star_Lite_Variant
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run** the demo GUI
   ```bash
   cd src
   python -m main --grid-size 64
   ```

## License

Created by Muhammad Akmal (13524099) for IF1220 Discrete Mathematics Paper Assignment.

[MIT LICENSE &copy; 2025 Muhammad Akmal](LICENSE).

