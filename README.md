# Team-I-Ground-to-air-Search

Will Weidler
Bailey Schoenike
Brennen Crawford
Donovan Bale
Lucas Wiley


Aircraft can be used for collecting information about the terrain it is flying over. This is commonly done
for search-and-rescue, geological surveys, infrastructure damage assessment, etc. In this project
students must come up with a route that an aircraft will fly over a geographic area to collect information.
Use a 2D grid world model. Some grid cells are traversable, some are not. The aircraft can move one grid
cell forward, move one grid cell left (a left turn), or move one grid cell right (a right turn). The aircraft
cannot move backwards to a grid cell behind it. The aircraft has a sensor that can scan a 2x3 rectangle of
cells ahead of it but the aircraft has a full map of the area prior to starting the flight. Figure 1 shows an
illustration of this grid world concept.
Generate a route that satisfies the movement constraints, avoids obstacles, minimizes the number of cell
movements, and scans at least 80% of all the grid cells. Note that the obstacles could be shaped such
that there are box canyons that the aircraft cannot turn around within. The algorithm must detect these
and avoid them.
Figure 1 Example Grid World
Possible stretch goals (pending team size, expected difficulty levels, student workloads, etc):
1. Create multiple competing heuristics and/or algorithms. Analyze which provides better results and
why.
2. New constraint: The aircraft can only move a total of X times. Maximize the grid world coverage
within this constraint.
3. What if we had two vehicles? Come up with routes that optimizes scanning the grid world using both
aircraft simultaneously.
4. Create a mechanism to visualize the problem and solution(s).


## How to Use
1. Install Docker Desktop
2. Launch Repo in VS Code
3. Re-open in container
4. Find Program.CS in the Air-To-Ground Directory
5. Click the play button in the top right
6. The web app should open in your default browser
