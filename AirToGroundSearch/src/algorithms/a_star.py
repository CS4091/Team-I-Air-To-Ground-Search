import pandas as pd
import heapq
from typing import Tuple
from enum import Enum
from datetime import time, timedelta
from collections import defaultdict
import math


def h(x, y, g_x, g_y):
    # Heuristic cost-estimation function
    # returns the straight-line distance between the goal and current node
    return math.sqrt((g_x - x) ** 2 + (g_y - y) ** 2)

def is_valid(range_row, range_col):
    return range_row >= 0 and range_col >= 0

def is_unblocked(grid, row, col):
    return grid[row][col] == 0

def is_destination(row, col, goal_coords):
    return row == goal_coords[0] and col == goal_coords[1]



def a_star_search(
    grid: pd.DataFrame,
    start_index: Tuple[int, int],
    radar_range: Tuple[int, int],
    goal_coords: Tuple[int, int],
    direction: int = 0,  # 0: N, 1: S, 2: E, 3: W
):
    start_row, start_col = start_index
    range_row, range_col = radar_range
    goal_row, goal_col = goal_coords
    found_destination = False

    if direction > 1:
        range_row, range_col = range_col, range_row

    if not is_unblocked(grid, start_row, start_col) or not is_unblocked(grid, goal_row, goal_col):
        print("Start or goal is blocked")
        return

    open_set: list[Tuple[int, int, int]] = [(start_row, start_col, direction)]

    came_from: list[Tuple[int, int, int]] = []

    while open_set is not None:
        current = heapq.heappop(open_set)
        current_row, current_col, current_dir = current

        if current_row == goal_row and current_col == goal_col:
            found_destination = True
            break

        for i in range(4):
            new_row, new_col = current_row, current_col
            if i == 0: #N
                new_row += 1
            elif i == 1: #S
                new_row -= 1
            elif i == 2: #E
                new_col += 1
            else: #W
                new_col -= 1

            if is_valid(new_row, new_col) and is_unblocked(grid, new_row, new_col) and not came_from[new_row][new_col]:
                heapq.heappush(open_set, (new_row, new_col, i))
                came_from.append((new_row, new_col, i))

    g_score = defaultdict(lambda: math.inf)
    g_score[start_index] = 0

    fscore = defaultdict(lambda: math.inf)
    fscore[start_index] = h(start_row, start_col, goal_row, goal_col)

    while open_set is not None:
        pass


print("TEST")
