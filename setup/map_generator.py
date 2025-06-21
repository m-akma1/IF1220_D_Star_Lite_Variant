import csv
import random

def generate_map(rows, cols, wall_prob=0.1, hill_prob=0.15, hill_max=5):
    grid = []
    for _ in range(rows):
        row = []
        for _ in range(cols):
            r = random.random()
            if r < wall_prob:
                cell = 0
            elif r < wall_prob + hill_prob:
                cell = random.randint(2, hill_max)
            else:
                cell = 1
            row.append(cell)
        grid.append(row)
    return grid

def save_csv(grid, filename):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(grid)

rows, cols = 16, 16
grid = generate_map(rows, cols, wall_prob=0.15, hill_prob=0.15, hill_max=5)
save_csv(grid, "../setup/map-3.csv")
