# Path-Visualizer
A pathfinding algorithm visualizer made with Python and Pygame

## Inspiration
I was studying various pathfinding algorithms as a part of my 5th semester B-tech subject Artificial Intelligence. But I did not have any hands-on lab to try out those algorithms and analyze the results. So I decided to build this application that visualizes them on three different sized grids with custom maze.

## How I made it 
I used a simple python game development module called Pygame to design the GUI. Then I created 3 square grids of size
1. 20 x 20 (small)
2. 28 x 28 (standard)
3. 35 x 35 (large)

After that, I designed the wall, start and goal node distinctions and implemented the following algorithms:

- Depth First Search
- Breadth First Search
- Bidirectional Search (non heuristic)
- Dijkstra's Algorithm 
- Greedy Best First Search (heuristic)
- A* search  (heuristic)
- Bidirectional Greedy Best First Search  (heuristic)
- Bidirectional A* search  (heuristic)

For the heuristic function, I chose the Manhattan Distance.
Assumption : Each node in the grid can be traversed only Left, Right, Up and Down. No diagonal movement is allowed

## How to run
There are three ways to run the application. Download the files as zip or clone the directory, then follow any of the three processes
 
1. Install Python 3 and download Pygame as  `pip install pygame`. Then run the `main.py` file as `python main.py` 
2. On a Windows PC double click on the `Visualizer.exe` file 
3. On a Windows PC install the `setup.exe`file and then execute the `Visualizer.exe` file from the installed directory

## Instructions 
All these application related Instructions can be found inside the `info` tab on the app main menu.

Left Click on a node to make it Start, Goal or Wall. The first clicked node will be set to Start, the next one will be set to Goal. After that the clicked nodes will be set to Walls. 
Right Click on a node to clear it.

 ![Start](https://via.placeholder.com/15/FE9801/000000?text=+) Start Node
 ![Goal](https://via.placeholder.com/15/CC0E74/000000?text=+) Goal Node
 ![Path](https://via.placeholder.com/15/0A043C/000000?text=+) Path Node
 ![Wall](https://via.placeholder.com/15/808080/000000?text=+) Wall Node
 ![Traversable](https://via.placeholder.com/15/FDCFDF/000000?text=+) Traversable Node
 ![Start](https://via.placeholder.com/15/16A596/000000?text=+) Open Node
 ![Start](https://via.placeholder.com/15/AEE6E6/000000?text=+) Closed Node

Press The ARROW UP or ARROW LEFT key to decrease the grid size.
Press The ARROW DOWN or ARROW RIGHT key to increase the grid size.
Press The SPACE key to start the algorithm.
Press The R key to clear the grid.
Press The ESC key to return to main menu.

## Demo
<img src="https://github.com/trinonandi/Path-Visualizer/blob/master/md_assets/demo.gif" width="500" height="500" />
