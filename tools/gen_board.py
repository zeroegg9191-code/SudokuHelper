#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate a valid jigsaw-sudoku board.

Strategy ("solve first, then melt"):
  1. build a random standard sudoku solution (rows / cols / boxes valid);
  2. start from the 3x3 box partition (a valid jigsaw partition);
  3. repeatedly pick two adjacent regions and randomly *re-partition* their
     18-cell union into two connected 9-cell sets that each contain 1-9.
     Validity is preserved by construction, shapes drift away from boxes.
  4. dig holes while keeping the solution unique.
"""
import json
import random
import sys
from collections import deque

N = 9
CELLS = [(r, c) for r in range(9) for c in range(9)]
NB = ((1, 0), (-1, 0), (0, 1), (0, -1))


def neighbours(r, c):
    for dr, dc in NB:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 9 and 0 <= nc < 9:
            yield nr, nc


def pat(r, c):
    return (3 * (r % 3) + r // 3 + c) % 9


def gen_solution(rng):
    digits = list(range(1, 10))
    rng.shuffle(digits)
    bands = [0, 1, 2]
    rng.shuffle(bands)
    rows = [b * 3 + i for b in bands for i in rng.sample([0, 1, 2], 3)]
    stacks = [0, 1, 2]
    rng.shuffle(stacks)
    cols = [s * 3 + i for s in stacks for i in rng.sample([0, 1, 2], 3)]
    raw = [[pat(r, c) for c in range(9)] for r in range(9)]
    return [[digits[raw[r][c]] for c in cols] for r in rows]


def connected_set(cells):
    cells = list(cells)
    if not cells:
        return False
    seen = {cells[0]}
    dq = deque([cells[0]])
    cs = set(cells)
    while dq:
        cr, cc = dq.popleft()
        for nr, nc in neighbours(cr, cc):
            if (nr, nc) in cs and (nr, nc) not in seen:
                seen.add((nr, nc))
                dq.append((nr, nc))
    return len(seen) == len(cs)


def repartition(rng, sol, union, original, min_diff=6):
    """split an 18-cell union into two connected 9-cell digit-complete halves"""
    union = set(union)
    seed = rng.choice(sorted(union))
    chosen = [seed]
    used = {sol[seed[0]][seed[1]]}
    budget = [8000]

    def dfs():
        budget[0] -= 1
        if budget[0] <= 0:
            return False
        if len(chosen) == 9:
            rest = union - set(chosen)
            return len(rest) == 9 and connected_set(rest) and len(set(chosen) ^ original) >= min_diff
        frontier = set()
        for cr, cc in chosen:
            for nr, nc in neighbours(cr, cc):
                p = (nr, nc)
                if p in union and p not in chosen and sol[nr][nc] not in used:
                    frontier.add(p)
        if not frontier:
            return False
        # reachable free area must still be large enough to finish a 9-cell set
        free = union - set(chosen)
        seen = set()
        dq = deque(sorted(frontier))
        seen |= set(dq)
        while dq:
            cr, cc = dq.popleft()
            for nr, nc in neighbours(cr, cc):
                p = (nr, nc)
                if p in free and p not in seen:
                    seen.add(p)
                    dq.append(p)
        if len(seen) < 9 - len(chosen):
            return False
        order = sorted(frontier)
        rng.shuffle(order)
        for p in order:
            v = sol[p[0]][p[1]]
            chosen.append(p)
            used.add(v)
            if dfs():
                return True
            used.discard(v)
            chosen.pop()
        return False

    if dfs():
        return set(chosen), union - set(chosen)
    return None


def region_cells(reg, k):
    return {(r, c) for r in range(9) for c in range(9) if reg[r][c] == k}


def neighbours_of_region(reg, k):
    """regions sharing an edge with region k, with shared edge length"""
    out = {}
    for r, c in region_cells(reg, k):
        for nr, nc in neighbours(r, c):
            j = reg[nr][nc]
            if j != k:
                out[j] = out.get(j, 0) + 1
    return out


def melt(rng, sol, iters=2200):
    reg = [[0] * 9 for _ in range(9)]
    for r in range(9):
        for c in range(9):
            reg[r][c] = (r // 3) * 3 + c // 3
    done = 0
    for _ in range(iters):
        k = rng.randrange(9)
        nb = neighbours_of_region(reg, k)
        if not nb:
            continue
        pool = []
        for j, w in nb.items():
            pool += [j] * w
        j = rng.choice(pool)
        union = region_cells(reg, k) | region_cells(reg, j)
        res = repartition(rng, sol, union, region_cells(reg, k))
        if res is None:
            continue
        a, b = res
        for r, c in a:
            reg[r][c] = k
        for r, c in b:
            reg[r][c] = j
        done += 1
    return reg, done


# ---------------- solver ----------------
def solve_count(grid, regions, limit=2):
    rows = [0] * 9
    cols = [0] * 9
    box = [0] * 9
    reg = [0] * 9
    for i, v in enumerate(grid):
        if v:
            r, c = divmod(i, 9)
            b = (r // 3) * 3 + c // 3
            bit = 1 << v
            rows[r] |= bit
            cols[c] |= bit
            box[b] |= bit
            reg[regions[i]] |= bit
    empty = [i for i, v in enumerate(grid) if not v]
    count = 0

    def rec(n):
        nonlocal count
        if count >= limit:
            return
        if n == len(empty):
            count += 1
            return
        best_i, best_mask, best_cnt = -1, 0, 10
        for idx in range(n, len(empty)):
            i = empty[idx]
            r, c = divmod(i, 9)
            b = (r // 3) * 3 + c // 3
            mask = ~(rows[r] | cols[c] | box[b] | reg[regions[i]]) & 0x3FE
            cnt = bin(mask).count("1")
            if cnt < best_cnt:
                best_i, best_mask, best_cnt = idx, mask, cnt
                if cnt <= 1:
                    break
        if best_cnt == 0:
            return
        empty[n], empty[best_i] = empty[best_i], empty[n]
        i = empty[n]
        r, c = divmod(i, 9)
        b = (r // 3) * 3 + c // 3
        mask = best_mask
        while mask:
            bit = mask & -mask
            mask ^= bit
            v = bit.bit_length() - 1
            rows[r] |= bit
            cols[c] |= bit
            box[b] |= bit
            reg[regions[i]] |= bit
            rec(n + 1)
            rows[r] ^= bit
            cols[c] ^= bit
            box[b] ^= bit
            reg[regions[i]] ^= bit
            if count >= limit:
                break
        empty[n], empty[best_i] = empty[best_i], empty[n]

    rec(0)
    return count


def make_puzzle(rng, sol, regions, target_givens=34):
    grid = [sol[r][c] for r in range(9) for c in range(9)]
    order = list(range(81))
    rng.shuffle(order)
    givens = 81
    for i in order:
        if givens <= target_givens:
            break
        keep = grid[i]
        grid[i] = 0
        if solve_count(grid, regions, limit=2) != 1:
            grid[i] = keep
        else:
            givens -= 1
    return grid, givens


def check(sol, reg):
    flat_sol = [sol[r][c] for r in range(9) for c in range(9)]
    flat_reg = [reg[r][c] for r in range(9) for c in range(9)]
    problems = []
    for k in range(9):
        cells = [i for i, v in enumerate(flat_reg) if v == k]
        if len(cells) != 9:
            problems.append("region %d has %d cells" % (k, len(cells)))
        if not connected_set([divmod(i, 9) for i in cells]):
            problems.append("region %d disconnected" % k)
        ds = {flat_sol[i] for i in cells}
        if len(ds) != 9:
            problems.append("region %d digits %s" % (k, sorted(ds)))
    for r in range(9):
        if len({sol[r][c] for c in range(9)}) != 9:
            problems.append("row %d" % r)
    for c in range(9):
        if len({sol[r][c] for r in range(9)}) != 9:
            problems.append("col %d" % c)
    for br in range(3):
        for bc in range(3):
            if len({sol[br * 3 + i][bc * 3 + j] for i in range(3) for j in range(3)}) != 9:
                problems.append("box %d%d" % (br, bc))
    return problems


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 20261121
    rng = random.Random(seed)
    sol = gen_solution(rng)
    reg, melted = melt(rng, sol)
    flat_sol = [sol[r][c] for r in range(9) for c in range(9)]
    flat_reg = [reg[r][c] for r in range(9) for c in range(9)]
    problems = check(sol, reg)
    print("melted steps:", melted, "problems:", problems, file=sys.stderr)
    puzzle, givens = make_puzzle(rng, sol, flat_reg, 34)
    print("givens:", givens, "solutions:", solve_count(puzzle, flat_reg, limit=3), file=sys.stderr)
    for r in range(9):
        print(" ".join(map(str, flat_sol[r * 9:(r + 1) * 9])), "   ",
              " ".join(map(str, flat_reg[r * 9:(r + 1) * 9])), file=sys.stderr)
    out = {
        "seed": seed,
        "solution": [flat_sol[r * 9:(r + 1) * 9] for r in range(9)],
        "regions": [flat_reg[r * 9:(r + 1) * 9] for r in range(9)],
        "puzzle": [puzzle[r * 9:(r + 1) * 9] for r in range(9)],
        "givens": givens,
    }
    with open("board.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False)


if __name__ == "__main__":
    main()


