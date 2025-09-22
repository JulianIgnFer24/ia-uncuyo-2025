from __future__ import annotations

from dataclasses import dataclass
from typing import List

from nqueens import Board


@dataclass
class AlgoResult:
    """Container with the outcome of a search run."""

    best_solution: Board
    H: int
    states: int
    time: float
    history: List[int]
