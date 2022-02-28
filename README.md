# Path-Finding-Visualizer
This is a path finding visualizer based on A* search algorithm , which is one of the best ways of finding a path in a graph.At each step the algorithm picks up the nodes with the smallest "F" value which itself is the sum of two other values "G" and "H".
G = it is the cost of moving from the starting index to the current index
H = it is the cost of getting from the current node to the final end node.

We can calculate G but how do we calculate H? 
There are two ways either we can calculate the exact value of H which will be time consuming, or we can work with the approximate values of H. In this implementation we have used Manhattan distance for approximate Heuristics.
####  h = abs (current_cell.x – goal.x) + abs (current_cell.y – goal.y)

## Snapshot of the application
![Path Finding Algorithm visualizer](https://user-images.githubusercontent.com/53488400/155970079-7a60969a-8221-4264-ae9f-1719a2272578.png)

