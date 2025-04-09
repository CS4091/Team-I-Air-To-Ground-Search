from ..backend.graph import TwoDimGraph
from ..backend.csv_to_png import display_grid
import numpy as np
from heapq import heapify, heappush, heappop
from typing import Tuple, Literal
import pathlib

from collections import defaultdict
import math

Location = Tuple[int, int]

Direction = {"N": 1, "S": -1, "E": 1, "W": -1}


class Cell:
    @staticmethod
    def h(goal_condition, cells_explored):
        return goal_condition - cells_explored

    def __init__(
        self,
        current: Location,
        direction: Literal["N", "S", "E", "W"],
        goal_condition: int,
        g_score: float = math.inf,
        explored: set[Location] = set(),
        # navigated_to: list[Location] = [],
        # came_from: Location | None = None,
    ):
        self.m, self.n = current
        self.dir = direction
        # self.explored = explored
        # self.navigated_to = navigated_to
        # if came_from:
        #     self.navigated_to.append(came_from)
        self.goal_condition = goal_condition

        self.g_score = g_score

        self.f_score = self.h(goal_condition, len(explored))

    def __lt__(self, other):
        return self.f_score < other.f_score

    def __repr__(self):
        return (
            f"PriorityItem(f_score={self.f_score}, data=({self.m, self.n, self.dir}))"
        )

    def __eq__(self, other):
        if isinstance(other, Cell):
            return (self.m, self.n, self.dir, self.f_score) == (
                other.m,
                other.n,
                other.dir,
                other.f_score,
            )

    def __str__(self):
        return f"{self.m},{self.n},{self.dir},{self.f_score}"

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

    def update_scores(self, explored, g_score: float):
        self.g_score = g_score
        self.f_score = self.h(self.goal_condition, len(explored))

    def reached_goal(self, explored, goal_condition: float):
        return len(explored) >= goal_condition

    def scan_area(self, grid: TwoDimGraph, range_row: int, range_col: int):
        m, n, dir = self.m, self.n, self.dir
        explored = set()
        if dir == "N" or dir == "S":
            for j in range(n - (range_col // 2), n + (range_col // 2) + 1, Direction[dir]):
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
                for j in range(n + Direction[dir], n + (Direction[dir] * range_col), Direction[dir]):
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
    path
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
    goal_condition: int = 10,
):
    start_row, start_col = start_index
    range_row, range_col = radar_range
    goal_condition = (grid.grid_size() // 100) * goal_condition
    first = Cell(
        (start_row, start_col),
        direction,
        goal_condition,
        g_score=0,
    )

    open_set = []
    heapify(open_set)
    heappush(
        open_set,
        first,
    )

    open_set_lookup = set()
    open_set_lookup.add(first)

    came_from: dict[Cell, Cell] = {}
    explored: dict[Cell, set] = {first: set()}
    g_scores: dict[Cell, int] = {first: 0}

    best = first

    while open_set:
        # Pop cell of lowest fscore value
        current: Cell = heappop(open_set)
        open_set_lookup.remove(current)

        # Commence radar scan!
        new_explored = current.scan_area(grid, range_row, range_col)
        explored[current] = explored[current].union(new_explored)

        if current.f_score < best.f_score:
            best = current

        # Check if cell meets goal condition
        if current.reached_goal(explored[current], goal_condition):
            print(f"coverage: {(goal_condition / grid.grid_size()) * 100}")
            return backtrace_path(grid, current, came_from, explored[current])

        if current.g_score + 1 >= fuel_range:
            continue

        # Check neighbors
        # m, n, dir = current.m, current.n, current.dir
        for i, j in grid.get_neighbors(current.m, current.n):
            new_dir = current.get_dir_neighbor(i, j)
            new_g_score = current.g_score + 1
            # new_neighbor = (i, j, new_dir)
            new_neighbor = Cell(
                (i, j),
                new_dir,
                goal_condition,
                explored=explored[current],
                g_score=current.g_score + 1,
            )
            # Elimination conditions
            if new_neighbor in came_from or grid.is_val(i, j, 1):
                continue

            if new_neighbor not in g_scores or new_g_score < g_scores[new_neighbor]:
                g_scores[new_neighbor] = new_g_score
                came_from[new_neighbor] = current
                explored[new_neighbor] = explored[current]

                if new_neighbor not in open_set:
                    heappush(open_set, new_neighbor)
                    open_set_lookup.add(new_neighbor)

    backtrace_path(grid, best, came_from)
    return False


if __name__ == "__main__":
    print("TEST")
