from __future__ import annotations

import math
import random
import time
from typing import List, Optional

from nqueens import Board, h_conflicts, random_board, random_neighbor

from .results import AlgoResult


def random_search(
    n: int,
    max_states: int,
    seed: int,
    record_history: bool = False,
) -> AlgoResult:
    rng = random.Random(seed)
    start_time = time.time()
    current = random_board(n, rng)
    current_h = h_conflicts(current)
    states = 1
    best_h = current_h
    best_b: Optional[Board] = current[:]
    history: List[int] = []
    if record_history:
        history.append(current_h)

    while best_h > 0 and states < max_states:
        nb = random_neighbor(current, rng)
        h = h_conflicts(nb)
        states += 1
        if record_history:
            history.append(h)
        if h < best_h:
            best_h = h
            best_b = nb[:]
        current = nb
        if h == 0:
            break

    end_time = time.time()
    assert best_b is not None
    return AlgoResult(best_solution=best_b, H=best_h, states=states, time=end_time - start_time, history=history)
