# NHL 94 PC Demo (HOCKEY94DEMO.EXE) disassembly / decompilation plan

Repo: github.com/abdulahmad/NHL94PCDemo (steps 1-2 approved).

Target repo (not created yet): `github.com/abdulahmad/NHL94PC` (or `NHL94PCDemo`). Plan only.

## 0. Key facts found (evidence)

| Fact | Evidence |
|---|---|
| Input: `HOCKEY94DEMO.EXE`, 241 KB, SHA-256 `8A6262BD…687F2`, MD5 `CD60DA30…340B`, CRC32 `CA8766EF` | `.lst` header lines 9-13 |
| **Real-mode 16-bit MZ, not LE/DOS4GW** | `.lst`: "Format: MS-DOS executable (EXE)", "Application type: Executable 16bit", `.model large`, all segments `use16`, entry `241A:04D2`, load range 10000h-4E600h (0x38E7C bytes) |
| Large memory model, ~90 code/data segments + DGROUP | `seg000`..`seg091`, `dseg` ends at AFAC, `seg091` = 0x1800-byte `STACK` segment |
| Instruction set 286+ (`.386` listing directive; code uses `enter`) | `displayDemoControls`: `enter 122h,0` |
| Calling convention = **cdecl far, caller pops** (`call X / add sp,8`), prologue `enter; push di; push si` | seg000:0000-0052. This is the **Microsoft C 7 / Visual C++ 1.x (/AL /G2)** pattern (MSC saves DI then SI; Borland uses `push bp/mov bp,sp/sub sp` then `push si/push di`; Watcom 16-bit `wcc` passes args in AX/DX/BX/CX and would not `add sp` after every call) |
| Symbols are `_main` (leading underscore) | xref `_main+473` – again MSC/Borland style, not Watcom (`main_`) |
| Partially named already (Abdul's names, e.g. `displayDemoControls`, `BlitOrFadeToScreen`, `CleanupGameResources`) mixed with `sub_XXXXX` | `.lst` body |
| EXE itself could not be opened by Read (binary); format facts above come from the listing | — |

**Consequence:** the 95PC compiler (Watcom 10.0 LA `wcc386`, `-5r -fpi -zp1`) does **not** apply to the demo. 94 PC demo was built with a 16-bit DOS compiler, most likely Microsoft C/C++ 7.0 or VC++ 1.0/1.5 (MSC 8.0). Exact 95PC byte matches are therefore impossible; matches against 95PC have to be at the **C-source / control-flow level**, not bytes. (If the retail 94 PC is also 16-bit, same conclusion; check later.)

Not yet counted (do first in step 1 with a script, since Read can't grep): number of `proc` entries, named vs `sub_`, library vs game split, copyright strings (`MS Run-Time Library - Copyright (c) 199x, Microsoft Corp` would confirm MSC and its version; Borland has `Borland C++ - Copyright 1991 Borland Intl.`).


## 0a. Confirmed by Abdul (2026-10-20, strings in the EXE)
- `MS Run-Time Library - Copyright (c) 1990, Microsoft Corp`, R6000-R6009 runtime errors, `_C_FILE_INFO=` → **Microsoft C, likely MSC 6.00A** (1990 runtime copyright fits 6.00/6.00A, not 7.0). Move MSC 6.00A to the top of the §2 candidate list; 7.0/VC 1.x are fallbacks.
- `This program requires an 80286` → `/G2`.
- EA library `c:\eaclib\%s` with function names in error strings: `unpacka`, `initmemman`, `emmcopybuf`, `reservemem`, `resizememblock`, `findmemblock`, `getmemblock` (EMS via `EMMXXXX0`). These are anchors: name each function from the xref to its string; EACLIB is likely shared with 95PC (check 95PC for the same names) and could be a separately compiled library (different flags) – treat as its own module set.

## 1. How NHL95PC works (what to reuse)

- Retail `HOCKEY.EXE` committed at root with size + SHA-1 in README/HANDOFF; `*.lst`, `build/`, `ref/`, `*.pkl` git-ignored.
- `tools/rebuild_exe.py extract|build|verify`: Python-only split of the EXE into parts (MZ stubs, LE header/tables JSON, fixups TSV, per-segment slices from `segmap95pc.json`) and byte-exact rebuild → `MATCH`.
- `src/`: one NASM file per segment (198 code / 106 data), linked by `tools/link_src.py`; `make` ends with MATCH; `tools/gen_src.py` / `asm_proto.py` generate asm from the `.lst`; `fixup_labels.py` turns fixups into labels.
- C matching: `wcc386` 10.0 LA run under headless DOSBox (`tools/wc10.sh`, `tools/cc.py check`), `tools/cdiff.py` per-function compare (capstone, fixups masked), `cverify.py`, `cc.py mark`, `CBUILD=1/0`, `make fullcheck`; progress via `tools/c_progress.py` → `C_PROGRESS.md`; failures logged in `docs/UNSURE.md`; `permute_decls.py`/`scope_decls.py` for register-pick near misses.
- Naming: `tools/matcher.py` + `sem_match.py` + `ref93_index.py`/`ref94_index.py` produce `name_map_94.csv` (name, source file, confidence, evidence); `manual_names.csv` overrides; `rename_symbol.py` renames across `src/` and must MATCH.
- Docs set: README, HANDOFF.md (setup, verify, current state, Next, Unsure), AGENTS.md, SEGMENT_AGENT.md, PROMPT.md, BUILD_NOTES.md, EXE_SEGMAP95PC.md, docs/C_MATCHING.md, docs/ASM_BUILD.md, docs/UNSURE.md, docs/SESSION_LOG.md.

Reuse as-is: doc structure, AGENTS/PROMPT rules (single agent, MATCH every commit, never force-push, UNSURE log, timeboxes), `lst_parse.py`/`lst.py`, `features.py`, `ref93_index.py`/`ref94_index.py`, `matcher.py`/`sem_match.py` scoring, `rename_symbol.py`, `c_progress.py`, the DOSBox headless harness pattern, the permuter idea.
Must be rewritten: `le_parse.py`/`rebuild_exe.py` (MZ + relocation table + overlay instead of LE/fixups), segmap, `link_src.py` (MZ relocs), `cdiff.py`/`cobj.py` (16-bit capstone mode, MSC OMF), `wc10.sh`/`cc.py` (new compiler).

## 2. Toolchain for 94 PC demo

1. Confirm compiler from strings/library: search EXE for `MS Run-Time Library`, `_C_FILE_INFO`, `R6000`-style runtime error messages (`R6001 - null pointer assignment` = MSC), Borland `Abnormal program termination`, or Watcom `WATCOM C/C++16`. Run IDA FLIRT names / `libmatch.py`-style module matching against MSC 7.0 `LLIBCE.LIB` and VC 1.0/1.5 `LLIBCE.LIB`.
2. Candidates in order: **MSC 7.0 (1992)**, **Visual C++ 1.0 (MSC 8.0, 1993)**, VC++ 1.5 (late 1993), Borland C++ 3.1 (fallback). Demo is late 1993, so MSC 7 / VC 1.0 most likely. Flags to sweep: `/AL /G2` (enter/leave), `/Gs` (stack checks off? look for `__chkstk` calls in prologues), `/Ox` vs `/Od` vs `/Os`, `/Zp1`/`/Zp2`, `/FPi` (emulator).
3. Confirm like 95PC did: hand-write 8 small leaf functions, compile with each candidate/flag set under DOSBox, compare bytes with relocations masked; record in `BUILD_NOTES.md` and `tools/cc_tests/sweep_*.txt`.
4. Assembler for byte-exact build: NASM (16-bit `bits 16`, segment-per-file) or JWasm/UASM (MASM syntax closer to IDA output). Linker: own Python MZ linker (like `link_src.py`), original `LINK.EXE` only later for C objects.
Timebox: 1 day to identify compiler+flags; if no candidate gives ≥6/8 exact, report back.

## 3. Repo bootstrap (mirror 95PC)

```
HOCKEY94DEMO.EXE        committed (size + SHA-1/256 in README/HANDOFF, like HOCKEY.EXE in 95PC)
README.md HANDOFF.md AGENTS.md PROMPT.md SEGMENT_AGENT.md BUILD_NOTES.md EXE_SEGMAP94PC.md
segmap94pc.json  name_map_95pc.csv  Makefile  build.sh
src/  (one .asm per segment seg000..seg091 + dseg; src/inc/symbols.inc; src/c/<seg>/<F>.c later)
tools/ (mz_parse.py, rebuild_exe.py, lst_parse.py, gen_src.py, link_src.py, matcher.py, xmatch95.py, cdiff.py, cc.py, rename_symbol.py, c_progress.py, compiler/ )
docs/  C_MATCHING.md ASM_BUILD.md UNSURE.md SESSION_LOG.md
.gitignore: *.lst, build/, ref/, tools/*.pkl
```
Steps: (a) `rebuild_exe.py verify`: split MZ header, relocation table, image, overlay/trailer; rebuild; SHA compare → MATCH. (b) generate per-segment asm from the `.lst`, relocations as symbolic `seg` refs; `make` → MATCH. (c) docs. The `.lst` stays ignored like 95PC (README tells how to make it); optionally keep Abdul's annotated `.lst` names extracted into `tools/manual_names.csv` so they aren't lost.

## 4. Naming by cross-reference

Byte matches to 95PC are ruled out (16-bit vs 32-bit compiler), so:
1. **Structural fingerprint** per function in both binaries: callee graph (ordered list of calls to already-named funcs), constant set (immediates ≥ 0x10, table sizes), string refs, basic-block count, loop shape, struct field offsets (scaled: 94PC fields are 16-bit, 95PC 32-bit; normalise via `struct_fieldmap.csv`).
2. Seed anchors: string xrefs (same message text in both EXEs), library/runtime, and Abdul's existing names. Propagate through the call graph (callers/callees of matched pairs), like 95PC `sem_match.py`.
3. **Exact within-16-bit matching** is still useful: opcode-hash with relocations masked to find duplicates inside the demo and, later, against retail 94 PC.
4. Names: take the 95PC name (which already carries 93G/94G provenance via `name_map_94.csv`); record source in `name_map_95pc.csv` (columns as 95PC: addr, name, source, confidence, evidence). Order: 93G → 94G names via 95PC, then 93S/94S names (`docs/history/name_map.csv`, `docs/name_map.csv` there) for SNES-port-only code (94 PC is a SNES port), then behaviour. Follow the clash rule and comment rules from NHL94Genesis HANDOFF.
5. Demo-only/front-end code (e.g. `displayDemoControls`) named from behaviour.

## 5. Order of work and timeboxes

1. Script-count funcs (named/sub_/lib) and confirm compiler strings — 1 h.
2. `rebuild_exe.py verify` MATCH — ½ day.
3. NASM per-segment build MATCH — 1-2 days.
4. Compiler + flags identification — 1 day cap.
5. Cross-ref naming pass vs 95PC (auto, then manual for high-value) — 2 days cap, then naming queue in SEGMENT_AGENT.md.
6. C matching: leaf functions first (no calls, < 64 bytes), then small callers, by size ascending; 10 min / 2 attempts per function, then UNSURE.md. Reuse 95PC C bodies as starting drafts (port int widths to 16-bit).
7. Permuter only after ≥50 matches show the main near-miss shape.

## 6. Risks / unknowns

- Compiler identity (MSC 7 vs VC 1.x vs Borland) and availability of the exact version + libs; possible runtime patch levels.
- Hand-written asm (blitters, sound, timer/keyboard ISRs) in a 16-bit DOS game is likely larger than in 95PC; mark as asm.
- MZ overlay/trailing data, packed/EXEPACK'd header? (check `e_cblp`, relocation count, overlay after image).
- Demo vs retail differences: code removed, names may not map 1:1; later retail 94 PC repo needed for full lineage.
- 16-bit vs 32-bit struct layouts make 95PC field maps only approximate.
- Abdul's expected "exact matches to 95PC" can only be source-level, not byte-level — confirm with him.
