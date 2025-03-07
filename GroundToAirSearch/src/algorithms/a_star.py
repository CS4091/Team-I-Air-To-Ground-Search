import pandas as pd
from typing import Tuple
from enum import Enum
from datetime import time, timedelta
from collections import defaultdict
import math


def h(x, y, g_x, g_y):
    # Heuristic cost-estimation function
    # returns the straight-line distance between the goal and current node
    return math.sqrt((g_x - x)**2 + (g_y - y)**2)
    


def a_star_search(
    grid: pd.DataFrame,
    start_index: Tuple[int, int],
    radar_range: Tuple[int, int],
    goal_coords: Tuple[int, int],
    direction: int = 0, # 0: N, 1: S, 2: E, 3: W
):
    start_row, start_col = start_index
    range_row, range_col = radar_range
    goal_row, goal_col = goal_coords

    if direction > 1:
        range_row, range_col = range_col, range_row

    open_set: list[Tuple[int, int, int]] = [(start_row, start_col, direction)]

    came_from: list[Tuple[int, int, int]] = []

    g_score = defaultdict(lambda: math.inf)
    g_score[start_index] = 0

    fscore = defaultdict(lambda: math.inf)
    fscore[start_index] = h(start_row, start_col, goal_row, goal_col)

    while open_set is not None:
        pass