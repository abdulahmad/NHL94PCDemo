# Handoff: NHL 94 PC Demo

## Status (2026-10-20)
- Repo bootstrapped: docs, `.gitignore`, `tools/rebuild_exe.py` (16-bit MZ split/rebuild/verify; tested MATCH on a synthetic MZ).
- `HOCKEY94DEMO.EXE` committed (SHA-256 `8a6262bd…687f2`); `python3 tools/rebuild_exe.py verify` prints MATCH (header 13312 B, 3300 relocs, image 233084 B, no overlay).
- Function/segment counts from the IDA listing: still to do (needs the `.lst` on disk; see Next).

## Setup
Python 3. Later: nasm or JWasm, DOSBox, Microsoft C 6.00A (to confirm; candidates MSC 6.00A, 7.0, VC++ 1.0).

## Verify
`python3 tools/rebuild_exe.py verify` must print `MATCH`.

## Known facts
- MZ, large model, `use16`, segments seg000..seg091 + dseg, stack seg 0x1800, entry 241A:04D2 (IDA).
- MSC: `MS Run-Time Library - Copyright (c) 1990`, R6000-R6009, `_C_FILE_INFO=`; `This program requires an 80286` (/G2); prologue `enter n,0; push di; push si`; cdecl far, caller pops.
- EACLIB (`c:\eaclib\%s`) error strings name functions: `unpacka`, `initmemman`, `emmcopybuf`, `reservemem`, `resizememblock`, `findmemblock`, `getmemblock` (EMS via `EMMXXXX0`). Name the functions that reference each string by xref.

## Naming rules (summary; CONTRIBUTING.md is canonical)

Same rules as NHL95PC (SEGMENT_AGENT.md, PROMPT.md) and NHL94SNES (SEGMENT_AGENT.md, docs/HANDOFF.md), adapted to the demo.

- **Lineage:** 92G / 93G -> 93S -> 94S -> **94PC demo** -> 95PC. 94 PC was ported from NHLPA 93 Genesis plus some 94 Genesis additions and a new PC menu system; the demo is that code base before 95PC.
- **Name priority** (match on the body: calls, constants, structure fields, branch shape, strings):
  1. 93G name (92G where 93G kept it; 92G is the naming root), else
  2. 94G name (one-timers, breakaways, extra assignment slots and other 94 features), else
  3. the 93S / 94S name for code that only lines up with the SNES ports, else
  4. the NHL95PC name when the routine is the same (95PC names already carry 93G -> 94G provenance), else
  5. a name from what the code clearly does (strings, callers, data it touches), with the evidence.
  NHL95Genesis is a loose reference only, not a naming source.
- **EACLIB** (`c:\eaclib\%s` library): keep EA's own function names from the error strings (`unpacka`, `initmemman`, `emmcopybuf`, `reservemem`, `resizememblock`, `findmemblock`, `getmemblock`), exact spelling and lower case, given to the function that references the string (by xref). MSC runtime routines keep their MSC library names (`_malloc`, `__chkstk`, ...).
- **No guessing:** a wrong name is worse than an auto name. If there is no match and the behaviour is not obvious, keep the IDA/auto name (`sub_SSSS_OOOO`, `word_...`) and list it under Unsure in `docs/HANDOFF.md`.
- **Clash rule:** never reuse a name for a different item. The earliest game's meaning keeps the name; the later item gets a new name. If a demo label already uses the name for something else, rename that label too.
- **Casing:** keep the source game's casing exactly (93G `skateto`, `SetSPA`, `doinput`; EACLIB lower case). Names from behaviour use CamelCase (`DrawTeamMenu`). Never add a name that differs from an existing one only in case.
- **Prefixes/suffixes:** no IDA artefacts left in finished code (`sub_`, `loc_`, `off_`, `unk_`). Locals in 92/93G style: `.loop`, `.next`, `.done`, `.exit`, or `.1`, `.2` for trivial jumps; a 93G local at the same instruction keeps its 93G name. Shared epilogues are named for the first function (`Func_x`), switch tables `Func_jt` with cases `.cN`. MSC C symbols keep the leading underscore of the cdecl name in asm (`_skateto` in asm is `skateto` in C).
- **Team abbreviations:** use the spelling in the demo's own team data / on-screen strings; where the demo has no string, follow NHL95PC. `NYIslanders` / `NYRangers` stay the long names for the two New York teams.
- **Data/BSS** (`dseg`): the 93G RAM name of the same variable (`ram93.asm`), else 94G (`ram94.asm`), else from what it holds. Name data labels as the code segments that use them are worked.
- **Comments:** no rename-history or provenance comments ("was X", "from 93G"); that history lives only in `docs/name_map.csv`.
- **Name map:** every rename gets a row in `docs/name_map.csv` (`address,name,auto_name,source,confidence,evidence,file`; `source` is `93G`, `92G`, `94G`, `93S`, `94S`, `95PC`, `EACLIB`, `MSC` or `new`). Hand-traced overrides go in `tools/manual_names.csv` (same columns).

Segment work: one MZ segment per session, queue in [SEGMENT_AGENT.md](../SEGMENT_AGENT.md).

## Next
2. `tools/lst_count.py`-style count of procs (named vs `sub_`) and segments from the `.lst`; name EACLIB functions from their error-string xrefs into `tools/manual_names.csv`.
3. Per-segment asm build (see docs/PLAN.md §3), then compiler confirmation, cross-ref naming vs 95PC, C matching.

## Unsure
- Exact MSC version/patch level; EXE overlay/trailing data contents.
