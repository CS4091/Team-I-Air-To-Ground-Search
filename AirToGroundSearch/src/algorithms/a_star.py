# import pandas as pd
from ..backend.graph import TwoDimGraph
import numpy as np
from heapq import heapify, heappush, heappop
from typing import Tuple
from collections import defaultdict
import math


def h(start_set, curr_set):
    pass


def a_star_search(
    grid: pd.DataFrame,
    start_index: Tuple[int, int],
    radar_range: Tuple[int, int],
    fuel_range: int,
    direction: int = 0,  # 0: N, 1: S, 2: E, 3: W
):
    start_row, start_col = start_index
    range_row, range_col = radar_range

    fuel_used = 0

    if direction > 1:
        range_row, range_col = range_col, range_row

    open_set: list[Tuple[int, int, int]] = [] 
    heapify(open_set)
    heappush(open_set, (start_row, start_col, direction, fuel_used))

    came_from: list[Tuple[int, int, int]] = []

    g_score = defaultdict(lambda: math.inf)
    g_score[start_index] = 0

    fscore = defaultdict(lambda: math.inf)
    fscore[start_index] = h(open_set[0], open_set[0])

    while open_set is not None:
        pass


if __name__ == "__main__":
    print("TEST")
