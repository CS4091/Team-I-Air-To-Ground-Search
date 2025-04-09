import numpy as np
import json
import heapq
import pathlib
import os
from ..external.drone import (
    Drone,
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


def dijkstra_scan(grid: np.ndarray, fuel: int, scanned_grid: np.ndarray, drone: Drone):
    rows, cols = grid.shape
    # print(f"Start Position: {drone.row} {drone.col}")
    start = (drone.row, drone.col)
    # print(drone.row, drone)
    costs = np.full((rows, cols), np.inf)
    visited = np.zeros_like(grid, dtype=bool)
    queue = []
    start_direction = drone.direction
    heapq.heappush(queue, (0, start, start_direction))
    costs[start] = 0
    moves = 0

    while queue and moves < fuel:
        current_cost, (current_row, current_col), current_direction = heapq.heappop(
            queue
        )
        # print(current_direction)

        if visited[current_row, current_col]:
            continue

        visited[current_row, current_col] = True
        #previous_row = drone.row
        #previous_col = drone.col
        drone.row, drone.col = current_row, current_col
        drone.direction = current_direction
        update_scanned_grid(drone, scanned_grid)
        moves += 1
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
                and grid[neighbor_row, neighbor_col] != 1
            ):
                new_cost = current_cost + 1

                if new_cost < costs[neighbor_row, neighbor_col]:
                    costs[neighbor_row, neighbor_col] = new_cost
                    heapq.heappush(
                        queue, (new_cost, (neighbor_row, neighbor_col), direction)
                    )
                    # print(f"Adding to queue: ({neighbor_row}, {neighbor_col}), Facing: {direction}, Cost: {new_cost}")

            drone.row, drone.col = original_row, original_col
            drone.direction = original_direction
            #scanned_grid[previous_row, previous_col] = 2
            scanned_grid[drone.row, drone.col] = 3

        # print(previous_row, previous_col)
        # print(f"Scanned grid:\n{scanned_grid}")
        # print(f"Queue state: {queue}")

    return scanned_grid


if __name__ == "__main__":
    generated_grid_filepath = pathlib.Path(
        "AirToGroundSearch/wwwroot/outputs/GeneratedGrid/grid_world.csv"
    )
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
                "AirToGroundSearch/wwwroot/outputs/GeneratedGrid/grid_world_params.json"
            )
        )
    start = (0, 0)
    fuel = 900
    scanned_grid = grid.copy()
    scanned_grid = dijkstra_scan(
        grid, fuel, scanned_grid, Drone(grid, start_row, start_col)
    )
    print("Final scanned grid:")
    print(scanned_grid)
    print(f"Coverage: {calculate_coverage(scanned_grid, grid):.2f}%")

    # Ensure the output directory exists
    output_dir = "/workspaces/Team-I-Air-To-Ground-Search/AirToGroundSearch/wwwroot/outputs/GridResults/"
    os.makedirs(output_dir, exist_ok=True)

    # Save the scanned grid to a text file
    with open(f"{output_dir}results_d.txt", "w") as file:
        file.write("Final scanned grid:\n")
        np.savetxt(file, scanned_grid, delimiter=",", fmt="%d")
        file.write(f"\nCoverage: {calculate_coverage(scanned_grid, grid):.2f}%\n")

    # Save the scanned grid to a CSV file
    np.savetxt(f"{output_dir}results_d.csv", scanned_grid, delimiter=",", fmt="%d")

    # Save the grid visualization
    display_grid(
        f"{output_dir}results_d.csv",
        f"{output_dir}results_d.png",
    )

# TODO detect obstacles and avoid, improve logic behind path selection (Chosing the path with the most land to scan), prevent diagonal movement, make drone.py detect walls
# To run code be in /workspaces/Team-I-Ground-to-air-Search# python -m AirToGroundSearch.src.algorithms.d_search
