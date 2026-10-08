#!/usr/bin/env python3
"""Deriva core-v14.gz de core-v13.gz por STREAM de cpio newc:
sustituye SOLO el contenido de 2 ficheros (bootsync.sh y el
default.script de udhcpc), conservando todas las demas entradas
byte a byte (modos setuid, owners, hardlinks, devices).
Necesario porque el arbol extraido tiene binarios sin permiso de
lectura (sudo 4111) que el cpio de filesystem no puede re-leer.
"""
import gzip, sys

SRC = "/home/hatch/workspace/flinux-jc/build/core-v13.gz"
DST = "/home/hatch/workspace/flinux-jc/isoroot-v14/boot/core.gz"
NEW_BOOTS = "/home/hatch/workspace/flinux-jc/build/rootfs-v14/opt/bootsync.sh"
NEW_SCRIPT = "/home/hatch/workspace/flinux-jc/build/rootfs-v14/usr/share/udhcpc/default.script"

raw = gzip.open(SRC, "rb").read()
newdata = {}
for p in (NEW_BOOTS, NEW_SCRIPT):
    with open(p, "rb") as f:
        newdata[p.split("rootfs-v14/")[1]] = f.read()

out = bytearray()
pos = 0
replaced = set()
names_seen = []
while True:
    hdr = raw[pos:pos+110]
    assert hdr[:6] == b"070701", (pos, hdr[:6])
    vals = [int(hdr[6+i*8:14+i*8], 16) for i in range(13)]
    (ino, mode, uid, gid, nlink, mtime, fsize,
     maj, mino, rmaj, rmin, namesize, check) = vals
    name = raw[pos+110:pos+110+namesize-1].decode()
    names_seen.append(name)
    head_len = 110 + namesize
    head_pad = (4 - (head_len % 4)) % 4
    data_start = pos + head_len + head_pad
    data = raw[data_start:data_start+fsize]
    data_pad = (4 - (fsize % 4)) % 4
    end = data_start + fsize + data_pad
    if name == "TRAILER!!!":
        out += raw[pos:end]
        pos = end
        break
    key = name[2:] if name.startswith("./") else name
    if key in newdata and nlink == 1:
        nd = newdata[key]
        nh = list(vals)
        nh[6] = len(nd)
        nhdr = b"070701" + b"".join(b"%08x" % v for v in nh)
        out += nhdr + raw[pos+110:data_start]
        out += nd + b"\x00" * ((4 - (len(nd) % 4)) % 4)
        replaced.add(key)
        print(f"sustituida {name}: {fsize} -> {len(nd)} bytes (mode {mode:06o})")
    else:
        out += raw[pos:end]
    pos = end

assert replaced == set(newdata), (replaced, set(newdata))
with gzip.open(DST, "wb", compresslevel=9) as g:
    g.write(bytes(out))
print("OK ->", DST)
