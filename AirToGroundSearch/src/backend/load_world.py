import pathlib
import json
from typing import Tuple
import numpy as np
from .graph import TwoDimGraph
from ..algorithms.a_star import a_star_search
import os


class GridWorld:
    def __init__(self, filepath: pathlib.Path):
        self.filepath: pathlib.Path = filepath

        world_data: Tuple[np.ndarray, dict] = self.load_world(self.filepath)
        self.world_grid, self.world_params = world_data
        m, n = self.world_grid.shape
        self.world_grid = TwoDimGraph(m, n, self.world_grid.flatten())

        self.starting_row: int = self.world_params["startPosition"]["row"]
        self.starting_col: int = self.world_params["startPosition"]["col"]

        self.num_moves: int = self.world_params["numMoves"]

        self.forward_range: int = self.world_params["sensorSize"]["forwardRange"]
        self.lateral_width: int = self.world_params["sensorSize"]["lateralWidth"]

    @staticmethod
    def load_world(dirpath: pathlib.Path) -> Tuple[np.ndarray, dict]:
        world: np.ndarray = np.genfromtxt(dirpath / "grid_world.csv", delimiter=",")
        f = open(dirpath / "grid_world_params.json")
        world_params: dict = json.load(f)
        f.close()

        return world, world_params

    def run_search(self, search_type="astar"):
        if search_type == "astar":
            return a_star_search(
                self.world_grid,
                (self.starting_row, self.starting_col),
                (self.forward_range, self.lateral_width),
                self.num_moves,
            )

def is_dead_end(r, c, grid):
    # Checks if a provided cell is dead end, meaning its
    # surrounded on 3 sides by obstacles, including the edges of the grid.
    rows, cols = grid.shape

    if grid[r, c] == 1:
        return False  # Already an obstacle

    obstacle_count = 0


    neighbors = [
        (r - 1, c),  # Up
        (r + 1, c),  # Down
        (r, c - 1),  # Left
        (r, c + 1),  # Right
    ]
    for nr, nc in neighbors:
        if not (0 <= nr < rows and 0 <= nc < cols) or grid[nr, nc] == 1:
            obstacle_count += 1

    return obstacle_count >= 3

def propagate_dead_ends(grid):
    # Creates and returns a copy of the grid with dead ends marked
    # as unnavigable. They then propogate out until no more dead ends exist

    rows, cols = grid.shape
    reduced_grid = grid.copy()  # Create a copy of the grid

    def back_propagate_dead_end(r, c):
        # Recursvively marks dead ends as propagate outwards
        if not (0 <= r < rows and 0 <= c < cols) or reduced_grid[r, c] == 1:
            return

        if not is_dead_end(r, c, reduced_grid):
            return

        # Mark the current cell as unnavigable
        reduced_grid[r, c] = 1

        # Recursively propagate to neighbors
        neighbors = [
            (r - 1, c),  # Up
            (r + 1, c),  # Down
            (r, c - 1),  # Left
            (r, c + 1),  # Right
        ]
        for nr, nc in neighbors:
            back_propagate_dead_end(nr, nc)

    # Start by checking all cells for dead ends
    for i in range(rows):
        for j in range(cols):
            if reduced_grid[i, j] == 0 and is_dead_end(i, j, reduced_grid):
                back_propagate_dead_end(i, j)

    return reduced_grid

if __name__ == "__main__":
    parent = pathlib.Path(__file__).parent.parent.parent
    if os.path.exists(
        pathlib.Path(
            pathlib.Path(parent / "wwwroot/outputs/ImportedGrid/grid_world.csv")
        )
    ):
        grid_path = pathlib.Path(parent / "wwwroot/outputs/ImportedGrid").resolve()
    else:
        grid_path = pathlib.Path(
            parent / "wwwroot/outputs/GeneratedGrid/data"
        ).resolve()
    world = GridWorld(grid_path)
    # print(world.world_params)
    # print(world.run_search())
    world.run_search()
