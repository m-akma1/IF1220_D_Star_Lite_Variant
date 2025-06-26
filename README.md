# A D\*-Lite Variant for Dynamic Pursuit–Evasion Scenario on Grid Graphs

This repository contains a Python simulation of a pursuit–evasion scenario on an open 2D grid based on a paper with the same title. 
The **Evader** uses a Risk-Aware D\*-Lite planner to replan its path at each time step, knowing the current pursuer location and avoid it. The **Pursuer** follows a modified A\* Algorithm to intercept and chase the evader.

Access the Paper [here](https://informatika.stei.itb.ac.id/~rinaldi.munir/Matdis/2024-2025-2/Makalah2025/Makalah-Matdis-2025-IF-ITB%20(146).pdf).

## Features
- Discrete-time simulation on an $N\times N$ grid  
- Evader path-planning with vanilla and risk-aware D\*-Lite  
- Metrics logged per run:
  - **Path cost**
  - **Planning runtime**
  - **Win and capture rate**
- Simple Pygame GUI to visualize agents and metrics overlay  
- Configurable grid size, seed, and radius in CLI
- Ability to load and save maps

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
   python -m main
   ```

## Control The Simulation

You can control the simulation using the following keys in the Pygame window:
- **Space**: Pause/Resume the simulation
- **Left Click**: Increase the weight of a cell at the clicked position
- **Right Click**: Decrease the weight of a cell at the clicked position
- **Shift + Left Click**: Place a wall at the clicked position
- **Shift + Right Click**: Delete a wall at the clicked position
- **Q**: Quit the simulation. This action can only be performed when the simulation is paused or finished

## Parsing Arguments

The script uses the `argparse` library to handle command-line arguments. Here are the main arguments you can configure:

- `--grid-size`: Set the size of the grid (default: 64)
- `--fps`: Set the frames per second for the simulation (default: 5)
- `--load-map`: Load a predefined map from the [`map`](map) directory
- `--save-map`: Save the current grid as a map file in the [`map`](map) directory
- `--radius`: Set the pursuit radius for the pursuer (default: 1 i.e. normal D*-Lite)
- `--penalty`: Set the penalty for the pursuer (default: 0 i.e. normal D*-Lite)

Example usage:  
```bash
# Simulation with grid size 32x32, 10 fps, and normal D*-Lite Algorithm
python -m main --grid-size 32 --fps 10


# Simulation with default grid and fps, load the map at ../maps/map-0.csv, and normal D*-Lite
# Note: grid size must be bigger or same with the map size
python -m main --grid-size 72 --load-map ../maps/map-0.csv


# Simulation with default grid and fps, load the map at ../maps/map-2.csv,
# and using Risk D*-Lite with r = 8 and lambda = 1.5
python -m main --load-map ../maps/map-0.csv --radius 8 --penalty 1.5
```

## Experiment Simulation

To run the simulation with a specific configuration, you can use the following command:

```bash
python -m experiment
```

This will execute the experiment script, which runs multiple simulations with different configurations and logs the results.

**Warning**: The experiment script is computationally heavy even for high-end CPUs. It is recommended to run it on a machine with at least 8GB of RAM and a multi-core processor with high clock speed.

## License

Created by Muhammad Akmal (13524099)
For IF1220 Discrete Mathematics Paper Assignment  
Semester 2 Academic Year 2024/2025

[MIT LICENSE &copy; 2025 Muhammad Akmal](LICENSE).

