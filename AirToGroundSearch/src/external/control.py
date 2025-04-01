import numpy as np
import pathlib
import random
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from drone import Drone, read_grid_from_csv, find_start_coordinate, print_grid_with_drone, update_scanned_grid, calculate_coverage

def manual_control(drone, stuck_grid, grid, scanned_grid):
    """
    Allows manual control of the drone.
    The drone navigates using the stuck_grid but scans tiles in the original grid.
    """
    while True:
        update_scanned_grid(drone, grid, scanned_grid)  # Use original grid for scanning
        print_grid_with_drone(stuck_grid, drone)  # Use stuck_grid for navigation
        print(f"Drone current position: {drone.get_position()}, facing {drone.direction.name}")
        coverage = calculate_coverage(scanned_grid, grid)
        print(f"Coverage: {coverage:.2f}%")
        if coverage >= 80:
            break
        command = input("Enter command (S for straight, L for left, R for right, Q to quit): ").strip().upper()
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
    coverage = calculate_coverage(scanned_grid, grid)
    print(f"Final Coverage: {coverage:.2f}%")

def random_movement(drone, stuck_grid, grid, scanned_grid, max_moves):
    moves = 0
    while moves < max_moves:
        update_scanned_grid(drone, grid, scanned_grid)  # Use original grid for scanning
        print_grid_with_drone(stuck_grid, drone)  # Use stuck_grid for navigation
        print(f"Drone current position: {drone.get_position()}, facing {drone.direction.name}")
        coverage = calculate_coverage(scanned_grid, grid)
        print(f"Coverage: {coverage:.2f}%")
        if coverage >= 80:
            break

        move = random.choice(["S", "L", "R"])
        if move == "S":
            drone.move_straight()
        elif move == "L":
            drone.turn_left()
        elif move == "R":
            drone.turn_right()

        moves += 1

    print("Drone final position:", drone.get_position())
    coverage = calculate_coverage(scanned_grid, grid)
    print(f"Final Coverage: {coverage:.2f}%")

def identify_stuck_points(grid):
    """
    Identifies points in the grid where the drone can get stuck (e.g., 1-wide tunnels or dead ends).
    Returns a new grid where stuck points are treated as obstacles.
    """
    stuck_grid = grid.copy()  # Create a copy of the grid to mark stuck points

    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] == 0:  # Only consider navigable points
                # Count the number of navigable neighbors (0s)
                neighbors = 0
                if i > 0 and grid[i - 1, j] == 0:  # Up
                    neighbors += 1
                if i < rows - 1 and grid[i + 1, j] == 0:  # Down
                    neighbors += 1
                if j > 0 and grid[i, j - 1] == 0:  # Left
                    neighbors += 1
                if j < cols - 1 and grid[i, j + 1] == 0:  # Right
                    neighbors += 1

                # If the cell has 1 or fewer navigable neighbors, it's a stuck point
                if neighbors <= 1:
                    stuck_grid[i, j] = 1  # Mark as an obstacle

    return stuck_grid

def update_grid(grid, scanned_grid):
    cmap = mcolors.ListedColormap(["black", "white", "red", "purple", "green"])
    bounds = [0, 1, 2, 3, 4]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)
  
    for i in range(scanned_grid.shape[0]):
        for j in range(scanned_grid.shape[1]):
            if scanned_grid[i, j] == 1:
                grid[i, j] = 3

    plt.imshow(grid, cmap=cmap, norm=norm)
    plt.axis("off")
    plt.savefig("./wwwroot/outputs/GeneratedGrid/grid_world.png")


if __name__ == "__main__":
    grid_filepath = pathlib.Path("AirToGroundSearch/wwwroot/outputs/GeneratedGrid/grid_world.csv")
    grid = read_grid_from_csv(grid_filepath)
    stuck_grid = identify_stuck_points(grid)

    scanned_grid = np.zeros_like(grid)

    start_row, start_col = find_start_coordinate(stuck_grid)
    drone = Drone(stuck_grid, start_row, start_col)

    print("Select mode:")
    print("1. Manual Control")
    print("2. Random Movement")
    mode = input("Enter mode number: ").strip()

    if mode == "1":
        manual_control(drone, stuck_grid, grid, scanned_grid)
    elif mode == "2":
        max_moves = int(input("Enter the maximum number of moves: ").strip())
        random_movement(drone, stuck_grid, grid, scanned_grid, max_moves)
    else:
        print("Invalid mode selected.")
    update_grid(grid, scanned_grid)