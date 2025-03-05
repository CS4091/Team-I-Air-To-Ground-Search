import pandas as pd
import pathlib
import json
from typing import Tuple


class GridWorld:
    def __init__(self, filepath: pathlib.Path):
        self.filepath: pathlib.Path = filepath

        world_data: Tuple[pd.DataFrame, dict] = self.load_world(self.filepath)
        self.world_grid, self.world_params = world_data

        self.starting_row: int = self.world_params["startPosition"]["row"]
        self.starting_col: int = self.world_params["startPosition"]["col"]

        self.num_moves: int = self.world_params["numMoves"]

        self.forward_range: int = self.world_params["sensorSize"]["forwardRange"]
        self.lateral_width: int = self.world_params["sensorSize"]["lateralWidth"]

    @staticmethod
    def load_world(filepath: pathlib.Path) -> Tuple[pd.DataFrame, dict]:
        world_df: pd.DataFrame = pd.read_csv(filepath / "grid_world.csv", header=None)
        f = open(filepath / "grid_world_params.json")
        world_params: dict = json.load(f)
        f.close()

        return world_df, world_params


if __name__ == "__main__":
    world = GridWorld(pathlib.Path("./src/external/").resolve())
    print(world.world_params)
