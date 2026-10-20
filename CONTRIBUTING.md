# Contributing
- `main` only takes byte-identical changes: `python3 tools/rebuild_exe.py verify` (and later `make`) must print MATCH before every commit.
- Small commits; never force-push. One agent at a time.
- Names: 95PC name (93G -> 94G provenance), then 93S/94S, then behaviour, with evidence. Clash rule: never reuse a name for a different item. Record renames in `docs/name_map.csv`.
- Comments: no IDA artefacts (sub_, loc_), no hardcoded addresses outside headers; every function gets a header comment (what, args, result).
- Failed matching attempts go in `docs/UNSURE.md`; never retry a listed shape.
- Do not commit `*.lst`, `build/`, `ref/`.
