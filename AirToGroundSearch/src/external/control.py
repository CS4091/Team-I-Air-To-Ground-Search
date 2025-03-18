import numpy as np
import pathlib
import random
from drone import Drone, read_grid_from_csv, find_start_coordinate, print_grid_with_drone, update_scanned_grid, calculate_coverage

def manual_control(drone, grid, scanned_grid):
    while True:
        update_scanned_grid(drone, scanned_grid)
        print_grid_with_drone(grid, drone)
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

def random_movement(drone, grid, scanned_grid, max_moves):
    moves = 0
    while moves < max_moves:
        update_scanned_grid(drone, scanned_grid)
        #print_grid_with_drone(grid, drone)
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

if __name__ == "__main__":
    grid_filepath = pathlib.Path("AirToGroundSearch/wwwroot/outputs/GeneratedGrid/grid_world.csv")
    grid = read_grid_from_csv(grid_filepath)
    scanned_grid = np.zeros_like(grid)

    start_row, start_col = find_start_coordinate(grid)
    drone = Drone(grid, start_row, start_col)

    print("Select mode:")
    print("1. Manual Control")
    print("2. Random Movement")
    mode = input("Enter mode number: ").strip()

    if mode == "1":
        manual_control(drone, grid, scanned_grid)
    elif mode == "2":
        max_moves = int(input("Enter the maximum number of moves: ").strip())
        random_movement(drone, grid, scanned_grid, max_moves)
    else:
        print("Invalid mode selected.")