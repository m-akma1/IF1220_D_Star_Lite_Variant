# Map Directory

This directory contains predefined maps for the simulation. The maps are stored in CSV format, where each cell have a weight representing its cost or difficulty to traverse. The format is as follows:
 - Each line represents a column in the grid, and each value in the line represents a cell in that column.
 - The values are integers, where:
   - $0$ represents a wall (impassable or have infinite cost)
   - $1$ represents a normal cell (default cost with no obstacle)
   - $> 1$ represents a cell with higher cost or difficulty to traverse

Note:
- To use a map, you can load it using the `--load-map` argument when running the simulation.
- To save the current grid as a map, you can use the `--save-map` argument followed by the desired filename. The saved map will be stored in this directory.
- The `--grid size` argument passed must be equal or larger than the size of the map loaded.
