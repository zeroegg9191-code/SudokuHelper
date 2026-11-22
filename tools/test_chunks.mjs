// Extra tests for the incremental (chunked) generation API.
import fs from 'node:fs';

const html = fs.readFileSync('sudoku.html', 'utf8');
const core = html.slice(html.indexOf('/* ==== CORE START ==== */'), html.indexOf('/* ==== CORE END ==== */'));
const SC = new Function(core + '\nreturn SC;')();

let pass = 0, fail = 0;
const ok = (c, n, e) => { if (c) pass++; else { fail++; console.log('FAIL  ' + n + (e ? '  ' + e : '')); } };

// 1. chunked melt === one-shot melt (same rng, same result)
{
  const a = SC.mulberry32(20261122);
  const solA = SC.genSolution(a);
  const oneShot = SC.meltRegions(a, solA, 600);

  const b = SC.mulberry32(20261122);
  const solB = SC.genSolution(b);
  const reg = SC.boxPartition();
  for (let i = 0; i < 6; i++) SC.meltStep(b, solB, reg, 100);

  ok(Array.from(oneShot).join(',') === Array.from(reg).join(','), 'chunked melt matches one-shot melt');
  ok(SC.validateRegions(reg).ok, 'chunked melt result is valid');
}

// 2. makeDigger stepped === digPuzzle
{
  const rng = SC.mulberry32(777);
  const sol = SC.genSolution(rng);
  const reg = SC.meltRegions(rng, sol, 600);

  const r1 = SC.digPuzzle(rng, sol, reg, 32);

  const rng2 = SC.mulberry32(777);
  const sol2 = SC.genSolution(rng2);
  const reg2 = SC.meltRegions(rng2, sol2, 600);
  const d = SC.makeDigger(rng2, sol2, reg2, 32);
  let guard = 0;
  while (!d.done() && guard++ < 500) d.step();
  const r2 = d.result();

  ok(r1.givens === r2.givens, 'digger matches digPuzzle (givens)', r1.givens + ' vs ' + r2.givens);
  ok(Array.from(r1.puzzle).join(',') === Array.from(r2.puzzle).join(','), 'digger matches digPuzzle (grid)');
  ok(SC.solver(r2.puzzle, reg2, { limit: 2 }).count === 1, 'chunked digger keeps uniqueness');
}

// 3. digExact: never below target, always unique
{
  const rng = SC.mulberry32(31337);
  const sol = SC.genSolution(rng);
  const reg = SC.meltRegions(rng, sol, 600);
  for (const target of [28, 34, 40]) {
    const r = SC.digExact(rng, sol, reg, target, null, 3);
    ok(r.givens >= target, 'digExact respects target ' + target, 'got ' + r.givens);
    ok(SC.solver(r.puzzle, reg, { limit: 2 }).count === 1, 'digExact unique at ' + target);
  }
}

// 4. digExact with preset digits keeps them
{
  const rng = SC.mulberry32(4242);
  const sol = SC.genSolution(rng);
  const reg = SC.meltRegions(rng, sol, 600);
  const keep = new Int8Array(81);
  [3, 12, 27, 45, 70].forEach(i => { keep[i] = sol[i]; });
  const r = SC.digExact(rng, sol, reg, 30, keep, 3);
  let kept = true;
  [3, 12, 27, 45, 70].forEach(i => { if (r.puzzle[i] !== sol[i]) kept = false; });
  ok(kept, 'digExact keeps preset digits');
  ok(r.givens >= 30, 'digExact respects target with presets', 'got ' + r.givens);
}

console.log(`\nchunk tests: pass ${pass} / fail ${fail}`);
process.exit(fail ? 1 : 0);
