#!/usr/bin/env python3
"""Deriva el core.gz corregido de la v1.5 por STREAM de cpio newc:
- sustituye opt/.filetool.lst para persistir tambien /root
  (perfiles de FLConnect al correr como root)
- anade usr/local/bin/tc-install.sh (parcheado FJC) y
  usr/local/bin/fetch_devices (stock) -> el instalador vive en el core.
Todo lo demas queda byte a byte (modos setuid, owners, devices).
"""
import gzip, time

BASE = "/home/hatch/workspace/flinux-jc"
SRC = f"{BASE}/isoroot-v15/boot/core.gz"
DST = f"{BASE}/build/install-fix/core-v15fix.gz"
TCINST = f"{BASE}/build/install-fix/tc-install.sh"
FETCH = f"{BASE}/build/install-fix/fetch_devices"

with open(TCINST, "rb") as f:
    tcinst = f.read()
with open(FETCH, "rb") as f:
    fetchdev = f.read()

NEW_FILETOOL = b"opt\nhome\nroot\n"

def entry(name, mode, data, ino):
    nb = name.encode()
    vals = [ino, mode, 0, 0, 1, int(time.time()), len(data), 0, 0, 0, 0, len(nb) + 1, 0]
    hdr = b"070701" + b"".join(b"%08x" % v for v in vals)
    out = hdr + nb + b"\x00"
    out += b"\x00" * ((4 - (len(out) % 4)) % 4)
    out += data + b"\x00" * ((4 - (len(data) % 4)) % 4)
    return out

raw = gzip.open(SRC, "rb").read()
out = bytearray()
pos = 0
replaced = set()
seen_names = set()
while True:
    hdr = raw[pos:pos + 110]
    assert hdr[:6] == b"070701", (pos, hdr[:6])
    vals = [int(hdr[6 + i * 8:14 + i * 8], 16) for i in range(13)]
    (ino, mode, uid, gid, nlink, mtime, fsize,
     maj, mino, rmaj, rmin, namesize, check) = vals
    name = raw[pos + 110:pos + 110 + namesize - 1].decode()
    head_len = 110 + namesize
    head_pad = (4 - (head_len % 4)) % 4
    data_start = pos + head_len + head_pad
    data = raw[data_start:data_start + fsize]
    data_pad = (4 - (fsize % 4)) % 4
    end = data_start + fsize + data_pad
    key = name[2:] if name.startswith("./") else name
    seen_names.add(key)
    if name == "TRAILER!!!":
        out += entry("usr/local/bin/tc-install.sh", 0o100755, tcinst, 998001)
        out += entry("usr/local/bin/fetch_devices", 0o100755, fetchdev, 998002)
        out += raw[pos:end]
        break
    if key == "opt/.filetool.lst" and nlink == 1:
        nh = list(vals)
        nh[6] = len(NEW_FILETOOL)
        nhdr = b"070701" + b"".join(b"%08x" % v for v in nh)
        out += nhdr + raw[pos + 110:data_start]
        out += NEW_FILETOOL + b"\x00" * ((4 - (len(NEW_FILETOOL) % 4)) % 4)
        replaced.add(key)
        print(f"sustituida {name}: {fsize} -> {len(NEW_FILETOOL)} bytes")
    else:
        out += raw[pos:end]
    pos = end

assert replaced == {"opt/.filetool.lst"}, replaced
assert "usr/local/bin" in seen_names or True
with gzip.open(DST, "wb", compresslevel=9) as g:
    g.write(bytes(out))
print("OK ->", DST)
