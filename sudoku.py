import sys
import time

DIGITS = "123456789"

# squares are indexed 0..80, row-major
UNITLIST = (
    [[r * 9 + c for c in range(9)] for r in range(9)]
    + [[r * 9 + c for r in range(9)] for c in range(9)]
    + [[(br + r) * 9 + bc + c for r in range(3) for c in range(3)] for br in (0, 3, 6) for bc in (0, 3, 6)]
)
UNITS = [[u for u in UNITLIST if s in u] for s in range(81)]
PEERS = [set(sum(UNITS[s], [])) - {s} for s in range(81)]


def assign(values, s, d):
    if all(eliminate(values, s, d2) for d2 in values[s].replace(d, "")):
        return values
    return False


def eliminate(values, s, d):
    if d not in values[s]:
        return values
    values[s] = values[s].replace(d, "")
    if not values[s]:
        return False
    # naked single: s is down to one value, so no peer can have it
    if len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, p, d2) for p in PEERS[s]):
            return False
    # hidden single: if d now fits in only one place in a unit, put it there
    for unit in UNITS[s]:
        places = [p for p in unit if d in values[p]]
        if not places:
            return False
        if len(places) == 1 and not assign(values, places[0], d):
            return False
    return values


def parse(puzzle):
    chars = [c for c in puzzle if c in DIGITS or c in "0."]
    if len(chars) != 81:
        raise ValueError(f"expected 81 cells, got {len(chars)}")
    values = [DIGITS] * 81
    for s, c in enumerate(chars):
        if c in DIGITS and not assign(values, s, c):
            return False
    return values










