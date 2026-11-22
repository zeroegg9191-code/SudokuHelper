// Node test harness for sudoku.html core logic.
// Extracts the CORE script block and exercises it without a DOM.
import fs from 'node:fs';
import path from 'node:path';

const file = path.resolve('sudoku.html');
const html = fs.readFileSync(file, 'utf8');

function extract(tag) {
  const start = html.indexOf(`/* ==== ${tag} START ==== */`);
  const end = html.indexOf(`/* ==== ${tag} END ==== */`);
  if (start < 0 || end < 0) throw new Error(`marker ${tag} not found`);
  return html.slice(start, end);
}

const SC = new Function(extract('CORE') + '\nreturn SC;')();

let pass = 0, fail = 0;
const t0 = Date.now();
function ok(cond, name, extra) {
  if (cond) { pass++; return; }
  fail++;
  console.log('FAIL  ' + name + (extra ? '  ' + extra : ''));
}
function eq(a, b, name) { ok(a === b, name, `expected ${b}, got ${a}`); }

const validGrid = (g) => {
  for (let r = 0; r < 9; r++) {
    const s = new Set();
    for (let c = 0; c < 9; c++) s.add(g[r * 9 + c]);
    if (s.size !== 9 || s.has(0)) return 'row' + r;
  }
  for (let c = 0; c < 9; c++) {
    const s = new Set();
    for (let r = 0; r < 9; r++) s.add(g[r * 9 + c]);
    if (s.size !== 9) return 'col' + c;
  }
  for (let br = 0; br < 3; br++) for (let bc = 0; bc < 3; bc++) {
    const s = new Set();
    for (let a = 0; a < 3; a++) for (let b = 0; b < 3; b++) s.add(g[(br * 3 + a) * 9 + bc * 3 + b]);
    if (s.size !== 9) return 'box';
  }
  return true;
};

// 1. solution generator
{
  const rng = SC.mulberry32(12345);
  let good = 0;
  for (let i = 0; i < 20; i++) if (validGrid(SC.genSolution(rng)) === true) good++;
  eq(good, 20, 'genSolution produces 20 valid grids');
}

// 2. jigsaw partition still valid (9 regions x 9 cells, digits 1-9)
{
  let allOk = 0;
  const t = Date.now();
  for (let seed = 1; seed <= 5; seed++) {
    const rng = SC.mulberry32(seed * 7777);
    const sol = SC.genSolution(rng);
    const reg = SC.meltRegions(rng, sol, 900);
    const v = SC.validateRegions(reg);
    const match = SC.regionsMatchSolution(sol, reg);
    if (v.ok && match && v.defined === 9) allOk++;
    else console.log('   seed', seed, 'problems', v.problems.slice(0, 2), 'match', match);
  }
  eq(allOk, 5, 'meltRegions yields 9 regions of 9 cells, 1-9 each');
  console.log('   melt x5 took ' + (Date.now() - t) + ' ms');
}

// 3. region rules changed: fewer regions allowed, connectivity NOT required
{
  const empty = new Int8Array(81).fill(-1);
  ok(!SC.validateRegions(empty).ok, 'zero regions rejected');

  const three = new Int8Array(81).fill(-1);
  for (let k = 0; k < 3; k++) for (let i = 0; i < 9; i++) three[k * 9 + i] = k;
  const v3 = SC.validateRegions(three);
  ok(v3.ok, 'three 9-cell regions are valid', JSON.stringify(v3.problems));
  eq(v3.defined, 3, 'defined count is 3');
  eq(v3.covered, 27, 'covered count is 27');

  // scattered / disconnected 9 cells must be accepted now
  const scat = new Int8Array(81).fill(-1);
  const cells = [0, 2, 4, 20, 22, 40, 60, 62, 80];
  cells.forEach(i => { scat[i] = 0; });
  ok(SC.validateRegions(scat).ok, 'disconnected 9-cell region is valid');

  const eight = new Int8Array(81).fill(-1);
  for (let i = 0; i < 8; i++) eight[i] = 0;
  ok(!SC.validateRegions(eight).ok, 'region with 8 cells rejected');

  const ten = new Int8Array(81).fill(-1);
  for (let i = 0; i < 10; i++) ten[i] = 0;
  ok(!SC.validateRegions(ten).ok, 'region with 10 cells rejected');
}

// 4. solver works with partial regions and preset digits
{
  const rng = SC.mulberry32(4242);
  const sol = SC.genSolution(rng);
  const full = SC.meltRegions(rng, sol, 800);
  const partial = new Int8Array(81).fill(-1);
  for (let k = 0; k < 4; k++) for (let i = 0; i < 81; i++) if (full[i] === k) partial[i] = k;
  ok(SC.validateRegions(partial).ok, 'partial 4-region layout valid');
  ok(SC.regionsMatchSolution(sol, partial), 'partial layout matches the solution');

  const preset = new Int8Array(81);
  for (let i = 0; i < 81; i += 7) preset[i] = sol[i];
  const res = SC.solver(preset, partial, { limit: 2 });
  ok(res.count >= 1, 'solver finds a solution with preset digits');
  for (let i = 0; i < 81; i++) if (preset[i] && res.first[i] !== preset[i]) { ok(false, 'preset digit kept', 'at ' + i); break; }

  // a contradictory preset must be reported as unsolvable
  const bad = Int8Array.from(preset);
  bad[0] = bad[1] = 5;
  const res2 = SC.solver(bad, partial, { limit: 1, nodeLimit: 2e5 });
  eq(res2.count, 0, 'contradictory preset has no solution');
}

// 5. digging preserves preset digits + uniqueness
{
  const rng = SC.mulberry32(99);
  const sol = SC.genSolution(rng);
  const reg = SC.meltRegions(rng, sol, 800);
  const keep = new Int8Array(81);
  const givensIdx = [0, 8, 13, 22, 40, 58, 70, 80];
  givensIdx.forEach(i => { keep[i] = sol[i]; });
  const dug = SC.digPuzzle(rng, sol, reg, 30, keep);
  const chk = SC.solver(dug.puzzle, reg, { limit: 2 });
  eq(chk.count, 1, 'dug puzzle unique with preset digits');
  let kept = true;
  for (const i of givensIdx) if (dug.puzzle[i] !== sol[i]) kept = false;
  ok(kept, 'all preset digits survive digging');
}

// 6. default puzzle embedded in the app
{
  const R = /const DEFAULT_R = '([0-9]+)'/.exec(html)[1];
  const Sg = /const DEFAULT_S = '([0-9]+)'/.exec(html)[1];
  const G = /const DEFAULT_G = '([0-9]+)'/.exec(html)[1];
  const regions = Int8Array.from(R.split('').map(Number));
  const sol = Int8Array.from(Sg.split('').map(Number));
  const givens = Int8Array.from(G.split('').map(Number));
  ok(SC.validateRegions(regions).ok, 'default regions valid');
  eq(SC.validateRegions(regions).defined, 9, 'default has 9 regions');
  ok(SC.regionsMatchSolution(sol, regions), 'default regions match solution');
  const res = SC.solver(givens, regions, { limit: 3 });
  eq(res.count, 1, 'default puzzle unique');
  eq(Array.from(res.first).join(''), Sg, 'default solves to embedded solution');
}

// 7. checkGrid / conflicts / candidates
{
  const rng = SC.mulberry32(9);
  const sol = SC.genSolution(rng);
  const reg = SC.meltRegions(rng, sol, 600);
  ok(SC.checkGrid(sol, reg).ok, 'valid full grid passes checkGrid');
  const bad = Int8Array.from(sol); bad[1] = bad[0];
  ok(!SC.checkGrid(bad, reg).ok, 'duplicate detected by checkGrid');
  ok(SC.conflictsOf(bad, reg).size >= 2, 'conflicts flagged');
  eq(SC.conflictsOf(sol, reg).size, 0, 'no conflicts on valid grid');
  eq(SC.candidatesAt(new Int8Array(81), reg, 0).length, 9, 'empty cell has 9 candidates');
  eq(SC.candidatesAt(sol, reg, 0).length, 0, 'filled cell has none');
}

// 8. share code round-trip
{
  const rng = SC.mulberry32(55);
  const sol = SC.genSolution(rng);
  const reg = SC.meltRegions(rng, sol, 600);
  const dug = SC.digPuzzle(rng, sol, reg, 32);
  const code = SC.encodeCode(reg, dug.puzzle);
  ok(code.startsWith('SH1.'), 'code has SH1. prefix');
  ok(code.length < 130, 'code is compact', 'len=' + code.length);
  const dec = SC.decodeCode(code);
  ok(dec !== null, 'decode returns object');
  eq(Array.from(dec.regions).join(','), Array.from(reg).join(','), 'roundtrip regions');
  eq(Array.from(dec.givens).join(','), Array.from(dug.puzzle).join(','), 'roundtrip givens');
  eq(SC.decodeCode('SH1.abc'), null, 'bad code rejected');
  eq(SC.decodeCode(''), null, 'empty code rejected');
  // partial regions survive (cells without region -> 15)
  const partial = Int8Array.from(reg);
  for (let i = 0; i < 30; i++) partial[i] = -1;
  const code2 = SC.encodeCode(partial, dug.puzzle);
  const dec2 = SC.decodeCode(code2);
  eq(Array.from(dec2.regions).slice(0, 30).join(','), new Array(30).fill('-1').join(','), 'empty cells roundtrip as -1');
}

// 9. daily determinism
{
  const t = Date.now();
  const a = SC.buildDaily('2026-11-22', { iters: 900, target: 34 });
  const ms = Date.now() - t;
  const b = SC.buildDaily('2026-11-22', { iters: 900, target: 34 });
  eq(Array.from(a.regions).join(','), Array.from(b.regions).join(','), 'same date -> same regions');
  eq(Array.from(a.givens).join(','), Array.from(b.givens).join(','), 'same date -> same puzzle');
  const c = SC.buildDaily('2026-11-23', { iters: 900, target: 34 });
  ok(Array.from(c.regions).join(',') !== Array.from(a.regions).join(','), 'different date -> different puzzle');
  eq(SC.solver(a.givens, a.regions, { limit: 2 }).count, 1, 'daily puzzle unique');
  console.log('   buildDaily took ' + ms + ' ms');
}

console.log('');
console.log(`pass ${pass} / fail ${fail}   (${Date.now() - t0} ms)`);
process.exit(fail ? 1 : 0);
