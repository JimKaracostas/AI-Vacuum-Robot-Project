import copy # Library for deep copy of objects
import time # Library for measuring time

# PROBLEM WORLD
# [Robot Position, Trash Tile 1, Trash Tile 2, ..., Trash Tile 8, Base Position, Robot Load]
# Indices: 0 is Robot Pos, 1-8 are Tiles, 9 is Base Pos, 10 is Robot Load
initial_state = [3, 2, 3, 0, 0, 2, 0, 1, 2, 3, 0] # Initial State
final_state = [3, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0]   # Final State

# OPERATORS

# Collect trash
def collect_trash(state):
    # Check if robot can pick up trash (limit is 3)
    # state[state[0]] is the trash on the current tile
    # 3 - state[-1] is the available space in the robot
    if state[state[0]] > 3 - state[-1]:
        # Robot can only pick up what fits up to the limit of 3
        state[state[0]] = state[state[0]] - (3 - state[-1]) 
        state[-1] = 3 # Robot becomes full
    else: 
        # Robot picks up all trash from the current tile
        state[-1] = state[-1] + state[state[0]] 
        state[state[0]] = 0 # Tile becomes empty
    return state # Return new state

# Empty trash (only if robot is at base)
def empty_trash(state):
    # If robot is at base (state[0] == state[-2]) and has trash
    if state[0] == state[-2] and state[-1] > 0: 
        trash_on_floor = sum(state[1:9]) # Calculate total trash remaining on floor
        # Optimization: Empty only if full OR if no trash is left on floor (to finish)
        if state[-1] == 3 or trash_on_floor == 0: 
            state[-1] = 0 # Empty the robot
            return state # Return new state
            
    return None # Return None if action is not valid

# Move Left
def move_left(state):
    # Check if robot can move left (boundary check > 1)
    if state[0] > 1:
        # Move left
        state[0] = state[0] - 1
        # Collect trash if there is space
        if state[-1] < 3:
            state = collect_trash(state) # Update state after collection
        return state # Return new state
    return None # Return None if cannot move left

# Move Right
def move_right(state):
    # Check if robot can move right (boundary check < 8)
    if state[0] < 8:
        # Move right
        state[0] = state[0] + 1
        # Collect trash if there is space
        if state[-1] < 3:
            state = collect_trash(state) # Update state after collection
        return state # Return new state
    return None # Return None if cannot move right

# Find Children (Successors)
# (Each child results from applying an operator)
def find_children(state):
    # List of children nodes
    children = []
    
    # Create child by moving left
    left_state = copy.deepcopy(state)
    left_child = move_left(left_state)
    if left_child != None: 
        children.append(left_child)
    
    # Create child by moving right
    right_state = copy.deepcopy(state)
    right_child = move_right(right_state)
    if right_child != None:
        children.append(right_child)
        
    # Create child by emptying trash
    empty_trash_state = copy.deepcopy(state)
    empty_trash_child = empty_trash(empty_trash_state)
    if empty_trash_child != None:
        children.append(empty_trash_child)

    return children # Return list of children

# CREATE AND EXTEND QUEUE/FRONT
def make_queue(state, monitoring):
    # Initialize queue with initial state
    if monitoring == 'Y':
        # If monitoring, return list with one state
        return [state]
    else:
        # If not monitoring, return list of paths
        return [[state]]

# Expand Queue
def expand_queue(queue, method, goal_state):
    if method == 'DFS': # Expansion for DFS
        print("Queue:\n")
        print(queue)
        node = queue.pop(0) # Remove first path from queue
        queue_copy = copy.deepcopy(queue) 
        children = find_children(node[-1]) # Find children of the last node in path
        for child in children:
            path = copy.deepcopy(node)
            path.append(child)
            queue_copy.insert(0, path) # Insert new path at the START (LIFO)
            
    elif method == 'BFS': # Expansion for BFS
        print("Queue:\n")
        print(queue)
        node = queue.pop(0) # Remove first path from queue
        queue_copy = copy.deepcopy(queue)
        children = find_children(node[-1])
        for child in children:
            path = copy.deepcopy(node)
            path.append(child)
            queue_copy.append(path) # Insert new path at the END (FIFO)
            
    elif method == 'BESTFS': # Expansion for BestFS
        print("Queue:\n")
        print(queue)
        node = queue.pop(0)
        queue_copy = copy.deepcopy(queue)
        children = find_children(node[-1])
        for child in children:
            path = copy.deepcopy(node)
            path.append(child)
            queue_copy.append(path)
        # Sort queue based on cost (heuristic: sum of remaining trash on floor)
        # state[-1][1:9] represents the trash on tiles 1 to 8
        queue_copy.sort(key=lambda x: sum(x[-1][1:9]))

    return queue_copy # Return new queue

# CREATE AND EXTEND FRONT (Used for monitoring)
def make_front(state):
    return [state]

# Expand Front
def expand_front(front, method, goal_state):
    if method == 'DFS': 
        if front: 
            print("Front:\n")
            print(front)
            node = front.pop(0)
            for child in find_children(node):
                front.insert(0, child) 
    elif method == 'BFS': 
        if front: 
            print("Front:\n")
            print(front)
            node = front.pop(0)
            for child in find_children(node):
                front.append(child) 
    elif method == 'BESTFS': 
        if front: 
            print("Front:\n")
            print(front)
            node = front.pop(0)
            for child in find_children(node):
                front.append(child) 
            # Sort front based on cost
            front.sort(key=lambda x: sum(x[1:9])) 
    return front

# CHECK IF GOAL STATE
def is_goal(state, goal_state):
    return state == goal_state 

# FIND SOLUTION
def scoupa_find_solution(monitoring, initial_state, goal_state, method):
    start_time = time.time() 
    queue = [[initial_state]] 
    visited = set() 
    visited.add(str(initial_state)) 
    counter = 0 
    
    while queue: 
        path = queue.pop(0) # Pop first path
        state = path[-1] # Current state is the last in the path
        counter += 1 
        
        if monitoring == 'Y': 
            print(f"Step {counter}: | Expanding node: {state} \n") 
            print(state) 
            print("No solution found yet.\n") 
            
        if is_goal(state, goal_state): 
            print("Solution found:") 
            for step in path: 
                print(step) 
            if monitoring == 'Y': 
                print(f"Total steps: {counter} | Time: {time.time() - start_time} seconds") 
            return 
            
        children = find_children(state) 
        
        # If DFS, reverse children order before inserting.
        # This ensures the 'Left' child is popped first (LIFO stack logic).
        x_children = list(reversed(children)) if method == 'DFS' else children 
        
        for child in x_children: 
            if monitoring == 'Y': 
                print(f'Viewing child: {child}\n') 
                
            if str(child) not in visited: 
                visited.add(str(child)) # Mark as visited
                new_path = copy.deepcopy(path) 
                new_path.append(child) 
                
                if method == 'DFS': 
                    queue.insert(0, new_path) # Insert at start
                elif method == 'BFS': 
                    queue.append(new_path) # Insert at end
                elif method == 'BESTFS': 
                    queue.append(new_path) 
                    # Heuristic: Sort by remaining trash on the floor (indices 1 to 8)
                    queue.sort(key=lambda x: sum(x[-1][1:9]))            
    return None 

# Main Function
def main():
    method = input("Choose search method (DFS/BFS/BESTFS): \n").upper()
    while method not in ['DFS', 'BFS', 'BESTFS']:
        method = input("ENTER ONLY DFS, BFS or BESTFS: \n").upper()
        
    monitoring = input("Do you want to monitor the process step by step? (Y/N): \n").upper()
    while monitoring not in ['Y', 'N']:
        monitoring = input("ENTER ONLY Y or N: \n").upper()
        
    # [Pos, T1, T2, T3, T4, T5, T6, T7, T8, BasePos, Load]
    initial_state = [3, 2, 3, 0, 0, 2, 0, 1, 2, 3, 0] 
    goal_state = [3, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0] 

    scoupa_find_solution(monitoring, initial_state, goal_state, method) 

if __name__ == "__main__":
    main()
