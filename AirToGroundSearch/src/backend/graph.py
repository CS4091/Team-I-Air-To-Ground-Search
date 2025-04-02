import numpy as np
import math
from typing import Iterable


class AdjMatrix:
    def __init__(self, n: int):
        self.adj_matrix: np.ndarray = np.zeros((n, n))

    def add_edge(self, u, v):
        self.adj_matrix[u][v] = 1

    def is_edge(self, u, v):
        return self.adj_matrix[u][v]


class TwoDimGraph:
    def __init__(self, m: int, n: int, vertices: np.typing.ArrayLike):
        self.adj_matrix = AdjMatrix(m * n)

        if m * n == len(vertices):
            self.vertices = np.array(vertices)

            for i in range(m * n):
                if i > 0:
                    self.adj_matrix.add_edge(i, i - 1)
                if i < m * n:
                    self.adj_matrix.add_edge(i, i + 1)
                if i + n < m * n:
                    self.adj_matrix.add_edge(i, i + n)
                if i - n > 0:
                    self.adj_matrix.add_edge(i, i - n)

            self.m = m
            self.n = n
        else:
            raise ValueError(
                f"Length of vertices ({len(vertices)}) doesn't match stated dimensions ({m}*{n})"
            )

    def get_flat_pos(self, i, j):
        return (self.m * i) + j

    def get_shape_position(self, k):
        return k // self.m, k % self.m

    def get_vertex(self, i, j):
        return self.vertices[self.get_flat_pos(i, j)]

    def get_neighbors(self, i, j):
        pos = self.get_flat_pos(i, j)
        neighbors = []
        for k in range(self.m * self.n):
            if self.adj_matrix.is_edge(pos, k):
                neighbors.append(self.get_shape_position(k))

        return neighbors
