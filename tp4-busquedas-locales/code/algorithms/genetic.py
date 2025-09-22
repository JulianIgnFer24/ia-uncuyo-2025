from __future__ import annotations

import random
import time
from typing import List, Optional, Tuple

from nqueens import Board, h_conflicts

from .results import AlgoResult


def _pmx(parent1: Board, parent2: Board, rng: random.Random) -> Tuple[Board, Board]:
    size = len(parent1)
    p1, p2 = parent1[:], parent2[:]
    c1, c2 = [-1] * size, [-1] * size
    a, b = sorted(rng.sample(range(size), 2))
    c1[a : b + 1] = p1[a : b + 1]
    c2[a : b + 1] = p2[a : b + 1]

    def fill(child: Board, donor: Board, start: int, end: int) -> None:
        for i in range(start, end + 1):
            val = donor[i]
            if val not in child:
                pos = i
                while True:
                    mapped = p1[pos] if donor is p2 else p2[pos]
                    if mapped not in child:
                        pos = p2.index(mapped) if donor is p2 else p1.index(mapped)
                    else:
                        break
                child[pos] = val
        for i in range(size):
            if child[i] == -1:
                child[i] = donor[i]

    fill(c1, p2, a, b)
    fill(c2, p1, a, b)
    return c1, c2


def genetic_algorithm(
    n: int,
    max_states: int,
    seed: int,
    pop_size: int = 100,
    tournament_k: int = 3,
    crossover_rate: float = 0.9,
    mutation_rate: float = 0.2,
    elitism: int = 2,
    max_generations: Optional[int] = None,
    record_history: bool = False,
) -> AlgoResult:
    rng = random.Random(seed)
    start_time = time.time()
    population: List[Board] = []
    for _ in range(pop_size):
        b = list(range(n))
        rng.shuffle(b)
        population.append(b)

    def fitness(b: Board) -> int:
        return -h_conflicts(b)

    states = 0
    fits = [fitness(ind) for ind in population]
    states += len(population)
    best_idx = max(range(pop_size), key=lambda i: fits[i])
    best = (-fits[best_idx], population[best_idx][:])
    history: List[int] = [best[0]] if record_history else []

    generation = 0
    while best[0] > 0 and states < max_states and (max_generations is None or generation < max_generations):
        generation += 1

        elite_indices = sorted(range(pop_size), key=lambda i: fits[i], reverse=True)[:elitism]
        new_population = [population[i][:] for i in elite_indices]

        def select_one() -> Board:
            cand = rng.sample(range(pop_size), tournament_k)
            best_i = max(cand, key=lambda i: fits[i])
            return population[best_i][:]

        while len(new_population) < pop_size:
            p1 = select_one()
            p2 = select_one()
            if rng.random() < crossover_rate:
                c1, c2 = _pmx(p1, p2, rng)
            else:
                c1, c2 = p1[:], p2[:]
            for child in (c1, c2):
                if rng.random() < mutation_rate:
                    i, j = rng.sample(range(n), 2)
                    child[i], child[j] = child[j], child[i]
                new_population.append(child)
                if len(new_population) >= pop_size:
                    break

        population = new_population
        fits = [fitness(ind) for ind in population]
        states += len(population)
        best_idx = max(range(pop_size), key=lambda i: fits[i])
        cand_h = -fits[best_idx]
        if cand_h < best[0]:
            best = (cand_h, population[best_idx][:])
        if record_history:
            history.append(best[0])

    end_time = time.time()
    return AlgoResult(best_solution=best[1], H=best[0], states=states, time=end_time - start_time, history=history)
