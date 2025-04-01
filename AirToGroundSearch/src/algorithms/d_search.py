import numpy as np
import heapq
from typing import Tuple

def dijkstra_scan(grid: np.ndarray, start: Tuple[int, int], fuel: int, scanned_grid: np.ndarray):
    rows, cols = grid.shape
    costs = np.full((rows, cols), np.inf)
    visited = np.zeros_like(grid, dtype=bool)
    queue = []
    heapq.heappush(queue, (0, start, (0, 1)))
    costs[start] = 0
    moves = 0

    while queue and moves < fuel:
        current_cost, (current_row, current_col), current_direction = heapq.heappop(queue)
        
        if visited[current_row, current_col]:
            continue

        visited[current_row, current_col] = True
        scanned_grid[current_row, current_col] += 2
        moves += 1

        forward = current_direction
        left = (-current_direction[1], current_direction[0])
        right = (current_direction[1], -current_direction[0])
        allowed_directions = [forward, left, right]

        for direction in allowed_directions:
            next_row, next_col = direction
            neighbor_row, neighbor_col = current_row + next_row, current_col + next_col

            if (0 <= neighbor_row < rows and
                0 <= neighbor_col < cols and
                not visited[neighbor_row, neighbor_col] and
                grid[neighbor_row, neighbor_col] != 1):

                new_cost = current_cost + 1 

                if new_cost < costs[neighbor_row, neighbor_col]:
                    costs[neighbor_row, neighbor_col] = new_cost
                    heapq.heappush(queue, (new_cost, (neighbor_row, neighbor_col), direction))
                    print(f"Moving to: ({neighbor_row}, {neighbor_col}), Facing: {direction}")
                    break
                
        print(scanned_grid)
    return scanned_grid

if __name__ == "__main__":
    grid = np.array([[0, 0, 0, 0],
                     [0, 1, 1, 0],
                     [0, 0, 0, 0],
                     [1, 1, 1, 0]])
    start = (0, 0)
    fuel = 5
    scanned_grid = grid.copy()
    scanned_grid = dijkstra_scan(grid, start, fuel, scanned_grid)

#TODO Add 2x3 scanner, detect obstacles and avoid, improve logic behind path selection (Chosing the path with the most land to scan)
