from ..backend.graph import TwoDimGraph
from ..backend.csv_to_png import display_grid
import numpy as np
from heapq import heapify, heappush, heappop
from typing import Tuple, Literal
import pathlib
import time

from collections import defaultdict
import math

Location = Tuple[int, int]

Direction = {"N": 1, "S": -1, "E": 1, "W": -1}


def h(cell_cov_goal, num_cells_explored, range_m, range_n, fuel_range, fuel_used):
    m = range_m + 1
    if range_n // 2 <= m:
        a = range_n // 2 + 1
        b = range_n // 2
    else:
        a = m
        b = m

    max_coverage_per_cell = range_m * range_n - a * b
    movements_left = fuel_range - fuel_used
    cells_needed = cell_cov_goal - num_cells_explored

    cost = cells_needed / max_coverage_per_cell

    if cost > movements_left:
        return math.inf

    return cost


class Cell:

    def __init__(
        self,
        current: Location,
        direction: Literal["N", "S", "E", "W"],
        heuristic_cost: int | float = math.inf,
        g_score: float = math.inf,
        fuel_used: int = 0,
        # navigated_to: list[Location] = [],
        # came_from: Location | None = None,
    ):
        self.m, self.n = current
        self.dir = direction
        # self.explored = explored
        # self.navigated_to = navigated_to
        # if came_from:
        #     self.navigated_to.append(came_from)

        self.fuel_used = fuel_used

        self.g_score = g_score

        self.f_score = self.g_score + heuristic_cost

    def __lt__(self, other):
        if isinstance(other, Cell):
            return self.f_score < other.f_score
        else:
            return False

    def __repr__(self):
        return f"PriorityItem(f_score={self.f_score}, g_score=({self.g_score}), data=({self.m, self.n, self.dir}))"

    def __eq__(self, other):
        if isinstance(other, Cell):
            return (self.m, self.n, self.dir, other.g_score, self.f_score) == (
                other.m,
                other.n,
                other.dir,
                other.g_score,
                other.f_score,
            )

    def __str__(self):
        return f"{self.m},{self.n},{self.dir},{self.g_score:.7f},{self.f_score:.7f}"

    def __hash__(self):
        return hash(str(self))

    # def add_explored(self, i: int, j: int):
    #     self.explored.add((i, j))

    def get_dir_neighbor(self, i, j):
        if self.m - i > 0 and self.n - j == 0:
            return "N"
        elif self.m - i < 0 and self.n - j == 0:
            return "S"
        elif self.m - i == 0 and self.n - j > 0:
            return "E"
        elif self.m - i == 0 and self.n - j < 0:
            return "W"

    def update_scores(self, g_score: float, heuristic_cost):
        self.g_score = g_score
        self.f_score = g_score + heuristic_cost

    def reached_goal(self, explored, goal_condition: float):
        return len(explored) >= goal_condition

    def scan_area(self, grid: TwoDimGraph, range_row: int, range_col: int):
        m, n, dir = self.m, self.n, self.dir
        explored = set()
        if dir == "N" or dir == "S":
            for j in range(
                n - (range_col // 2), n + (range_col // 2) + 1, Direction[dir]
            ):
                for i in range(
                    m + Direction[dir], m + (range_row * Direction[dir]) + 1
                ):
                    if i < 0 or i >= grid.m or j < 0 or j >= grid.n:
                        continue
                    explored.add((i, j))
                    if grid.is_val(i, j, 1):
                        break
        else:
            for i in range(m - (range_row // 2), m + (range_row // 2) + 1):
                for j in range(
                    n + Direction[dir], n + (Direction[dir] * range_col), Direction[dir]
                ):
                    if i < 0 or i >= grid.m or j < 0 or j >= grid.n:
                        continue
                    explored.add((i, j))
                    if grid.is_val(i, j, 1):
                        break
        return explored


def backtrace_path(grid: TwoDimGraph, current: Cell, came_from: dict, explored):
    output_grid = np.array(grid.vertices).reshape(grid.shape())
    for i, j in explored:
        output_grid[i][j] = 2
    path = []

    cell_key = current
    while cell_key in came_from:
        path.append(cell_key)
        cell_key = came_from[cell_key]

    for cell in path:
        i, j = cell.m, cell.n
        output_grid[i][j] = 3

    if path:
        start_m, start_n = path[0].m, path[0].n
        output_grid[start_m][start_n] = 4

    workspace_path = pathlib.Path(__file__).parent.parent.parent
    np.savetxt(
        pathlib.Path(
            workspace_path / "wwwroot/outputs/GridResults/results_a.csv"
        ).resolve(),
        output_grid,
        delimiter=",",
        fmt="%d",
    )
    display_grid(
        pathlib.Path(
            workspace_path / "wwwroot/outputs/GridResults/results_a.csv"
        ).resolve(),
        pathlib.Path(workspace_path / "wwwroot/outputs/GridResults/results_a.png"),
    )
    return True


def a_star_search(
    grid: TwoDimGraph,
    start_index: Tuple[int, int],
    radar_range: Tuple[int, int],
    fuel_range: int,
    direction: Literal["N", "S", "E", "W"] = "N",  # N, S, E, W
    goal_percent: int = 80,
):
    start_time = time.time() 

    start_row, start_col = start_index
    range_row, range_col = radar_range
    goal_condition = int((grid.n_count(0) / 100) * goal_percent)
    first = Cell(
        (start_row, start_col),
        direction,
        heuristic_cost=h(goal_condition, 0, range_row, range_col, fuel_range, 0),
        g_score=0,
    )

    print(
        "Scannable cells:",
        grid.n_count(0),
        f", Coverage Condition: {goal_condition} cells",
    )

    open_set = []
    heapify(open_set)
    heappush(
        open_set,
        first,
    )

    open_set_lookup = set()
    open_set_lookup.add(first)

    came_from: dict[Cell, Cell | None] = defaultdict(lambda: None)
    explored: dict[Cell, set] = {first: set()}
    g_scores: dict[Cell, int] = {first: 0}

    best = first

    paths_considered = 1

    while open_set:
        # Pop cell of lowest fscore value
        current: Cell = heappop(open_set)
        open_set_lookup.remove(current)

        # Commence radar scan!
        new_explored = current.scan_area(grid, range_row, range_col)
        explored[current] = explored[current].union(new_explored)

        if len(explored[current]) > len(explored[best]):
            # print("Current Best Path:", current, len(explored[current]))
            best = current

        # Check if cell meets goal condition
        if current.reached_goal(explored[current], goal_condition):
            end_time = time.time()
            total_time = end_time - start_time
            print(f"fuel used: {current.fuel_used}")
            print(
                f"start position: ({first.m},{first.n},{first.dir}), end position: ({current.m},{current.n},{current.dir})"
            )
            print(f"paths considered: {paths_considered}")
            print(f"time elapsed: {total_time:.2f}s")
            print(f"coverage: {len(explored[current])}")
            return backtrace_path(grid, current, came_from, explored[current])

        if current.fuel_used + 1 >= fuel_range:
            continue

        # Check neighbors
        # m, n, dir = current.m, current.n, current.dir
        for index, (i, j) in enumerate(grid.get_neighbors(current.m, current.n)):
            new_dir = current.get_dir_neighbor(i, j)
            new_fuel_used = current.fuel_used + 1
            new_g_score = new_fuel_used / len(explored[current])
            # new_neighbor = (i, j, new_dir)
            new_neighbor = Cell(
                (i, j),
                new_dir,
                g_score=new_g_score,
                fuel_used=new_fuel_used,
                heuristic_cost=h(
                    goal_condition,
                    len(explored[current]),
                    range_row,
                    range_col,
                    fuel_range,
                    new_fuel_used,
                ),
            )
            # Elimination conditions
            prev_m, prev_n = (
                (came_from[current].m, came_from[current].m)
                if came_from[current]
                else (math.nan, math.nan)
            )

            if (
                (new_neighbor.m, new_neighbor.n) == (prev_m, prev_n)
                or grid.is_val(i, j, 1)
                or new_neighbor.f_score == math.inf
            ):
                continue

            if new_neighbor not in g_scores or new_g_score < g_scores[new_neighbor]:
                g_scores[new_neighbor] = new_g_score
                came_from[new_neighbor] = current
                explored[new_neighbor] = explored[current]

                if new_neighbor not in open_set:
                    heappush(open_set, new_neighbor)
                    open_set_lookup.add(new_neighbor)
                    if index > 0:
                        paths_considered += 1

    backtrace_path(grid, best, came_from)
    return False


if __name__ == "__main__":
    print("TEST")
