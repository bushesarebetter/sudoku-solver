# Sudoku solver

A Sudoku solver in the style of Peter Norvig's essay. Constraint propagation does most of the work: naked singles remove a fixed digit from every peer, and hidden singles place a digit that fits in only one square of a unit. When that stalls, it backtracks on the square with the fewest candidates left. Plain Python, no dependencies.

[Setup](#setup) · [Run](#run) · [Puzzle set and timings](#puzzle-set-and-timings) · [Tests](#tests)

## Setup

Nothing to install beyond Python 3.8+ (and `pytest` for the tests).

## Run

```bash
python sudoku.py                 # solves puzzles.txt
python sudoku.py other.txt
```

The input file has one puzzle per line, 81 characters, with `.` or `0` for blanks. Lines starting with `#` are skipped. For each puzzle it prints the solution, the time taken and whether the result checks out, then a timing summary at the end.

## Puzzle set and timings

`puzzles.txt` has three easy puzzles, four well-known hard ones (Norvig's "hardest", Arto Inkala's 2012 puzzle, Easter Monster, Golden Nugget) and one with clashing givens. On my machine the easy ones take about 2 ms each, the hard ones 5 to 60 ms, and the broken one is rejected in under a millisecond.

## Tests

Install pytest before running the checks:

```bash
pip install pytest
```

```bash
python -m pytest -q
```

The tests check that every solution is a valid grid that keeps the original givens, and that both clashing givens and a square with no possible digit come back as "no solution".
