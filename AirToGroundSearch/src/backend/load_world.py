import pathlib
import json
from typing import Tuple
import numpy as np
from backend.graph import TwoDimGraph
from algorithms.a_star import a_star_search

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


if __name__ == "__main__":
    world = GridWorld(
        pathlib.Path("../wwwroot/outputs/GeneratedGrid").resolve()
    )
    print(world.world_params)
    print(world.run_search())
