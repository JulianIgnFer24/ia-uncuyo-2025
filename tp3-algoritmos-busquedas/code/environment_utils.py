import random
from typing import List, Tuple, Optional


def generate_random_map_custom(size: int, p_frozen: float = 0.92,
                                rng: Optional[random.Random] = None) -> Tuple[List[str], Tuple[int, int], Tuple[int, int]]:
    """Generate a random FrozenLake map.

    Args:
        size: side length of the square grid.
        p_frozen: probability of a cell being frozen ("F"). The rest
            of the cells will be holes ("H").
        rng: optional instance of ``random.Random`` for reproducibility.

    Returns:
        A tuple with the description of the map as list of strings,
        the start coordinates and the goal coordinates.
    """
    if rng is None:
        rng = random.Random()

    grid = []
    for _ in range(size):
        row = []
        for _ in range(size):
            cell = 'F' if rng.random() < p_frozen else 'H'
            row.append(cell)
        grid.append(row)

    start = (rng.randrange(size), rng.randrange(size))
    goal = (rng.randrange(size), rng.randrange(size))
    while goal == start:
        goal = (rng.randrange(size), rng.randrange(size))

    grid[start[0]][start[1]] = 'S'
    grid[goal[0]][goal[1]] = 'G'

    desc = [''.join(row) for row in grid]
    return desc, start, goal


def print_map(desc: List[str]) -> None:
    """Print the map description in a human friendly way."""
    for row in desc:
        print(' '.join(row))

