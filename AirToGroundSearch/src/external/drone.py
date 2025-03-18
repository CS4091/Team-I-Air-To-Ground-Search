import numpy as np
from enum import Enum


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Drone:
    def __init__(self, grid, start_row, start_col):
        self.grid = grid
        self.row = start_row
        self.col = start_col
        self.direction = Direction.UP  # Initial direction

    def move_straight(self):
        if (
            self.direction == Direction.UP
            and self.row > 0
            and self.grid[self.row - 1, self.col] == 0
        ):
            self.row -= 1
        elif (
            self.direction == Direction.DOWN
            and self.row < self.grid.shape[0] - 1
            and self.grid[self.row + 1, self.col] == 0
        ):
            self.row += 1
        elif (
            self.direction == Direction.LEFT
            and self.col > 0
            and self.grid[self.row, self.col - 1] == 0
        ):
            self.col -= 1
        elif (
            self.direction == Direction.RIGHT
            and self.col < self.grid.shape[1] - 1
            and self.grid[self.row, self.col + 1] == 0
        ):
            self.col += 1

    def turn_left(self):
        if self.direction == Direction.UP:
            self.direction = Direction.LEFT
        elif self.direction == Direction.DOWN:
            self.direction = Direction.RIGHT
        elif self.direction == Direction.LEFT:
            self.direction = Direction.DOWN
        elif self.direction == Direction.RIGHT:
            self.direction = Direction.UP
        self.move_straight()

    def turn_right(self):
        if self.direction == Direction.UP:
            self.direction = Direction.RIGHT
        elif self.direction == Direction.DOWN:
            self.direction = Direction.LEFT
        elif self.direction == Direction.LEFT:
            self.direction = Direction.UP
        elif self.direction == Direction.RIGHT:
            self.direction = Direction.DOWN
        self.move_straight()

    def get_position(self):
        return self.row, self.col



def read_grid_from_csv(filepath):
    return np.loadtxt(filepath, delimiter=",", dtype=int)

def update_scanned_grid(drone, scanned_grid):
    if drone.direction == Direction.UP:
        view = [
            (drone.row - 1, drone.col - 1), (drone.row - 1, drone.col), (drone.row - 1, drone.col + 1),
            (drone.row, drone.col - 1), (drone.row, drone.col), (drone.row, drone.col + 1)
        ]
    elif drone.direction == Direction.DOWN:
        view = [
            (drone.row + 1, drone.col - 1), (drone.row + 1, drone.col), (drone.row + 1, drone.col + 1),
            (drone.row, drone.col - 1), (drone.row, drone.col), (drone.row, drone.col + 1)
        ]
    elif drone.direction == Direction.LEFT:
        view = [
            (drone.row - 1, drone.col - 1), (drone.row, drone.col - 1), (drone.row + 1, drone.col - 1),
            (drone.row - 1, drone.col), (drone.row, drone.col), (drone.row + 1, drone.col)
        ]
    elif drone.direction == Direction.RIGHT:
        view = [
            (drone.row - 1, drone.col + 1), (drone.row, drone.col + 1), (drone.row + 1, drone.col + 1),
            (drone.row - 1, drone.col), (drone.row, drone.col), (drone.row + 1, drone.col)
        ]

    for r, c in view:
        if 0 <= r < scanned_grid.shape[0] and 0 <= c < scanned_grid.shape[1]:
            scanned_grid[r, c] = 1

def calculate_coverage(scanned_grid, grid):
    navigable_tiles = np.sum(grid == 0)
    scanned_tiles = np.sum((scanned_grid == 1) & (grid == 0))
    return (scanned_tiles / navigable_tiles) * 100

def find_start_coordinate(grid):
    while True:
        random_index = np.random.randint(0, grid.size)
        row_index = random_index // grid.shape[1]
        col_index = random_index % grid.shape[1]
        if grid[row_index, col_index] == 0:
            return row_index, col_index

def print_grid_with_drone(grid, drone):
    grid_copy = grid.copy()
    grid_copy[drone.row, drone.col] = "2"  # Mark the drone's position with a 2
    for row in grid_copy:
        print(" ".join(str(cell) for cell in row))
    print()
