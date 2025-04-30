import numpy as np
import pathlib
import os
import time
import json
from ..external.drone import (
    Drone,
    Direction,
    update_scanned_grid,
    read_grid_from_csv,
    calculate_coverage,
)

from ..backend.csv_to_png import display_grid

def read_json(filepath):
    with open(filepath, "r") as file:
        data = json.load(file)
    start_row = data["startPosition"]["row"]
    start_col = data["startPosition"]["col"]
    return start_row, start_col

def dfs_scan(grid: np.ndarray, fuel: int, scanned_grid: np.ndarray, drone: Drone):
    rows, cols = grid.shape
    start = (drone.row, drone.col)
    visited = np.zeros_like(grid, dtype=bool)
    stack = [(start, drone.direction)]
    moves = 0
    fuel_used = 0
    paths_considered = 0
    start_time = time.time()

    while stack and calculate_coverage(scanned_grid, grid) <= 80 and fuel_used < fuel:
        (current_row, current_col), current_direction = stack.pop()

        if visited[current_row, current_col]:
            continue

        visited[current_row, current_col] = True
        paths_considered += 1
        drone.row, drone.col = current_row, current_col
        drone.direction = current_direction
        update_scanned_grid(drone, scanned_grid)
        scanned_grid[drone.row, drone.col] = 3
        moves += 1

        # Explore neighbors in DFS order
        forward = drone.direction
        drone.turn_left()
        left = drone.direction
        drone.turn_right()
        drone.turn_right()
        right = drone.direction
        drone.turn_left()
        allowed_directions = [forward, left, right]

        for direction in allowed_directions:
            original_row, original_col = drone.row, drone.col
            original_direction = drone.direction

            if direction == forward:
                drone.move_straight()
            elif direction == left:
                drone.turn_left()
                drone.move_straight()
            elif direction == right:
                drone.turn_right()
                drone.move_straight()

            neighbor_row, neighbor_col = drone.row, drone.col

            if (
                0 <= neighbor_row < rows
                and 0 <= neighbor_col < cols
                and not visited[neighbor_row, neighbor_col]
            ):
                stack.append(((neighbor_row, neighbor_col), direction))

            # Reset drone position and direction
            drone.row, drone.col = original_row, original_col
            drone.direction = original_direction

        fuel_used += 1

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Fuel used: {fuel_used}")
    print(f"Start Position: {start}")
    print(f"End Position: {drone.row} {drone.col}")
    print(f"Moves: {moves}")
    print(f"Time: {elapsed_time:.2f} seconds")
    return scanned_grid


if __name__ == "__main__":
    generated_grid_filepath = pathlib.Path("AirToGroundSearch/wwwroot/outputs/GeneratedGrid/data/grid_world.csv")
    imported_grid_filepath = pathlib.Path(
        "AirToGroundSearch/wwwroot/outputs/ImportedGrid/grid_world.csv"
    )
    try:
        grid = read_grid_from_csv(imported_grid_filepath)
        start_row, start_col = read_json(
            pathlib.Path(
                "AirToGroundSearch/wwwroot/outputs/ImportedGrid/grid_world_params.json"
            )
        )
    except FileNotFoundError:
        grid = read_grid_from_csv(generated_grid_filepath)
        start_row, start_col = read_json(
            pathlib.Path(
                "AirToGroundSearch/wwwroot/outputs/GeneratedGrid/data/grid_world_params.json"
            )
        )
    fuel = 4000
    scanned_grid = grid.copy()
    scanned_grid = dfs_scan(
        grid, fuel, scanned_grid, Drone(grid, start_row, start_col)
    )
    """print("Final scanned grid:")
    print(scanned_grid)"""
    print(f"Coverage: {calculate_coverage(scanned_grid, grid):.2f}%")

    # Ensure the output directory exists
    output_dir = "/workspaces/Team-I-Air-To-Ground-Search/AirToGroundSearch/wwwroot/outputs/GridResults/"
    os.makedirs(output_dir, exist_ok=True)

    # Save the scanned grid to a text file
    with open(f"{output_dir}results_dfs.txt", "w") as file:
        file.write("Final scanned grid:\n")
        np.savetxt(file, scanned_grid, delimiter=",", fmt="%d")
        file.write(f"\nCoverage: {calculate_coverage(scanned_grid, grid):.2f}%\n")

    # Save the scanned grid to a CSV file
    np.savetxt(f"{output_dir}results_dfs.csv", scanned_grid, delimiter=",", fmt="%d")

    # Save the grid visualization
    display_grid(
        f"{output_dir}results_dfs.csv",
        f"{output_dir}results_dfs.png",
    )