import numpy as np
import pathlib
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


if __name__ == "__main__":
    grid_filepath = pathlib.Path("./wwwroot/outputs/grid_world.csv")
    grid = read_grid_from_csv(grid_filepath)

    start_row, start_col = find_start_coordinate(grid)
    drone = Drone(grid, start_row, start_col)

    while True:
        print_grid_with_drone(grid, drone)
        print(
            f"Drone current position: {drone.get_position()}, facing {drone.direction.name}"
        )
        command = (
            input(
                "Enter command (S for straight, L for left, R for right, Q to quit): "
            )
            .strip()
            .upper()
        )
        if command == "S":
            drone.move_straight()
        elif command == "L":
            drone.turn_left()
        elif command == "R":
            drone.turn_right()
        elif command == "Q":
            break
        else:
            print("Invalid command. Please enter S, L, R, or Q.")

    print("Drone final position:", drone.get_position())
