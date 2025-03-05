import pandas as pd
import pathlib
import json

def load_world(filepath: pathlib.Path):
    world_df = pd.read_csv(filepath / "grid_world.csv", header=None)
    f = open(filepath / "grid_world_params.json")
    world_params = json.load(f)
    f.close()

    return world_df, world_params


if __name__ == "__main__":
    world_df, world_params = load_world(pathlib.Path("./src/external/").resolve())
    print(world_params)