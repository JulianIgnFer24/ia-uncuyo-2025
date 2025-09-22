import random
from typing import List, Tuple


Board = List[int]


def random_board(n: int, rng: random.Random) -> Board:
    """Return a random permutation board of size n (one queen per column and row)."""
    b = list(range(n))
    rng.shuffle(b)
    return b


def h_conflicts(board: Board) -> int:
    """Objective function H: number of attacking pairs of queens.

    board[c] = row index of queen in column c.
    Count pairs (i, j), i < j, that are in same row or same diagonal.
    """
    n = len(board)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j]:
                conflicts += 1
            elif abs(i - j) == abs(board[i] - board[j]):
                conflicts += 1
    return conflicts


def neighbor_move(board: Board, col: int, new_row: int) -> Board:
    """Return a new board with queen in column `col` moved to `new_row`."""
    nboard = board.copy()
    nboard[col] = new_row
    return nboard


def random_neighbor(board: Board, rng: random.Random) -> Board:
    n = len(board)
    c = rng.randrange(n)
    r = rng.randrange(n)
    # ensure a different row
    if r == board[c]:
        r = (r + 1) % n
    return neighbor_move(board, c, r)


def is_solution(board: Board) -> bool:
    return h_conflicts(board) == 0

