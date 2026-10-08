#!/usr/bin/env python3
"""Deriva core.gz de la v1.5 desde el de la v1.4 por STREAM de cpio newc:
- sustituye etc/skel/.conkyrc (cabecera con fecha/hora numericas)
- anade usr/share/zoneinfo/America/Havana (zonefile) y el enlace
  etc/localtime -> /usr/share/zoneinfo/America/Havana
Todo lo demas queda byte a byte (modos setuid, owners, hardlinks, devices).
"""
import gzip, time

BASE = "/home/hatch/workspace/flinux-jc"
SRC = f"{BASE}/isoroot-v14/boot/core.gz"
DST = f"{BASE}/isoroot-v15/boot/core.gz"
CONKY = f"{BASE}/tmp-v15work/v15f/etc/skel/.conkyrc"
ZONE = f"{BASE}/tmp-v15work/v15f/usr/share/zoneinfo/America/Havana"

with open(CONKY, "rb") as f:
    new_conky = f.read()
with open(ZONE, "rb") as f:
    zone_data = f.read()

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
    if name == "TRAILER!!!":
        out += entry("usr/share/zoneinfo", 0o040755, b"", 999003)
        out += entry("usr/share/zoneinfo/America", 0o040755, b"", 999004)
        out += entry("usr/share/zoneinfo/America/Havana", 0o100644, zone_data, 999001)
        out += entry("etc/localtime", 0o120777, b"/usr/share/zoneinfo/America/Havana", 999002)
        out += raw[pos:end]
        break
    key = name[2:] if name.startswith("./") else name
    if key == "etc/skel/.conkyrc" and nlink == 1:
        nh = list(vals)
        nh[6] = len(new_conky)
        nhdr = b"070701" + b"".join(b"%08x" % v for v in nh)
        out += nhdr + raw[pos + 110:data_start]
        out += new_conky + b"\x00" * ((4 - (len(new_conky) % 4)) % 4)
        replaced.add(key)
        print(f"sustituida {name}: {fsize} -> {len(new_conky)} bytes")
    else:
        out += raw[pos:end]
    pos = end

assert replaced == {"etc/skel/.conkyrc"}, replaced
with gzip.open(DST, "wb", compresslevel=9) as g:
    g.write(bytes(out))
print("OK ->", DST)
