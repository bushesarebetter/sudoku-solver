from pathlib import Path

from sudoku import is_valid, parse, solve

PUZZLES = [
    ln.strip()
    for ln in (Path(__file__).parent / "puzzles.txt").read_text().splitlines()
    if ln.strip() and not ln.startswith("#")
]
SOLVABLE = PUZZLES[:-1]


def test_solutions_are_valid_and_keep_givens():
    for p in SOLVABLE:
        s = solve(p)
        assert is_valid(s, p), p


def test_easy_puzzle_needs_no_search():
    values = parse(PUZZLES[0])
    assert all(len(v) == 1 for v in values)


def test_known_solution():
    assert solve(PUZZLES[0]) == (
        "483921657967345821251876493548132976729564138"
        "136798245372689514814253769695417382"
    )


def test_conflicting_givens_have_no_solution():
    assert solve(PUZZLES[-1]) is None


def test_dead_cell_has_no_solution():
    # givens never clash directly, but the top-left cell has no candidate left
    p = ".12345678" + "9" + "." * 71
    assert solve(p) is None


def test_is_valid_catches_tampering():
    p = SOLVABLE[0]
    s = solve(p)
    swapped = s[1] + s[0] + s[2:]
    assert not is_valid(swapped, p)
