from backend.graph import TwoDimGraph
from backend.csv_to_png import display_grid
import numpy as np
from heapq import heapify, heappush, heappop
from typing import Tuple, Literal

# from collections import defaultdict
import math

Location = Tuple[int, int]

Direction = {"N": 1, "S": -1, "E": 1, "W": -1}


class Cell:
    @staticmethod
    def h(fuel_range, cells_explored):
        return fuel_range / cells_explored

    def __init__(
        self,
        current: Location,
        direction: Literal["N", "S", "E", "W"],
        fuel_range: int,
        g_score: float = math.inf,
        f_score: float = math.inf,
        explored: set[Location] = set(),
        # navigated_to: list[Location] = [],
        # came_from: Location | None = None,
    ):
        self.m, self.n = current
        self.dir = direction
        self.explored = explored
        # self.navigated_to = navigated_to
        # if came_from:
        #     self.navigated_to.append(came_from)
        self.fuel_range = fuel_range

        self.g_score = g_score

        if not self.explored:
            self.f_score = f_score
        else:
            self.f_score = g_score + self.h(fuel_range, len(self.explored))

    def __lt__(self, other):
        return self.f_score < other.f_score

    def __repr__(self):
        return (
            f"PriorityItem(f_score={self.f_score}, data=({self.m, self.n, self.dir}))"
        )

    def __eq__(self, other):
        if isinstance(other, Cell):
            return (self.m, self.n, self.dir) == (other.m, other.n, other.dir) and len(
                self.explored
            ) == len(other.explored)

    def add_explored(self, i: int, j: int):
        self.explored.add((i, j))

    def get_dir_neighbor(self, i, j):
        if self.m - i > 0 and self.n - j == 0:
            return "N"
        elif self.m - i < 0 and self.n - j == 0:
            return "S"
        elif self.m - i == 0 and self.n - j > 0:
            return "E"
        elif self.m - i == 0 and self.n - j < 0:
            return "W"

    def update_scores(self, g_score: float):
        self.g_score = g_score
        self.f_score = self.h(self.fuel_range, len(self.explored))

    def reached_goal(self, grid_size: int, goal_condition: float):
        return len(self.explored) >= grid_size * goal_condition

    def scan_area(self, grid: TwoDimGraph, range_row: int, range_col: int):
        m, n, dir = self.m, self.n, self.dir
        if dir == "N" or dir == "S":
            for j in range(n - (range_col // 2), n + (range_col // 2) + 1):
                for i in range(
                    m + Direction[dir], m + (range_row * Direction[dir]) + 1
                ):
                    if (i, j) in self.explored or i >= grid.m or j >= grid.n:
                        continue
                    self.add_explored(i, j)
                    if grid.is_val(i, j, 1):
                        break
        else:
            for i in range(m - (range_row // 2), m + (range_row // 2) + 1):
                for j in range(n + Direction[dir], n + (Direction[dir] * range_col)):
                    if (i, j) in self.explored or i >= grid.m or j >= grid.n:
                        continue
                    self.add_explored(i, j)
                    if grid.is_val(i, j, 1):
                        break


def backtrace_path(grid: TwoDimGraph, current: Cell, came_from: dict):
    output_grid = np.array(grid.vertices).reshape(grid.shape())
    for location in current.explored:
        i, j = location
        output_grid[i][j] = 2
    path = []
    cell_key = (current.m, current.n, current.dir)

    while cell_key in came_from:
        path.append((cell_key[0], cell_key[1]))
        cell_key = came_from[cell_key]
    path.reverse()
    for i, j in path:
        output_grid[i][j] = 3

    if path:
        start_m, start_n = path[0]
        output_grid[start_m][start_n] = 4

    display_grid(output_grid, name=f"a_star_search.csv")
    return True


def a_star_search(
    grid: TwoDimGraph,
    start_index: Tuple[int, int],
    radar_range: Tuple[int, int],
    fuel_range: int,
    direction: Literal["N", "S", "E", "W"] = "N",  # N, S, E, W
    goal_condition: float = 0.8,
):
    start_row, start_col = start_index
    range_row, range_col = radar_range

    open_set = []
    heapify(open_set)
    heappush(
        open_set,
        Cell(
            (start_row, start_col),
            direction,
            fuel_range,
            g_score=0,
        ),
    )

    open_set_lookup = set()
    open_set_lookup.add((start_row, start_col, direction))

    came_from = {}
    g_scores = {(start_row, start_col, direction): 0}

    while open_set:
        # Pop cell of lowest fscore value
        current: Cell = heappop(open_set)
        open_set_lookup.remove((current.m, current.n, current.dir, len(current.explored)))

        # Commence radar scan!
        current.scan_area(grid, range_row, range_col)

        # Check if cell meets goal condition
        if current.reached_goal(grid.grid_size(), goal_condition):
            return backtrace_path(grid, current, came_from)

        if current.g_score + 1 >= fuel_range:
            continue

        # Check neighbors
        # m, n, dir = current.m, current.n, current.dir
        for i, j in grid.get_neighbors(current.m, current.n):
            new_dir = current.get_dir_neighbor(i, j)
            new_g_score = current.g_score + 1
            neighbor_key = (i, j, new_dir)
            # Elimination conditions
            if neighbor_key in came_from or grid.is_val(i, j, 1):
                continue

            if neighbor_key not in g_scores or new_g_score < g_scores[neighbor_key]:
                g_scores[neighbor_key] = new_g_score
                came_from[neighbor_key] = (current.m, current.n)
                new_neighbor = Cell(
                    (i, j),
                    new_dir,
                    fuel_range,
                    explored=current.explored.copy(),
                    g_score=current.g_score + 1,
                )

                if new_neighbor not in open_set:
                    heappush(open_set, new_neighbor)
                    open_set_lookup.add(neighbor_key)

    return False


if __name__ == "__main__":
    print("TEST")
