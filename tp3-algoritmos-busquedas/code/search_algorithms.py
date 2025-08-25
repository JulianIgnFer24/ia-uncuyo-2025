from collections import deque
import heapq
import random
from typing import Dict, List, Optional, Tuple, Set

Action = Tuple[int, int]
State = Tuple[int, int]
Grid = List[List[str]]

# Actions: up, right, down, left
actions: List[Action] = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def get_neighbors(state: State, grid: Grid) -> List[Tuple[State, Action]]:
    """Return reachable neighbor states and the action taken to reach them."""
    neighbors: List[Tuple[State, Action]] = []
    n = len(grid)
    for action in actions:
        nx, ny = state[0] + action[0], state[1] + action[1]
        if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] != 'H':
            neighbors.append(((nx, ny), action))
    return neighbors


def reconstruct_path(parent: Dict[State, Optional[State]], start: State, goal: State) -> List[State]:
    if goal not in parent:
        return []
    path = [goal]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path


def random_search(grid: Grid, start: State, goal: State, max_steps: int = 1000,
                   rng: Optional[random.Random] = None) -> Tuple[List[State], int]:
    """Perform a random walk until the goal is found or the step limit is reached."""
    if rng is None:
        rng = random.Random()
    current = start
    path = [start]
    visited: Set[State] = {start}
    for _ in range(max_steps):
        if current == goal:
            return path, len(visited)
        neighbors_list = [n for n, _ in get_neighbors(current, grid)]
        if not neighbors_list:
            break
        current = rng.choice(neighbors_list)
        path.append(current)
        visited.add(current)
    return [], len(visited)


def bfs(grid: Grid, start: State, goal: State) -> Tuple[List[State], int]:
    queue = deque([start])
    parent: Dict[State, Optional[State]] = {start: None}
    states_explored = 0
    while queue:
        state = queue.popleft()
        states_explored += 1
        if state == goal:
            break
        for neighbor, _ in get_neighbors(state, grid):
            if neighbor not in parent:
                parent[neighbor] = state
                queue.append(neighbor)
    path = reconstruct_path(parent, start, goal)
    return path, states_explored


def dfs(grid: Grid, start: State, goal: State) -> Tuple[List[State], int]:
    stack: List[State] = [start]
    parent: Dict[State, Optional[State]] = {start: None}
    visited: Set[State] = set()
    states_explored = 0
    while stack:
        state = stack.pop()
        if state in visited:
            continue
        visited.add(state)
        states_explored += 1
        if state == goal:
            break
        for neighbor, _ in reversed(get_neighbors(state, grid)):
            if neighbor not in parent:
                parent[neighbor] = state
            stack.append(neighbor)
    path = reconstruct_path(parent, start, goal)
    return path, states_explored


def dls(grid: Grid, start: State, goal: State, limit: int) -> Tuple[List[State], int]:
    stack: List[Tuple[State, int]] = [(start, 0)]
    parent: Dict[State, Optional[State]] = {start: None}
    visited: Set[State] = set()
    states_explored = 0
    while stack:
        state, depth = stack.pop()
        if state in visited:
            continue
        visited.add(state)
        states_explored += 1
        if state == goal:
            break
        if depth < limit:
            for neighbor, _ in reversed(get_neighbors(state, grid)):
                if neighbor not in parent:
                    parent[neighbor] = state
                stack.append((neighbor, depth + 1))
    path = reconstruct_path(parent, start, goal)
    return path, states_explored


def cost_scenario1(_: Action) -> int:
    return 1


def cost_scenario2(action: Action) -> int:
    if action in [(0, -1), (0, 1)]:
        return 1
    return 10


def ucs(grid: Grid, start: State, goal: State, cost_fn) -> Tuple[List[State], int]:
    frontier: List[Tuple[int, State]] = [(0, start)]
    parent: Dict[State, Optional[State]] = {start: None}
    cost_so_far: Dict[State, int] = {start: 0}
    states_explored = 0
    visited: Set[State] = set()
    while frontier:
        cost, state = heapq.heappop(frontier)
        if state in visited:
            continue
        visited.add(state)
        states_explored += 1
        if state == goal:
            break
        for neighbor, action in get_neighbors(state, grid):
            new_cost = cost + cost_fn(action)
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                parent[neighbor] = state
                heapq.heappush(frontier, (new_cost, neighbor))
    path = reconstruct_path(parent, start, goal)
    return path, states_explored


def heuristic_scenario2(state: State, goal: State) -> int:
    vertical = abs(goal[0] - state[0]) * 10
    horizontal = abs(goal[1] - state[1]) * 1
    return vertical + horizontal


def astar(grid: Grid, start: State, goal: State, cost_fn, heuristic_fn) -> Tuple[List[State], int]:
    frontier: List[Tuple[int, int, State]] = [(heuristic_fn(start, goal), 0, start)]
    parent: Dict[State, Optional[State]] = {start: None}
    cost_so_far: Dict[State, int] = {start: 0}
    states_explored = 0
    visited: Set[State] = set()
    while frontier:
        f, g, state = heapq.heappop(frontier)
        if state in visited:
            continue
        visited.add(state)
        states_explored += 1
        if state == goal:
            break
        for neighbor, action in get_neighbors(state, grid):
            new_g = g + cost_fn(action)
            if neighbor not in cost_so_far or new_g < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_g
                parent[neighbor] = state
                heapq.heappush(frontier, (new_g + heuristic_fn(neighbor, goal), new_g, neighbor))
    path = reconstruct_path(parent, start, goal)
    return path, states_explored

