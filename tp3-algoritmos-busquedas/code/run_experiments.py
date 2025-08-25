import csv
import os
import time
from typing import List, Dict

from environment_utils import generate_random_map_custom
from search_algorithms import (
    random_search,
    bfs,
    dfs,
    dls,
    ucs,
    astar,
    cost_scenario2,
    heuristic_scenario2,
)


def evaluate():
    runs = 30
    size = 100
    p_frozen = 0.92
    max_steps = 1000
    results: List[Dict] = []
    for env_i in range(1, runs + 1):
        desc, start, goal = generate_random_map_custom(size, p_frozen)
        grid = [list(row) for row in desc]
        algorithms = {
            'RANDOM': lambda: random_search(grid, start, goal, max_steps),
            'BFS': lambda: bfs(grid, start, goal),
            'DFS': lambda: dfs(grid, start, goal),
            'DLS50': lambda: dls(grid, start, goal, 50),
            'DLS75': lambda: dls(grid, start, goal, 75),
            'DLS100': lambda: dls(grid, start, goal, 100),
            'UCS': lambda: ucs(grid, start, goal, cost_scenario2),
            'A*': lambda: astar(grid, start, goal, cost_scenario2, heuristic_scenario2),
        }
        for name, func in algorithms.items():
            start_time = time.time()
            path, explored = func()
            elapsed = time.time() - start_time
            solution_found = bool(path) and path[-1] == goal
            actions_count = len(path) - 1 if solution_found else 0
            actions_cost = 0
            if solution_found:
                for i in range(len(path) - 1):
                    step = (path[i + 1][0] - path[i][0], path[i + 1][1] - path[i][1])
                    actions_cost += cost_scenario2(step)
            results.append({
                'algorithm_name': name,
                'env_n': env_i,
                'states_n': explored,
                'actions_count': actions_count,
                'actions_cost': actions_cost,
                'time': elapsed,
                'solution_found': solution_found,
            })
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, '..', 'results.csv')
    fieldnames = [
        'algorithm_name',
        'env_n',
        'states_n',
        'actions_count',
        'actions_cost',
        'time',
        'solution_found',
    ]
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)
    print('Results saved to results.csv')


if __name__ == '__main__':
    evaluate()

