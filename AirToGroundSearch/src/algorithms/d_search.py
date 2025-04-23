import numpy as np
import json
import heapq
import pathlib
import os
import time
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


def dijkstra_scan(grid: np.ndarray, fuel: int, scanned_grid: np.ndarray, drone: Drone):
    rows, cols = grid.shape
    start = (drone.row, drone.col)
    costs = np.full((rows, cols), np.inf)
    visited = np.zeros_like(grid, dtype=bool)
    queue = []
    start_direction = drone.direction
    heapq.heappush(queue, (0, start, start_direction))
    costs[start] = 0
    moves = 0
    fuel_used = 0
    paths_considered = 0
    start_time = time.time()

    while calculate_coverage(scanned_grid, grid) <= 80 and fuel_used < fuel:
        current_cost, (current_row, current_col), current_direction = heapq.heappop(queue)

        if visited[current_row, current_col]:
            continue

        visited[current_row, current_col] = True
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
            ):
                current_scanned_area = 0
                future_scanned_area = 0
                scanner_view = get_scanner_view(drone, neighbor_row, neighbor_col)

                for scan_row, scan_col in scanner_view:
                    if 0 <= scan_row < rows and 0 <= scan_col < cols:
                        if scanned_grid[scan_row, scan_col] == 0:
                            current_scanned_area += 1

                future_scanned_area = simulate_potential_coverage(drone, scanned_grid, rows, cols, sims=2)
                total_scanned_area = current_scanned_area + future_scanned_area
                new_cost = current_cost + 5 - total_scanned_area
                paths_considered += 1

                if new_cost < costs[neighbor_row, neighbor_col]:
                    costs[neighbor_row, neighbor_col] = new_cost
                    heapq.heappush(
                        queue, (new_cost, (neighbor_row, neighbor_col), direction)
                    )

            drone.row, drone.col = original_row, original_col
            drone.direction = original_direction
            scanned_grid[drone.row, drone.col] = 3

        fuel_used += 1

    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"Fuel used: {fuel_used}")
    print(f"Start Position: {start}")
    print(f"End Position: {drone.row} {drone.col}")
    print(f"Paths considered: {paths_considered}")
    print(f"Time: {elapsed_time:.2f} seconds")
    return scanned_grid


def simulate_potential_coverage(drone, scanned_grid, rows, cols, sims):   
    if sims == 0:
        return 0

    original_row, original_col = drone.row, drone.col
    original_direction = drone.direction
    total_coverage = 0

    for direction in [drone.direction, drone.turn_left(), drone.turn_right()]:
        drone.row, drone.col = original_row, original_col
        drone.direction = original_direction

        if direction == drone.direction:
            drone.move_straight()
        elif direction == drone.turn_left():
            drone.turn_left()
            drone.move_straight()
        elif direction == drone.turn_right():
            drone.turn_right()
            drone.move_straight()

        neighbor_row, neighbor_col = drone.row, drone.col

        scanner_view = get_scanner_view(drone, neighbor_row, neighbor_col)

        for scan_row, scan_col in scanner_view:
            if 0 <= scan_row < rows and 0 <= scan_col < cols:
                if scanned_grid[scan_row, scan_col] == 0:
                    total_coverage += 2


        total_coverage += simulate_potential_coverage(drone, scanned_grid, rows, cols, sims - 1)

    drone.row, drone.col = original_row, original_col
    drone.direction = original_direction

    return total_coverage

def get_scanner_view(drone, neighbor_row, neighbor_col):
    #Drone chooses based off info slightly outside scanner range
    if drone.direction == Direction.UP:
        return [
            (neighbor_row - 1, neighbor_col - 2), (neighbor_row - 1, neighbor_col - 1), (neighbor_row - 1, neighbor_col),
            (neighbor_row - 1, neighbor_col + 1), (neighbor_row - 1, neighbor_col + 2),
            (neighbor_row - 2, neighbor_col - 2), (neighbor_row - 2, neighbor_col - 1), (neighbor_row - 2, neighbor_col),
            (neighbor_row - 2, neighbor_col + 1), (neighbor_row - 2, neighbor_col + 2),
            (neighbor_row - 3, neighbor_col - 1), (neighbor_row - 3, neighbor_col), (neighbor_row - 3, neighbor_col + 1)
        ]
    elif drone.direction == Direction.DOWN:
        return [
            (neighbor_row + 1, neighbor_col - 2), (neighbor_row + 1, neighbor_col - 1), (neighbor_row + 1, neighbor_col),
            (neighbor_row + 1, neighbor_col + 1), (neighbor_row + 1, neighbor_col + 2),
            (neighbor_row + 2, neighbor_col - 2), (neighbor_row + 2, neighbor_col - 1), (neighbor_row + 2, neighbor_col),
            (neighbor_row + 2, neighbor_col + 1), (neighbor_row + 2, neighbor_col + 2),
            (neighbor_row + 3, neighbor_col - 1), (neighbor_row + 3, neighbor_col), (neighbor_row + 3, neighbor_col + 1)
        ]
    elif drone.direction == Direction.LEFT:
        return [
            (neighbor_row - 2, neighbor_col - 1), (neighbor_row - 1, neighbor_col - 1), (neighbor_row, neighbor_col - 1),
            (neighbor_row + 1, neighbor_col - 1), (neighbor_row + 2, neighbor_col - 1),
            (neighbor_row - 2, neighbor_col - 2), (neighbor_row - 1, neighbor_col - 2), (neighbor_row, neighbor_col - 2),
            (neighbor_row + 1, neighbor_col - 2), (neighbor_row + 2, neighbor_col - 2),
            (neighbor_row - 1, neighbor_col - 3), (neighbor_row, neighbor_col - 3), (neighbor_row + 1, neighbor_col - 3)
        ]
    elif drone.direction == Direction.RIGHT:
        return [
            (neighbor_row - 2, neighbor_col + 1), (neighbor_row - 1, neighbor_col + 1), (neighbor_row, neighbor_col + 1),
            (neighbor_row + 1, neighbor_col + 1), (neighbor_row + 2, neighbor_col + 1),
            (neighbor_row - 2, neighbor_col + 2), (neighbor_row - 1, neighbor_col + 2), (neighbor_row, neighbor_col + 2),
            (neighbor_row + 1, neighbor_col + 2), (neighbor_row + 2, neighbor_col + 2),
            (neighbor_row - 1, neighbor_col + 3), (neighbor_row, neighbor_col + 3), (neighbor_row + 1, neighbor_col + 3)
        ]

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
    fuel = 400
    scanned_grid = grid.copy()
    scanned_grid = dijkstra_scan(
        grid, fuel, scanned_grid, Drone(grid, start_row, start_col)
    )
    """print("Final scanned grid:")
    print(scanned_grid)"""
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

# TODO detect obstacles and avoid, possibly improve cost function to be based off more than just what's in scanner range