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


def search(values):
    if values is False:
        return False
    if all(len(v) == 1 for v in values):
        return values
    # minimum remaining values: branch on the most constrained square
    s = min((s for s in range(81) if len(values[s]) > 1), key=lambda s: len(values[s]))
    for d in values[s]:
        result = search(assign(values.copy(), s, d))
        if result:
            return result
    return False


def solve(puzzle):
    """Return the solution as an 81-char string, or None if there isn't one."""
    result = search(parse(puzzle))
    return "".join(result) if result else None


def is_valid(solution, puzzle):
    if solution is None or len(solution) != 81:
        return False
    givens = [c for c in puzzle if c in DIGITS or c in "0."]
    if any(g in DIGITS and g != v for g, v in zip(givens, solution)):
        return False
    return all(sorted(solution[s] for s in u) == list(DIGITS) for u in UNITLIST)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "puzzles.txt"
    puzzles = [ln.strip() for ln in open(path) if ln.strip() and not ln.startswith("#")]

    times = []
    for i, puzzle in enumerate(puzzles, 1):
        t0 = time.perf_counter()
        solution = solve(puzzle)
        dt = time.perf_counter() - t0
        times.append(dt)
        print(f"#{i:<2} {puzzle}")
        if solution:
            print(f"    {solution}  {dt * 1000:7.2f} ms  {'ok' if is_valid(solution, puzzle) else 'INVALID'}")
        else:
            print(f"    no solution  {dt * 1000:.2f} ms")
    print(f"\n{len(times)} puzzles, total {sum(times):.3f} s, "
          f"avg {sum(times) / len(times) * 1000:.2f} ms, max {max(times) * 1000:.2f} ms")


if __name__ == "__main__":
    main()
