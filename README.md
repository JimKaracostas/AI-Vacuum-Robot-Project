# AI Vacuum Robot Agent

An Artificial Intelligence project implementing a vacuum cleaner robot agent that navigates a 1D corridor environment to clean trash using various search algorithms.

## 📌 Overview

The goal of the robot is to clean all trash distributed across 8 tiles and return to its base station empty. The project demonstrates the implementation and comparison of three fundamental search algorithms:
* **DFS** (Depth-First Search)
* **BFS** (Breadth-First Search)
* **BestFS** (Best-First Search)

## 🌍 Problem World & State Representation

The world consists of a corridor with 8 tiles. The state is represented by a list of 11 integers:

`[RobotPos, T1, T2, T3, T4, T5, T6, T7, T8, BasePos, Load]`

* **RobotPos (Index 0):** Current position of the robot (1-8).
* **T1 - T8 (Indices 1-8):** Amount of trash on each of the 8 tiles.
* **BasePos (Index 9):** Position of the base station (fixed at 3).
* **Load (Index 10):** Current amount of trash carried by the robot (Max capacity = 3).

**Initial State:** `[3, 2, 3, 0, 0, 2, 0, 1, 2, 3, 0]`
**Goal State:** `[3, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0]`

## ⚙️ Implementation Details

### Operators
1.  **Move Left/Right:** Moves the robot to adjacent tiles. It automatically collects trash from the new tile if capacity allows.
2.  **Collect Trash:** Logic embedded in movement. The robot picks up trash until it hits capacity (3).
3.  **Empty Trash:** Can only be performed at the Base Station (Tile 3).
    * *Optimization:* The robot only empties if it is completely full (3/3) OR if there is no trash left on the floor (to allow finishing).

### Algorithms & Heuristics
* **DFS:** Implemented using a LIFO approach. Children are reversed before insertion to ensure Left-to-Right tree traversal.
* **BFS:** Implemented using a FIFO approach. Finds the optimal solution in terms of steps (levels), though not necessarily the fastest execution time.
* **BestFS:** Uses a heuristic function $h(n)$.
    * **Heuristic $h(n)$:** The sum of all remaining trash on the floor (indices 1-8). The algorithm prioritizes states where the environment is cleaner.

### Cycle Prevention
A `visited` set is used to store state strings, preventing the robot from entering infinite loops.

## 🚀 How to Run

### Prerequisites
* Python 3.x

### Execution
Run the script via terminal:

```bash
python vacuum_robot.py
