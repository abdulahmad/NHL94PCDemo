# NHL 94 PC Demo segment agent

This file is the queue. Do not rewrite it as a whole file. Edit the current row in place; no history entries.
(Adapted from the NHL95PC and NHL94SNES SEGMENT_AGENT.md.)

## Current segment

Not started. Prerequisite: the per-segment asm build (docs/PLAN.md §3) must exist and `make`/`verify` must MATCH from `src/`. Then take seg000.

## Scope

- Queue segments are the MZ code segments `seg000` .. `seg091`, in order, one per session. Segment boundaries come from the IDA listing / segment map and are fixed for the queue; a boundary move is a separate change, never part of a segment session.
- `dseg` (initialised data, BSS, stack) is not a queue segment. Name each `dseg` label the current segment uses, in its `dseg` file, in the same session. Any data label or library routine may be named whenever the evidence is there.
- Library segments (MSC runtime, EACLIB) are queue rows too: MSC routines keep MSC library names, EACLIB routines keep EA's names from the `c:\eaclib\%s` error strings.

## Naming

Follow "Naming rules" in CONTRIBUTING.md (93G first, then 94G, then 93S/94S, then the 95PC name, then behaviour; no guesses; clash rule; casing; team abbreviations; `docs/name_map.csv`).

## Sources

- Reference EXE: `HOCKEY94DEMO.EXE` at the repo root (SHA-256 `8a6262bd…687f2`). Do not commit the `.lst` or `ref/`.
- Name evidence: `docs/name_map.csv`, `tools/manual_names.csv`; NHL95PC `name_map_94.csv` and its `src/` (same code base, 32-bit, later); NHLPA93Genesis, NHL94Genesis, NHLPA93SNES, NHL94SNES on GitHub.

## Per segment

1. Take the current row. Build (`python3 tools/rebuild_exe.py verify`, later `make`) and confirm MATCH.
2. For each proc, find the counterpart (95PC first as a map, then confirm against 93G / 94G / 93S / 94S): calls, constants, structure fields, branch shape, strings. Reject a proposal that does not hold.
3. Rename every label the segment defines (functions, `loc_` -> 93G-style locals, switch tables `_jt`, shared tails), with evidence; add a `docs/name_map.csv` row per rename.
4. Name the `dseg` labels the segment uses (93G RAM name, else 94G, else from what it holds).
5. Comments: the 93G comment when the routine matches, else a header saying what it does, its arguments and result. Note PC differences from Genesis values.
6. Build: MATCH.
7. Mark the row `done` (date, procs named, what is left), set Current segment to the next row, update docs/HANDOFF.md.
8. Commit and push to main: one segment per commit. Never force-push.

## Rules (16-bit x86, MSC large model)

- The bytes must not change: edit names, operands written as names, comments and labels, never the encoding. Keep encoding hints (`short`/`near`, `byte`/`word` displacements, segment overrides, `far` calls).
- Far pointers and `seg` references carry MZ relocations; a number where the original had a segment reference (or the reverse) changes `relocs.tsv`, and verify fails.
- MSC conventions: cdecl far, caller pops; prologue `enter n,0; push di; push si`; result in `ax` (`dx:ax` for long / far pointer); `/G2` 80286 code.
- Hand-written asm (EACLIB, runtime) does not follow the C conventions.

## Queue

| Row | Segment | Status | Note |
|-----|---------|--------|------|
| 0 | seg000 | todo | |
| ... | seg001 - seg091 | todo | add a row per segment when the asm build lands (sizes and roles from the listing) |
