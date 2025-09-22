from __future__ import annotations

import math
import random
import time
from typing import List

from nqueens import Board, h_conflicts, random_board, random_neighbor

from .results import AlgoResult


def simulated_annealing(
    n: int,
    max_states: int,
    seed: int,
    T0: float = 1.0,
    alpha: float = 0.995,
    Tmin: float = 1e-4,
    record_history: bool = False,
) -> AlgoResult:
    rng = random.Random(seed)
    start_time = time.time()
    current = random_board(n, rng)
    current_h = h_conflicts(current)
    best = (current_h, current[:])
    states = 1
    history: List[int] = [current_h] if record_history else []

    T = T0 if T0 > 0 else 1.0
    while current_h > 0 and states < max_states and T > Tmin:
        nb = random_neighbor(current, rng)
        h = h_conflicts(nb)
        states += 1
        dE = h - current_h
        if dE <= 0 or rng.random() < math.exp(-dE / T):
            current = nb
            current_h = h
            if current_h < best[0]:
                best = (current_h, current[:])
        if record_history:
            history.append(current_h)
        T *= alpha

    end_time = time.time()
    final_h, final_board = best
    return AlgoResult(best_solution=final_board, H=final_h, states=states, time=end_time - start_time, history=history)
