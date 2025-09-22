from __future__ import annotations

import random
import time
from typing import List, Tuple

from nqueens import Board, h_conflicts, neighbor_move, random_board

from .results import AlgoResult


def hill_climbing(
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
    best_seen: Tuple[int, Board] = (current_h, current[:])
    history: List[int] = [current_h] if record_history else []

    while current_h > 0 and states < max_states:
        best_neighbor = None
        best_h = current_h
        for col in range(n):
            orig_row = current[col]
            for row in range(n):
                if row == orig_row:
                    continue
                nb = neighbor_move(current, col, row)
                h = h_conflicts(nb)
                states += 1
                if h < best_h:
                    best_h = h
                    best_neighbor = nb
                if states >= max_states:
                    break
            if states >= max_states:
                break

        if best_neighbor is None or best_h >= current_h:
            break
        current = best_neighbor
        current_h = best_h
        if record_history:
            history.append(current_h)
        if current_h < best_seen[0]:
            best_seen = (current_h, current[:])

    end_time = time.time()
    final_h, final_board = (current_h, current)
    if best_seen[0] < final_h:
        final_h, final_board = best_seen
    return AlgoResult(best_solution=final_board, H=final_h, states=states, time=end_time - start_time, history=history)
