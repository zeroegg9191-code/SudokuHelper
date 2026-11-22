#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the UI mockup screens (HTML) for the jigsaw-sudoku platform."""
import base64
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAL = [("#FFC9C9", "#D25C5C"), ("#FFD8A8", "#C77424"), ("#F7E68E", "#A08A1E"),
       ("#C4E8AC", "#578741"), ("#AEE3D6", "#2E8175"), ("#BED4F7", "#4468AE"),
       ("#CFC2F6", "#6450AC"), ("#EAC2EF", "#8B4FA5"), ("#F8BBD5", "#A94672")]
CNAME = ["珊瑚红", "杏橙", "芥末黄", "草绿", "青碧", "天蓝", "靛紫", "紫罗兰", "樱粉"]
INK = "#232A3C"

CSS = r"""
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff}
body{font-family:"Microsoft YaHei UI","Microsoft YaHei","Segoe UI",system-ui,sans-serif;
  -webkit-font-smoothing:antialiased;color:#161B2E}
.screen{position:relative;overflow:hidden;background:#F4F6FB;display:flex;flex-direction:column}
.card{background:#fff;border:1px solid #ECEEF5;border-radius:16px;
  box-shadow:0 1px 2px rgba(16,24,40,.04),0 10px 28px -12px rgba(16,24,40,.16)}
.muted{color:#7A8296}
.title{font-size:13px;font-weight:600;color:#161B2E;letter-spacing:.2px}

/* ---------- app bar ---------- */
.appbar{height:58px;flex:0 0 58px;background:#fff;border-bottom:1px solid #EDEFF6;
  display:flex;align-items:center;padding:0 20px;gap:14px}
.logo{width:30px;height:30px;border-radius:9px;background:linear-gradient(140deg,#6366F1,#8B5CF6);
  display:grid;grid-template-columns:repeat(3,3px);grid-gap:2.5px;place-content:center;
  box-shadow:0 4px 10px -3px rgba(99,102,241,.6)}
.logo i{width:3px;height:3px;border-radius:1px;background:#fff;display:block;opacity:.95}
.brand{font-size:15px;font-weight:700;letter-spacing:.4px}
.brand small{font-size:9.5px;font-weight:600;color:#9AA1B4;letter-spacing:1.4px;margin-left:7px;
  text-transform:uppercase;vertical-align:2px}
.tabs{display:flex;background:#F1F3F8;border-radius:10px;padding:3px;margin-left:6px}
.tab{font-size:12.5px;color:#6B7280;padding:5px 13px;border-radius:8px;font-weight:500}
.tab.on{background:#fff;color:#3F3FD1;font-weight:600;box-shadow:0 1px 3px rgba(16,24,40,.12)}
.spacer{flex:1}
.chip{display:flex;align-items:center;gap:7px;height:30px;padding:0 11px;border-radius:9px;
  background:#F5F6FB;border:1px solid #ECEEF5;font-size:12px;color:#3D4457;font-weight:500}
.chip .dot{width:8px;height:8px;border-radius:3px;background:linear-gradient(140deg,#7C3AED,#EC4899)}
.timer{display:flex;align-items:center;gap:6px;font-size:13px;font-weight:600;color:#161B2E;
  font-variant-numeric:tabular-nums;letter-spacing:.4px;padding:0 4px}
.iconbtn{width:30px;height:30px;border-radius:9px;border:1px solid #ECEEF5;background:#fff;
  display:grid;place-items:center;color:#5B6376}
.avatar{width:30px;height:30px;border-radius:50%;background:linear-gradient(140deg,#F0ABFC,#818CF8);
  display:grid;place-items:center;color:#fff;font-size:11.5px;font-weight:700}

/* ---------- layout ---------- */
.body{flex:1;display:flex;gap:18px;padding:20px 22px}
.col{display:flex;flex-direction:column;gap:16px}
.pad{padding:15px 16px}

/* ---------- board ---------- */
.board-card{padding:16px 16px 14px}
.board-row{display:flex;gap:14px}
.board{position:relative;flex:0 0 auto;border-radius:3px;overflow:hidden;background:#fff;
  box-shadow:0 2px 6px rgba(16,24,40,.10)}
.cell{position:absolute;background-color:#fff}
.cell.peer{background-image:linear-gradient(rgba(79,70,229,.045),rgba(79,70,229,.045))}
.cell.same{background-image:linear-gradient(rgba(79,70,229,.13),rgba(79,70,229,.13))}
.cell.bad{background-image:linear-gradient(rgba(239,68,68,.17),rgba(239,68,68,.17))}
.cell.void{background-color:#F7F8FC}
svg.lines{position:absolute;left:0;top:0;pointer-events:none}
.val{position:absolute;display:grid;place-items:center;font-weight:600;color:#1B2030;
  font-variant-numeric:tabular-nums;line-height:1}
.val.user{color:#3B5BDB;font-weight:600}
.val.bad{color:#DC2626}
.val.faint{color:#B7BECF;font-weight:500}
.notes{position:absolute;display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(3,1fr);
  padding:2px;color:#94A0B8;font-weight:600;line-height:1}
.notes span{display:grid;place-items:center}
.sel{position:absolute;border:2.6px solid #4F46E5;border-radius:6px;z-index:6;
  box-shadow:0 0 0 3px rgba(79,70,229,.15)}
.hint{position:absolute;border:2px dashed #F59E0B;border-radius:7px;z-index:5}
.brush{position:absolute;border:2.5px solid #F59E0B;border-radius:6px;z-index:6;
  box-shadow:0 0 0 4px rgba(245,158,11,.18)}

/* legend */
.legend{flex:1;display:flex;flex-direction:column;gap:4px;min-width:0}
.legend .hd{font-size:10px;color:#9AA1B4;font-weight:600;letter-spacing:1px;margin-bottom:3px}
.lg{display:flex;align-items:center;gap:7px;height:26px;padding:0 6px;border-radius:7px}
.lg .sw{width:13px;height:13px;border-radius:4px;flex:0 0 auto}
.lg .nm{font-size:10.5px;font-weight:600;color:#3D4457;white-space:nowrap}
.lg .ct{font-size:9.5px;color:#9AA1B4;margin-left:auto;font-variant-numeric:tabular-nums}

/* status strip */
.status{display:flex;align-items:center;gap:10px;margin-top:12px;font-size:11.5px;color:#6B7280}
.bar{flex:1;height:6px;border-radius:3px;background:#EEF0F6;overflow:hidden}
.bar i{display:block;height:100%;border-radius:3px;background:linear-gradient(90deg,#6366F1,#8B5CF6)}
.pill{display:flex;align-items:center;gap:5px;height:22px;padding:0 8px;border-radius:6px;
  background:#F5F6FB;border:1px solid #ECEEF5;font-size:11px;font-weight:500;color:#4B5265}
.pill.red{background:#FEF2F2;border-color:#FEE2E2;color:#DC2626}
.pill.green{background:#F0FDF4;border-color:#DCFCE7;color:#15803D}
.pill.amber{background:#FFFBEB;border-color:#FEF3C7;color:#B45309}

/* stats */
.stats{display:flex;gap:0}
.stat{flex:1;padding:2px 4px}
.stat .k{font-size:10px;color:#9AA1B4;font-weight:600;letter-spacing:.6px}
.stat .v{font-size:19px;font-weight:700;letter-spacing:.2px;font-variant-numeric:tabular-nums;margin-top:3px}
.stat .v small{font-size:10.5px;color:#9AA1B4;font-weight:600;margin-left:2px}

/* keypad */
.grid-nine{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.key{height:52px;border-radius:11px;border:1px solid #ECEEF5;background:#FCFCFE;
  display:flex;align-items:center;justify-content:center;position:relative}
.key b{font-size:21px;font-weight:600;color:#1B2030}
.key em{position:absolute;right:7px;bottom:4px;font-size:9px;font-style:normal;color:#A6AEC0;font-weight:600}
.key.done b{color:#C6CCDA}
.key.done{background:#F7F8FC}

/* tools */
.tools{display:grid;grid-template-columns:repeat(6,1fr);gap:6px;margin-top:10px}
.tool{height:52px;border-radius:10px;display:flex;flex-direction:column;align-items:center;
  justify-content:center;gap:4px;color:#5B6376;background:#F8F9FC;border:1px solid #EFF1F7}
.tool span{font-size:9.5px;font-weight:500;letter-spacing:.2px}
.tool.on{background:#EEF0FF;border-color:#DDE0FF;color:#4F46E5}

/* ai card */
.ai{display:flex;flex-direction:column;flex:1;padding:0;overflow:hidden;
  background:linear-gradient(165deg,#FFFFFF 0%,#FBFAFF 60%,#F7F5FF 100%);border-color:#EAE7FB}
.ai .hd{display:flex;align-items:center;gap:8px;padding:13px 15px 0}
.spark{width:22px;height:22px;border-radius:7px;background:linear-gradient(140deg,#6366F1,#A855F7);
  display:grid;place-items:center;color:#fff;box-shadow:0 3px 8px -2px rgba(124,58,237,.55)}
.ai .hd .t{font-size:12.5px;font-weight:700}
.ai .hd .s{font-size:9.5px;color:#9AA1B4;font-weight:500;margin-top:1px}
.tech{display:inline-flex;align-items:center;gap:5px;height:21px;padding:0 8px;border-radius:6px;
  background:#EEF0FF;color:#4F46E5;font-size:10px;font-weight:600;letter-spacing:.2px}
.quote{font-size:11.5px;line-height:1.75;color:#3D4457;margin-top:8px}
.quote b{color:#4F46E5;font-weight:700}
.ai .btns{display:flex;gap:7px;margin-top:auto;padding-top:10px}
.chain{margin-top:11px;border-top:1px dashed #E7E3F7;padding-top:9px}
.chain-hd{font-size:9px;letter-spacing:1.2px;color:#A2A9BC;font-weight:700;margin-bottom:6px}
.chain-row{display:flex;gap:7px;font-size:10.5px;color:#5B6376;line-height:1.55;margin-bottom:5px}
.chain-row i{flex:0 0 auto;width:15px;height:15px;border-radius:50%;background:#EEF0FF;color:#4F46E5;
  font-style:normal;font-size:8.5px;font-weight:700;display:grid;place-items:center;margin-top:1px}
.btn{height:32px;border-radius:9px;display:flex;align-items:center;justify-content:center;
  font-size:11.5px;font-weight:600;gap:5px}
.btn.primary{background:linear-gradient(140deg,#6366F1,#7C3AED);color:#fff;flex:1;
  box-shadow:0 5px 14px -6px rgba(99,102,241,.9)}
.btn.ghost{border:1px solid #E4E6F0;background:#fff;color:#4B5265;padding:0 12px}

/* editor */
.steps{display:flex;align-items:center;gap:0;padding:0 2px}
.step{display:flex;align-items:center;gap:6px;font-size:10.5px;color:#98A0B3;font-weight:600}
.step .n{width:17px;height:17px;border-radius:50%;border:1.4px solid #D7DBE6;display:grid;
  place-items:center;font-size:9.5px;color:#98A0B3;background:#fff}
.step.on{color:#4F46E5}
.step.on .n{background:#4F46E5;border-color:#4F46E5;color:#fff}
.step.done{color:#15803D}
.step.done .n{background:#DCFCE7;border-color:#BBF7D0;color:#15803D}
.step-line{flex:1;height:1.4px;background:#E6E9F1;margin:0 8px}
.step-line.done{background:#BBF7D0}
.regchip{display:flex;align-items:center;gap:6px;height:30px;padding:0 8px;border-radius:8px;
  border:1px solid #EEF0F6;background:#fff;font-size:10.5px;color:#3D4457;font-weight:600}
.regchip .sw{width:10px;height:10px;border-radius:3px}
.regchip .ok{color:#15803D;margin-left:auto;font-size:9.5px}
.regchip.warn{background:#FFFBEB;border-color:#FDE68A;color:#B45309}
.regchip.warn .ok{color:#B45309}
.small{font-size:10px;color:#9AA1B4;line-height:1.6}
.kv{display:flex;justify-content:space-between;font-size:10.5px;padding:3px 0;color:#5B6376}
.kv b{color:#161B2E;font-weight:600}
.footnote{font-size:9.5px;color:#9AA1B4}
"""


def load_board():
    return json.loads((ROOT / "board.json").read_text(encoding="utf-8"))


def candidates(grid, region_of, r, c):
    used = set()
    for i in range(9):
        used.add(grid[r][i])
        used.add(grid[i][c])
    for i in range(3):
        for j in range(3):
            used.add(grid[(r // 3) * 3 + i][(c // 3) * 3 + j])
    k = region_of[r][c]
    for rr in range(9):
        for cc in range(9):
            if region_of[rr][cc] == k:
                used.add(grid[rr][cc])
    return [d for d in range(1, 10) if d not in used]


def find_hint(grid, region_of):
    naked = []
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                cs = candidates(grid, region_of, r, c)
                if len(cs) == 1:
                    naked.append((r, c, cs[0]))
    if naked:
        return ("naked", naked[0])
    units = []
    for r in range(9):
        units.append(("row", r, [(r, c) for c in range(9)]))
    for c in range(9):
        units.append(("col", c, [(r, c) for r in range(9)]))
    for br in range(3):
        for bc in range(3):
            units.append(("box", (br, bc), [(br * 3 + i, bc * 3 + j) for i in range(3) for j in range(3)]))
    for k in range(9):
        units.append(("reg", k, [(r, c) for r in range(9) for c in range(9) if region_of[r][c] == k]))
    for kind, idx, cells in units:
        for d in range(1, 10):
            spots = [(r, c) for r, c in cells if grid[r][c] == 0 and d in candidates(grid, region_of, r, c)]
            if len(spots) == 1:
                return ("hidden", (spots[0][0], spots[0][1], d, kind, idx))
    return None


def build_state(b, rng_seed=11):
    import random
    rnd = random.Random(rng_seed)
    puzzle = b["puzzle"]
    sol = b["solution"]
    region_of = b["regions"]
    grid = [row[:] for row in puzzle]
    empties = [(r, c) for r in range(9) for c in range(9) if grid[r][c] == 0]
    rnd.shuffle(empties)
    wrong = None
    filled = []
    for i, (r, c) in enumerate(empties):
        if i < 15:
            grid[r][c] = sol[r][c]
            filled.append((r, c))
    # one deliberate mistake in a cell that conflicts with its row
    for r, c in empties[15:]:
        row_digits = {grid[r][i] for i in range(9)} | {sol[r][i] for i in range(9) if i != c}
        bad = None
        for d in range(1, 10):
            if d != sol[r][c] and d in {sol[r][i] for i in range(9) if i != c}:
                bad = d
                break
        if bad:
            grid[r][c] = bad
            wrong = (r, c, bad)
            break
    hint = find_hint(grid, region_of)
    # notes on a few empty cells
    notes = {}
    for r, c in empties[20:]:
        if grid[r][c] == 0:
            cs = candidates(grid, region_of, r, c)
            if 2 <= len(cs) <= 4:
                notes[(r, c)] = cs
        if len(notes) >= 4:
            break
    return {
        "grid": grid, "given": puzzle, "sol": sol, "region": region_of,
        "filled": filled, "wrong": wrong, "notes": notes, "hint": hint,
    }


def board_html(cell, region_of, opts):
    W = cell * 9
    grid = opts.get("grid")
    given = opts.get("given")
    sel = opts.get("sel")
    hint = opts.get("hint_cell")
    voids = opts.get("voids", set())
    conflicts = opts.get("conflicts", set())
    same = opts.get("same", set())
    peers = opts.get("peers", set())
    show_values = opts.get("show_values", True)
    faint = opts.get("faint", False)
    labels = opts.get("labels", False)
    brush = opts.get("brush")

    out = [f'<div class="board" style="width:{W}px;height:{W}px">']
    for r in range(9):
        for c in range(9):
            k = region_of[r][c]
            if (r, c) in voids:
                cls = "cell void"
                bg = "#F7F8FC"
            else:
                cls = "cell"
                bg = PAL[k % 9][0]
            if (r, c) in peers and (r, c) not in voids:
                cls += " peer"
            if (r, c) in same:
                cls += " same"
            if (r, c) in conflicts:
                cls += " bad"
            out.append(f'<div class="{cls}" style="left:{c*cell}px;top:{r*cell}px;'
                       f'width:{cell}px;height:{cell}px;background-color:{bg}"></div>')

    # ---- vector lines: full cell grid, full 3x3 grid, then region borders ----
    thin, box, thick, dash = [], [], [], []
    for r in range(9):
        for c in range(9):
            x, y = c * cell, r * cell
            if c < 8:
                thin.append((x + cell, y, x + cell, y + cell))
                a, b2 = (r, c), (r, c + 1)
                av, bv = a in voids, b2 in voids
                if av != bv:
                    dash.append((x + cell, y, x + cell, y + cell))
                elif not av and region_of[a[0]][a[1]] != region_of[b2[0]][b2[1]]:
                    thick.append((x + cell, y, x + cell, y + cell))
            if r < 8:
                thin.append((x, y + cell, x + cell, y + cell))
                a, b2 = (r, c), (r + 1, c)
                av, bv = a in voids, b2 in voids
                if av != bv:
                    dash.append((x, y + cell, x + cell, y + cell))
                elif not av and region_of[a[0]][a[1]] != region_of[b2[0]][b2[1]]:
                    thick.append((x, y + cell, x + cell, y + cell))
    for i in (3, 6):
        box.append((i * cell, 0, i * cell, W))
        box.append((0, i * cell, W, i * cell))

    svg = [f'<svg class="lines" width="{W}" height="{W}" viewBox="0 0 {W} {W}">']
    for x1, y1, x2, y2 in thin:
        svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="rgba(35,42,60,.085)" stroke-width="0.9"/>')
    for x1, y1, x2, y2 in box:
        svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#8C95A8" stroke-opacity="0.95" stroke-width="1.7"/>')
    for x1, y1, x2, y2 in thick:
        svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{INK}" stroke-width="3.2" stroke-linecap="square"/>')
    for x1, y1, x2, y2 in dash:
        svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#8E97AC" stroke-width="1.7" '
                   f'stroke-dasharray="5 4"/>')
    svg.append(f'<rect x="1.6" y="1.6" width="{W-3.2}" height="{W-3.2}" fill="none" stroke="{INK}" stroke-width="3.2"/>')
    svg.append("</svg>")
    out.append("".join(svg))

    # ---- values ----
    if show_values and grid:
        for r in range(9):
            for c in range(9):
                v = grid[r][c]
                if not v:
                    continue
                cls = "val"
                if given and given[r][c]:
                    cls += " given"
                elif (r, c) in conflicts:
                    cls += " bad"
                elif faint:
                    cls += " faint"
                else:
                    cls += " user"
                fs = int(cell * 0.54)
                out.append(f'<div class="{cls}" style="left:{c*cell}px;top:{r*cell}px;width:{cell}px;'
                           f'height:{cell}px;font-size:{fs}px">{v}</div>')

    # ---- notes ----
    if opts.get("notes"):
        for (r, c), cs in opts["notes"].items():
            fs = max(8, int(cell * 0.19))
            spans = "".join(f'<span>{d}</span>' for d in range(1, 10))
            vis = "".join(f'<span>{d if d in cs else ""}</span>' for d in range(1, 10))
            out.append(f'<div class="notes" style="left:{c*cell}px;top:{r*cell}px;width:{cell}px;'
                       f'height:{cell}px;font-size:{fs}px">{vis}</div>')

    # ---- region labels ----
    if labels:
        for k in range(9):
            cells = [(r, c) for r in range(9) for c in range(9)
                     if region_of[r][c] == k and (r, c) not in voids]
            if not cells:
                continue
            cx = sum(c for r, c in cells) / len(cells)
            cy = sum(r for r, c in cells) / len(cells)
            r, c = min(cells, key=lambda p: (p[0] - cy) ** 2 + (p[1] - cx) ** 2)
            col = PAL[k % 9][1]
            fs = max(8, int(cell * 0.19))
            out.append(f'<div style="position:absolute;left:{c*cell + cell/2}px;top:{r*cell + cell/2}px;'
                       f'transform:translate(-50%,-50%);z-index:3;background:rgba(255,255,255,.86);'
                       f'border:1px solid {col};color:{col};font-size:{fs}px;font-weight:700;'
                       f'padding:1px 4px;border-radius:4px;line-height:1.25;letter-spacing:.3px">R{k+1}</div>')

    # ---- selection / hint / brush ----
    def ring(r, c, cls, inset=1.5):
        return (f'<div class="{cls}" style="left:{c*cell+inset}px;top:{r*cell+inset}px;'
                f'width:{cell-2*inset}px;height:{cell-2*inset}px"></div>')

    if hint:
        out.append(ring(hint[0], hint[1], "hint", 2.5))
    if sel:
        out.append(ring(sel[0], sel[1], "sel", 1.5))
    if brush:
        out.append(ring(brush[0], brush[1], "brush", 1.5))
    out.append("</div>")
    return "".join(out)


def ico(name, size=15):
    paths = {
        "pencil": '<path d="M14.5 4.5l5 5L9 20H4v-5z"/><path d="M13 6l5 5"/>',
        "dots": '<circle cx="7" cy="7" r="1.4"/><circle cx="12" cy="7" r="1.4"/><circle cx="17" cy="7" r="1.4"/>'
                '<circle cx="7" cy="12" r="1.4"/><circle cx="12" cy="12" r="1.4"/><circle cx="17" cy="12" r="1.4"/>'
                '<circle cx="7" cy="17" r="1.4"/><circle cx="12" cy="17" r="1.4"/><circle cx="17" cy="17" r="1.4"/>',
        "eraser": '<path d="M8 20h11"/><path d="M14.5 4.5l5 5-7.5 7.5H7.5L4.5 14z"/>',
        "undo": '<path d="M3 9a9 9 0 1 1 2.7 6.4"/><path d="M3 4.5V9h4.5"/>',
        "redo": '<path d="M21 9A9 9 0 1 0 18.3 15.4"/><path d="M21 4.5V9h-4.5"/>',
        "bulb": '<path d="M9.5 18h5"/><path d="M10.5 21h3"/><path d="M12 3a6 6 0 0 0-3.4 10.9c.3.3.4.7.4 1.1v.5h6v-.5c0-.4.1-.8.4-1.1A6 6 0 0 0 12 3z"/>',
        "spark": '<path d="M12 3l1.7 5.3L19 10l-5.3 1.7L12 17l-1.7-5.3L5 10l5.3-1.7z"/>',
        "share": '<path d="M4 12v7a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-7"/><path d="M12 15V4"/><path d="M8 8l4-4 4 4"/>',
        "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
        "gear": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.9l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-2.9 1.2 2 2 0 1 1-4 0 1.7 1.7 0 0 0-2.9-1.2l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1A1.7 1.7 0 0 0 4.6 15a2 2 0 1 1 0-4 1.7 1.7 0 0 0 1.2-2.9l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1A1.7 1.7 0 0 0 11.5 4a2 2 0 1 1 4 0 1.7 1.7 0 0 0 2.9 1.2l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0 1.2 2.9 2 2 0 1 1 0 4z"/>',
        "chev": '<path d="M15 6l-6 6 6 6"/>',
        "check": '<path d="M4.5 12.5l5 5 10-11"/>',
    }
    fill = "currentColor" if name in ("spark",) else "none"
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="{fill}" stroke="currentColor" '
            f'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{paths[name]}</svg>')


# ------------------------------------------------------------------ screen A
def screen_solve(st):
    cell = 54
    b = load_board()
    region_of = b["regions"]
    grid = st["grid"]
    given = b["puzzle"]

    hint = st["hint"]
    hint_cell = None
    hint_digit = None
    tech = "候选扫描"
    quote = "当前局面没有单步可推的唯一解，建议先补全候选数。"
    if hint and hint[0] == "naked":
        r, c, d = hint[1]
        hint_cell, hint_digit = (r, c), d
        tech = "唯一候选 · Naked Single"
        quote = (f'<b>第 {r+1} 行第 {c+1} 列</b>只剩 <b>{d}</b> 一个候选：这一行、这一列、所在的 3×3 宫，'
                 f'以及{CNAME[region_of[r][c]]}区域已经把其余 8 个数字全部排除。')
    elif hint and hint[0] == "hidden":
        r, c, d, kind, idx = hint[1]
        hint_cell, hint_digit = (r, c), d
        label = {"row": f"第 {idx+1} 行", "col": f"第 {idx+1} 列",
                 "box": "该 3×3 宫", "reg": f"第 {region_of[r][c]+1} 号异形区域"}[kind]
        tech = {"row": "隐性唯一 · Hidden Single", "col": "隐性唯一 · Hidden Single",
                "box": "宫排除 · Box Line", "reg": "区域唯一 · Region Single"}[kind]
        quote = (f'在 <b>{label}</b> 里，数字 <b>{d}</b> 只剩 <b>第 {r+1} 行第 {c+1} 列</b> 一个落点。'
                 f'异形区域的边界不规则，这类“区域内唯一”往往是解题的突破口。')

    sel = hint_cell or (0, 0)
    same = {(r, c) for r in range(9) for c in range(9)
            if grid[r][c] and grid[r][c] == grid[sel[0]][sel[1]]}
    conflicts = set()
    if st["wrong"]:
        r, c, d = st["wrong"]
        conflicts.add((r, c))
        for i in range(9):
            if i != c and grid[r][i] == d:
                conflicts.add((r, i))

    notes = dict(st["notes"])
    if hint_cell and hint_digit:
        notes[hint_cell] = [hint_digit]

    board = board_html(cell, region_of, {
        "grid": grid, "given": given, "sel": sel, "hint_cell": hint_cell,
        "notes": notes, "conflicts": conflicts, "same": same,
    })

    filled = sum(1 for r in range(9) for c in range(9) if grid[r][c])
    pct = round(filled / 81 * 100)
    empties = 81 - filled
    cand_total = sum(len(candidates(grid, region_of, r, c))
                     for r in range(9) for c in range(9) if grid[r][c] == 0)
    avg_cand = round(cand_total / empties, 1) if empties else 0
    remain = {d: 9 - sum(1 for r in range(9) for c in range(9) if grid[r][c] == d) for d in range(1, 10)}

    keys = []
    for d in range(1, 10):
        cls = "key done" if remain[d] == 0 else "key"
        keys.append(f'<div class="{cls}"><b>{d}</b><em>{remain[d]}</em></div>')

    legend = []
    for k in range(9):
        cnt = sum(1 for r in range(9) for c in range(9) if region_of[r][c] == k and grid[r][c])
        legend.append(
            f'<div class="lg"><span class="sw" style="background:{PAL[k][0]};'
            f'box-shadow:inset 0 0 0 1.6px {PAL[k][1]}"></span>'
            f'<span class="nm">R{k+1} · {CNAME[k]}</span><span class="ct">{cnt}/9</span></div>')

    tools = [("pencil", "铅笔", True), ("dots", "候选", True), ("eraser", "擦除", False),
             ("undo", "撤销", False), ("redo", "重做", False), ("bulb", "提示", False)]
    tool_html = "".join(
        f'<div class="tool{" on" if on else ""}">{ico(n, 16)}<span>{label}</span></div>'
        for n, label, on in tools)

    return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><style>{CSS}</style></head>
<body><div class="screen" style="width:1140px;height:840px">
  <div class="appbar">
    <div class="logo"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
    <div class="brand">数独工坊<small>Jigsaw</small></div>
    <div class="tabs"><div class="tab on">解题</div><div class="tab">出题</div><div class="tab">学习</div></div>
    <div class="spacer"></div>
    <div class="chip"><span class="dot"></span>异形 · 专家</div>
    <div class="timer">{ico('clock', 14)}12:47</div>
    <div class="iconbtn">{ico('share', 14)}</div>
    <div class="iconbtn">{ico('gear', 14)}</div>
    <div class="avatar">林</div>
  </div>

  <div class="body">
    <div class="col" style="width:664px">
      <div class="card board-card">
        <div class="board-row">
          {board}
          <div class="legend">
            <div class="hd">异形区域 · 已填 / 9</div>
            {''.join(legend)}
          </div>
        </div>
        <div class="status">
          <span class="pill green">{ico('check', 11)}区域合法</span>
          <span class="pill red">冲突 1</span>
          <div class="bar"><i style="width:{pct}%"></i></div>
          <span style="font-variant-numeric:tabular-nums">{filled}/81</span>
        </div>
      </div>
      <div class="card pad stats" style="align-items:center">
        <div class="stat"><div class="k">用时</div><div class="v">12:47</div></div>
        <div class="stat"><div class="k">错误</div><div class="v">1<small>次</small></div></div>
        <div class="stat"><div class="k">提示</div><div class="v">2<small>次</small></div></div>
        <div class="stat"><div class="k">难度</div><div class="v" style="font-size:16px;padding-top:4px">专家</div></div>
        <div style="display:flex;flex-direction:column;gap:4px;align-items:flex-end">
          <span class="footnote">自动候选 · 已开启</span>
          <span class="footnote">本地存档 · 刚刚</span>
        </div>
      </div>
    </div>

    <div class="col" style="flex:1">
      <div class="card pad">
        <div style="display:flex;align-items:center;justify-content:space-between">
          <span class="title">数字键盘</span><span class="footnote">角标 = 还可填</span>
        </div>
        <div class="grid-nine" style="margin-top:10px">{''.join(keys)}</div>
      </div>

      <div class="card pad">
        <span class="title">工具</span>
        <div class="tools">{tool_html}</div>
      </div>

      <div class="card ai">
        <div class="hd">
          <div class="spark">{ico('spark', 13)}</div>
          <div style="flex:1">
            <div class="t">AI 教练</div>
            <div class="s">规则引擎先算 · 模型只负责讲人话</div>
          </div>
          <span class="pill" style="height:20px;font-size:9.5px">仅解释</span>
        </div>
        <div style="padding:10px 15px 13px;display:flex;flex-direction:column;flex:1">
          <div><span class="tech">{tech}</span></div>
          <div class="quote">{quote}</div>
          <div class="chain">
            <div class="chain-hd">推 理 链</div>
            <div class="chain-row"><i>1</i><span>候选扫描：{empties} 个空格，平均 {avg_cand} 个候选</span></div>
            <div class="chain-row"><i>2</i><span>单元排查：行 / 列 / 3×3 宫 / 异形区域</span></div>
            <div class="chain-row"><i>3</i><span>结论：唯一落点，已在棋盘上高亮</span></div>
            <div class="chain-row"><i>4</i><span>校验：与唯一解一致，可信度高</span></div>
          </div>
          <div class="quote muted" style="font-size:10px;margin-top:8px;line-height:1.6">
            提示由求解器生成并校验，模型只做转述——不会算错，也不会烧 token。
          </div>
          <div style="display:flex;gap:6px;margin-top:11px;flex-wrap:wrap">
            <span class="pill" style="height:23px;font-size:9.5px">为什么不是 4？</span>
            <span class="pill" style="height:23px;font-size:9.5px">有更快的解法吗？</span>
            <span class="pill" style="height:23px;font-size:9.5px">讲讲剩余法则</span>
          </div>
          <div class="btns">
            <div class="btn primary">解释这一步</div>
            <div class="btn ghost">完整推理链</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div></body></html>"""


# ------------------------------------------------------------------ screen B
def screen_editor():
    b = load_board()
    region_of = [row[:] for row in b["regions"]]
    # last region is partially drawn: 3 cells still unassigned
    k = 8
    cells = [(r, c) for r in range(9) for c in range(9) if region_of[r][c] == k]
    cells.sort(key=lambda p: (-p[1], p[0]))
    voids = set(cells[:3])
    region_of = [[(-1 if (r, c) in voids else region_of[r][c]) for c in range(9)] for r in range(9)]
    brush = cells[3]

    board = board_html(46, region_of, {
        "grid": None, "show_values": False, "voids": voids, "labels": True, "brush": brush,
    })

    chips = []
    for kk in range(9):
        cnt = sum(1 for r in range(9) for c in range(9) if region_of[r][c] == kk)
        if kk == 8:
            chips.append(f'<div class="regchip warn"><span class="sw" style="background:{PAL[kk][0]};'
                         f'box-shadow:inset 0 0 0 1.4px {PAL[kk][1]}"></span>R9 异形区'
                         f'<span class="ok">{cnt}/9</span></div>')
        else:
            chips.append(f'<div class="regchip"><span class="sw" style="background:{PAL[kk][0]};'
                         f'box-shadow:inset 0 0 0 1.4px {PAL[kk][1]}"></span>R{kk+1}'
                         f'<span class="ok">9/9 ✓</span></div>')

    return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><style>{CSS}</style></head>
<body><div class="screen" style="width:560px;height:840px">
  <div class="appbar" style="height:52px;flex:0 0 52px;padding:0 14px;gap:10px">
    <div class="iconbtn" style="width:28px;height:28px">{ico('chev', 14)}</div>
    <div style="font-size:14px;font-weight:700">出题工作台</div>
    <div class="spacer"></div>
    <span class="pill" style="height:24px">草稿已保存</span>
  </div>

  <div style="padding:12px 16px 0">
    <div class="steps">
      <div class="step on"><span class="n">1</span>画区域</div>
      <div class="step-line"></div>
      <div class="step"><span class="n">2</span>生成答案</div>
      <div class="step-line"></div>
      <div class="step"><span class="n">3</span>挖空</div>
      <div class="step-line"></div>
      <div class="step"><span class="n">4</span>校验</div>
    </div>
  </div>

  <div style="padding:12px 16px 0">
    <div class="card" style="padding:12px">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:9px">
        <span class="title">勾选 9 格异形区域</span>
        <span class="pill amber" style="height:20px;font-size:9.5px">还需 3 格</span>
      </div>
      {board}
      <div class="status" style="margin-top:10px">
        <span class="pill green">{ico('check', 11)}连通</span>
        <span class="pill">区域 8/9</span>
        <div class="bar"><i style="width:89%"></i></div>
        <span style="font-variant-numeric:tabular-nums">89%</span>
      </div>
    </div>
  </div>

  <div style="padding:10px 16px 0;flex:1;display:flex;flex-direction:column;gap:8px">
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:6px">
      {''.join(chips)}
    </div>
    <div class="card" style="padding:10px 12px">
      <div class="kv"><span>每区格数 = 9</span><b style="color:#15803D">8 / 9 通过</b></div>
      <div class="kv"><span>区域内 1–9 不重复</span><b style="color:#15803D">通过</b></div>
      <div class="kv"><span>3×3 宫 / 行 / 列</span><b style="color:#15803D">通过</b></div>
    </div>
    <div style="display:flex;gap:8px">
      <div class="btn ghost" style="flex:1;height:38px">随机区域</div>
      <div class="btn ghost" style="flex:1;height:38px">套用模板</div>
      <div class="btn primary" style="flex:1.2;height:38px">生成答案</div>
    </div>
    <div class="footnote" style="text-align:center">区域必须连通，且每区恰好 9 格</div>
  </div>
</div></body></html>"""


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    out = ROOT / "ui"
    out.mkdir(exist_ok=True)
    st = build_state(load_board())
    if what in ("solve", "all"):
        (out / "screen_solve.html").write_text(screen_solve(st), encoding="utf-8")
    if what in ("editor", "all"):
        (out / "screen_editor.html").write_text(screen_editor(), encoding="utf-8")
    print("ok")


if __name__ == "__main__":
    main()
