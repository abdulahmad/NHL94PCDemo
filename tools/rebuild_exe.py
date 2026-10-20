#!/usr/bin/env python3
"""Split HOCKEY94DEMO.EXE (16-bit MZ) into parts and rebuild it byte-exact.

  python3 tools/rebuild_exe.py extract [EXE]  # -> build/parts/
  python3 tools/rebuild_exe.py build          # build/parts/ -> build/HOCKEY94DEMO.EXE
  python3 tools/rebuild_exe.py verify [EXE]   # extract + build + compare, prints MATCH

Parts: header.json (MZ fields), header_extra.bin (bytes between the fixed
28-byte header and the end of the header paragraphs, minus the relocation
table), relocs.tsv (seg:off pairs), image.bin (load module), overlay.bin
(anything after the MZ image size, e.g. debug info or packed data).
"""
import hashlib, json, os, struct, sys

EXPECTED_SHA256 = "8a6262bdb40c3eace3dd3a061f56a1a2be073738b27f9b2c3c7ef6ae973687f2"  # from the IDA listing header
FIELDS = ["e_magic", "e_cblp", "e_cp", "e_crlc", "e_cparhdr", "e_minalloc", "e_maxalloc",
          "e_ss", "e_sp", "e_csum", "e_ip", "e_cs", "e_lfarlc", "e_ovno"]
PARTS = "build/parts"


def image_size(h):
    n = h["e_cp"] * 512
    if h["e_cblp"]:
        n -= 512 - h["e_cblp"]
    return n


def extract(exe):
    d = open(exe, "rb").read()
    sha = hashlib.sha256(d).hexdigest()
    print(f"{exe}: {len(d)} bytes sha256 {sha}" + ("" if sha == EXPECTED_SHA256 else "  (NOT the listed demo EXE)"))
    h = dict(zip(FIELDS, struct.unpack_from("<14H", d, 0)))
    if h["e_magic"] not in (0x5A4D, 0x4D5A):
        sys.exit("not an MZ executable")
    hdr_len = h["e_cparhdr"] * 16
    rel_off, n = h["e_lfarlc"], h["e_crlc"]
    relocs = [struct.unpack_from("<HH", d, rel_off + 4 * i) for i in range(n)]
    extra = bytearray(d[28:hdr_len])  # rel table zeroed; restored from relocs.tsv
    a, b = rel_off - 28, rel_off - 28 + 4 * n
    if a < 0 or b > len(extra):
        sys.exit("relocation table outside header")
    extra[a:b] = bytes(b - a)
    end = image_size(h)
    os.makedirs(PARTS, exist_ok=True)
    json.dump(h, open(f"{PARTS}/header.json", "w"), indent=1)
    open(f"{PARTS}/header_extra.bin", "wb").write(extra)
    with open(f"{PARTS}/relocs.tsv", "w") as f:
        f.write("".join(f"{o:04X}\t{s:04X}\n" for o, s in relocs))
    open(f"{PARTS}/image.bin", "wb").write(d[hdr_len:end])
    open(f"{PARTS}/overlay.bin", "wb").write(d[end:])
    print(f"header {hdr_len} B, {n} relocs, image {end - hdr_len} B, overlay {len(d) - end} B, "
          f"entry {h['e_cs']:04X}:{h['e_ip']:04X}, stack {h['e_ss']:04X}:{h['e_sp']:04X}")
    return d


def build(out="build/HOCKEY94DEMO.EXE"):
    h = json.load(open(f"{PARTS}/header.json"))
    extra = bytearray(open(f"{PARTS}/header_extra.bin", "rb").read())
    relocs = [tuple(int(x, 16) for x in l.split()) for l in open(f"{PARTS}/relocs.tsv") if l.strip()]
    image = open(f"{PARTS}/image.bin", "rb").read()
    overlay = open(f"{PARTS}/overlay.bin", "rb").read()
    h["e_crlc"] = len(relocs)
    a = h["e_lfarlc"] - 28
    extra[a:a + 4 * len(relocs)] = b"".join(struct.pack("<HH", o, s) for o, s in relocs)
    hdr = struct.pack("<14H", *[h[k] for k in FIELDS]) + bytes(extra)
    total = len(hdr) + len(image)
    h["e_cp"], h["e_cblp"] = (total + 511) // 512, total % 512
    hdr = struct.pack("<14H", *[h[k] for k in FIELDS]) + bytes(extra)
    d = hdr + image + overlay
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "wb").write(d)
    return d


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "verify"
    exe = sys.argv[2] if len(sys.argv) > 2 else "HOCKEY94DEMO.EXE"
    if cmd == "extract":
        extract(exe)
    elif cmd == "build":
        build()
    elif cmd == "verify":
        orig = extract(exe)
        new = build()
        if new == orig:
            print("MATCH: build/HOCKEY94DEMO.EXE is byte-identical to", exe)
        else:
            i = next((i for i, (x, y) in enumerate(zip(orig, new)) if x != y), min(len(orig), len(new)))
            sys.exit(f"MISMATCH at offset 0x{i:X} (sizes {len(orig)} vs {len(new)})")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
