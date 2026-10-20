# Contributing
- `main` only takes byte-identical changes: `python3 tools/rebuild_exe.py verify` (and later `make`) must print MATCH before every commit.
- Small commits; never force-push. One agent at a time.
- Names: see Naming rules below; segment work follows SEGMENT_AGENT.md.
- Comments: no IDA artefacts (sub_, loc_), no hardcoded addresses outside headers; every function gets a header comment (what, args, result).
- Failed matching attempts go in `docs/UNSURE.md`; never retry a listed shape.
- Do not commit `*.lst`, `build/`, `ref/`.

## Naming rules

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
