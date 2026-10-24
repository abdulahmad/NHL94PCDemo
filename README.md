# NHL 94 PC Demo

> **Work in progress:** bootstrap stage. Layout and docs follow [NHL95PC](https://github.com/abdulahmad/NHL95PC).

Bitwise rebuild (then matching C decompilation) of the DOS demo of NHL Hockey 94 (`HOCKEY94DEMO.EXE`, EA Sports). The demo is cut down from retail, so it is the easier first target. **Picking this up? Start with [docs/HANDOFF.md](docs/HANDOFF.md).**

`HOCKEY94DEMO.EXE` is a **16-bit real-mode MS-DOS MZ executable** (large model, 286+), built with **Microsoft C** (runtime string `MS Run-Time Library - Copyright (c) 1990, Microsoft Corp`, R6000-R6009, `_C_FILE_INFO=`; most likely MSC 6.00A, `/AL /G2`) and linked with EA's `EACLIB` library (`c:\eaclib\%s`; EMS memory manager). It is not a Watcom/DOS4GW LE like NHL 95 PC, so the 95 PC compiler does not apply.

Lineage: 94 PC is a port of NHLPA 93 SNES / NHL 94 SNES (93S from 92/93 Genesis, 94S from 93S + 94G). NHL 95 PC derives from 94 PC plus 94/95 Genesis. **Names: 95PC name (which carries 93G/94G), then 93S/94S, then behaviour.**

## Retail EXE

| | |
| --- | --- |
| File | `HOCKEY94DEMO.EXE` (to be committed at repo root) |
| SHA-256 | `8a6262bdb40c3eace3dd3a061f56a1a2be073738b27f9b2c3c7ef6ae973687f2` |
| MD5 | `cd60da303e5c7e3be874d0abc7ac340b` |

`.gitignore` keeps the IDA listing (`*.lst`), `build/` and `ref/` out of commits.

## Byte-exact rebuild from the EXE's own parts

Python 3 only:
```
python3 tools/rebuild_exe.py extract   # split into build/parts/ (MZ header, relocs, image, overlay)
python3 tools/rebuild_exe.py build     # rebuild build/HOCKEY94DEMO.EXE from build/parts/
python3 tools/rebuild_exe.py verify    # extract + build + compare; prints MATCH
```

## AI assistance

This project is AI-assisted. The work is directed by a strict ruleset and curated by hand, with the aim of producing correctly labelled and commented code that matches the spirit of what the original source code would have been. We can't guarantee it's perfect, and ultimately this will always be a work in progress. If you see something that needs fixing, raise an issue, or even better, raise a PR.

## Docs
* [docs/HANDOFF.md](docs/HANDOFF.md): setup, verify, current state, next
* [PROMPT.md](PROMPT.md): session prompt
* [CONTRIBUTING.md](CONTRIBUTING.md): rules
* [docs/PLAN.md](docs/PLAN.md): full project plan

Sister projects: [NHL95PC](https://github.com/abdulahmad/NHL95PC), [NHLPA93SNES](https://github.com/abdulahmad/NHLPA93SNES), [NHL94SNES](https://github.com/abdulahmad/NHL94SNES), [NHL94Genesis](https://github.com/abdulahmad/NHL94Genesis), [NHLPA93Genesis](https://github.com/abdulahmad/NHLPA93Genesis).
