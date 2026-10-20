# Handoff: NHL 94 PC Demo

## Status (2026-10-20)
- Repo bootstrapped: docs, `.gitignore`, `tools/rebuild_exe.py` (16-bit MZ split/rebuild/verify; tested MATCH on a synthetic MZ).
- **Blocker:** `HOCKEY94DEMO.EXE` is not committed yet; the agent could not get the bytes onto the box. Commit it at the root, then run `python3 tools/rebuild_exe.py verify` (expects SHA-256 `8a6262bd…687f2`).
- Function/segment counts from the IDA listing: still to do (needs the `.lst` on disk; see Next).

## Setup
Python 3. Later: nasm or JWasm, DOSBox, Microsoft C 6.00A (to confirm; candidates MSC 6.00A, 7.0, VC++ 1.0).

## Verify
`python3 tools/rebuild_exe.py verify` must print `MATCH`.

## Known facts
- MZ, large model, `use16`, segments seg000..seg091 + dseg, stack seg 0x1800, entry 241A:04D2 (IDA).
- MSC: `MS Run-Time Library - Copyright (c) 1990`, R6000-R6009, `_C_FILE_INFO=`; `This program requires an 80286` (/G2); prologue `enter n,0; push di; push si`; cdecl far, caller pops.
- EACLIB (`c:\eaclib\%s`) error strings name functions: `unpacka`, `initmemman`, `emmcopybuf`, `reservemem`, `resizememblock`, `findmemblock`, `getmemblock` (EMS via `EMMXXXX0`). Name the functions that reference each string by xref.

## Next
1. Commit the EXE; `verify` MATCH.
2. `tools/lst_count.py`-style count of procs (named vs `sub_`) and segments from the `.lst`; name EACLIB functions from their error-string xrefs into `tools/manual_names.csv`.
3. Per-segment asm build (see docs/PLAN.md §3), then compiler confirmation, cross-ref naming vs 95PC, C matching.

## Unsure
- Exact MSC version/patch level; EXE overlay/trailing data contents.
