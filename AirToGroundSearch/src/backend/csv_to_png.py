
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import sys

def display_grid(csv_filepath, end_filepath):
    grid = np.genfromtxt(csv_filepath, delimiter=',')
    cmap = mcolors.ListedColormap(["black", "white", "red", "green", "purple"])
    bounds = [0, 1, 2, 3, 4, 5]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)
    plt.imshow(grid, cmap=cmap, norm=norm)
    plt.axis("off")
    plt.savefig(end_filepath)

if __name__ == "__main__":
    filepath = sys.argv[1]
    end_filepath = sys.argv[2]
    display_grid(filepath, end_filepath)



