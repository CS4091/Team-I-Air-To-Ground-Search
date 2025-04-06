
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import sys

def display_grid(grid, name):
    cmap = mcolors.ListedColormap(["black", "white", "red", "green", "purple"])
    bounds = [0, 1, 2, 3, 4]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)
    plt.imshow(grid, cmap=cmap, norm=norm)
    plt.axis("off")
    plt.savefig("./wwwroot/outputs/GeneratedGrid/" + name)

if __name__ == "__main__":
    filepath = sys.argv[1]
    name = sys.argv[2]
    grid = np.genfromtxt(filepath, delimiter=',')
    display_grid(grid, name)



