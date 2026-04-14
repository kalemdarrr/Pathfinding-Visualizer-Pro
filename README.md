# Pathfinding Visualizer Pro 

A modern, highly professional desktop application built with Python and Pygame. This application dynamically visualizes popular pathfinding and graph search algorithms in real-time, allowing users to draw barriers, set targets, and watch algorithms navigate the grid layer by layer.

 Features
- **Clean & Modern UI**: Designed with a sharp, card-based interface, clear layouts, and professional aesthetic tones.
- **Real-Time Visualization**: Watch search algorithms step through and evaluate the grid natively with controlled animations.
- **Interactive Map**: Draw and erase your very own walls/barriers and assign start/end coordinates on the fly using mouse controls.

  Implemented Algorithms
- **Breadth-First Search (BFS)**: Explores equally in all directions. *Guarantees the shortest path.*
- **Depth-First Search (DFS)**: Exhausts individual paths by exploring as deeply as possible before backtracking. *Does not guarantee the shortest path.*
- **Dijkstra's Algorithm**: A weighted search algorithm determining best routes based on distance. In this unweighted grid environment, it inherently behaves like BFS and *Guarantees the shortest path.*

 Installation & Usage

1. Prerequisites
You need to have Python 3 installed. Clone this repository locally:
```bash
git clone https://github.com/kalemdarrr/Pathfinding-Visualizer-Pro.git
cd Pathfinding-Visualizer-Pro
```

 2. Install Dependencies
Install the required Pygame graphical library using pip:
```bash
pip install -r requirements.txt
```

 3. Run the Application
Launch the visualizer directly from your terminal:
```bash
python main.py
```

 Desktop Controls

 Mouse Inputs
- **First Left Click**: Set Start Node (Green)
- **Second Left Click**: Set End Node (Red)
- **Other Left Clicks (Hold & Drag)**: Draw Barriers/Obstacles (Dark Gray)
- **Right Click (Hold & Drag)**: Erase Grid Cells

### Keyboard Shortcuts
- `1` : Select Breadth-First Search (BFS)
- `2` : Select Depth-First Search (DFS)
- `3` : Select Dijkstra's Search
- **`SPACE`** : **Start Algorithm Simulation**
- **`C`** : **Clear Entire Grid**
