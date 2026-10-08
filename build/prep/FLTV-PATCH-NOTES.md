# FLTV-PATCH-NOTES — Lista de canales LOCAL (flinux-jc)

**Paquete:** `fltv.tcz` (28,672 bytes; md5 `01ff29fd2fb4f75e23499dec384a921a`) — reemplaza al `fltv` del repo.
**Binario:** `usr/local/bin/fltv`, ELF 32-bit LSB executable Intel 80386, 53,164 bytes stripped
(original: 71,592 bytes). Estructura del `.tcz` idéntica a la original:
`usr/local/bin/fltv`, `usr/local/bin/fltv-open`, `usr/local/share/applications/fltv.desktop`,
`usr/local/share/pixmaps/fltv.png` (los tres últimos, copiados byte a byte del paquete original).

## 1. El parche (src/backend.c, +49 líneas, solo adiciones)

Problema confirmado en el código: `online_m3u_load()` («M3U → En Línea») descargaba SIEMPRE
`URL_CH` (channels.json de GitLab) y la fusión de `listas/*.m3u` vía `URL_REPO_TREE`; el
`channels.json` local nunca se leía. La pestaña «Local» de la GUI es un texto «Proximamente…».

Cambios, todos en `src/backend.c` justo antes de `online_m3u_load()`:

1. Nueva función estática `try_load_local_channels()`:
   - Lee `$HOME/.config/fltv/channels.json` (nuevo `#define CH_LOCAL_FILE "/.config/fltv/channels.json"`).
   - Lee el archivo completo (límite 64 MB), lo parsea con json-c exigiendo array JSON.
   - Por cada entrada con `name` y `url` no vacíos llama a `m3u_add(name, url, category| "General", logo)`
     — exactamente el mismo formato y semántica que la rama de descarga de `URL_CH`.
   - Devuelve cuántos canales añadió; respeta la cancelación por generación (`*gen_ptr != my_gen`).
2. `online_m3u_load()` nuevo arranque (antes del cuerpo original, sin tocarlo):
   ```c
   if (status_cb) status_cb("Cargando lista local...");
   int local = try_load_local_channels(gen_ptr, my_gen);
   if (*gen_ptr != my_gen) return;
   if (local > 0) return;
   /* ... código original de descarga intacto ... */
   ```
   Si no hay archivo, o está vacío/corrupto, o tiene 0 canales válidos → comportamiento
   original intacto (descarga de `URL_CH` + `URL_REPO_TREE`). GUI y cuentas Xtream sin cambios.

El estado visible pasa a «Cargando lista local...» y, al terminar, el contador normal
«N canales en linea». Diff completo del fuente en el árbol de build (`git diff src/backend.c`
sobre https://gitlab.com/AnddyCort/fltv @ HEAD clonado 2026-10-04).

## 2. Método de compilación (i386, sin apt)

El host no ejecuta binarios de 32 bits (segfault incluso con hello-world vía loader/chroot),
así que se reutilizó la vía probada de TCWire: **Zig 0.16.0** como compilador cruzado
(`~/workspace/tcwire/tools/zig-x86_64-linux-0.16.0/zig`), `zig cc/c++ -target x86-linux-gnu`:

- Headers: FLTK 1.3 + X11 de `~/workspace/tcwire/dl/` (fltk-headers, x11-headers,
  stdcpp9-dev-i386), libcurl 8.5.0 (github curl `curl-8_5_0`), json-c 0.17 (github json-c,
  con `json.h`/`json_config.h` generados desde sus `.in`).
- Librerías i386 enlazadas: las de los `.tcz` reales de TinyCore 17.1
  (`~/workspace/flinux-jc/optional/`: fltk-1.3, curl, json-c, libX11, libXext, libXcursor,
  libpng, libjpeg-turbo) + zlib/libstdc++ del rootfs base TC 17.1.
- Flags del Makefile original: `-O2 -std=c++11 -fno-rtti -fno-exceptions`,
  RUNPATH `/usr/local/lib`, enlace con `--start-group`.

**Estático/dinámico:** el binario ORIGINAL resultó ser *dinámico* en FLTK (NEEDED
`libfltk.so.1.3`, `libfltk_images.so.1.3`; la hipótesis «estático» era falsa), así que se
compiló igual: dinámico. NEEDED del nuevo binario: `libstdc++.so.6`, `libfltk_images.so.1.3`,
`libfltk.so.1.3`, `libcurl.so.4`, `libjson-c.so.2`, `libc.so.6` (el resto llega transitivo,
igual que en el original). Exige máx. `GLIBC_2.34` y `GLIBCXX_3.4`; el rootfs TC 17.1
provee hasta `GLIBC_2.42` — compatible.

## 3. `fltv.tcz.dep`

```
fltk-1.3.tcz
curl.tcz
json-c.tcz
mplayer-cli.tcz
```

El original trae solo las últimas tres; se añade `fltk-1.3.tcz` porque el binario (original
y parcheado) enlaza FLTK dinámico y el `.dep` debe declarar las dependencias reales. Si el
sistema ya lo tiene cargado, `tce-load` lo da por satisfecho.

## 4. Verificación (qemu-i386-static 7.2.22, sysroot = rootfs TC 17.1 + `.tcz` reales)

- `file`/`readelf`: ELF 32-bit LSB, Intel 80386, intérprete `/lib/ld-linux.so.2`, RUNPATH
  `/usr/local/lib` — igual que el original. El binario dentro del `.tcz` es byte-idéntico al
  compilado (`cmp` OK); `md5sum -c fltv.tcz.md5.txt` OK.
- **ldd completo, 0 «not found»** (26 librerías resueltas: fltk, fltk_images, curl, json-c,
  stdc++, X11/Xext/Xcursor/Xrender/Xfixes/xcb/Xau/Xdmcp, png, jpeg, ssl, crypto, zstd…),
  verificado con el loader 32-bit bajo qemu sobre el sysroot TC.
- **Harness headless** (test C enlazado solo con el backend parcheado, ejecutado bajo qemu):
  - Caso A — `HOME` con `.config/fltv/channels.json` (el de `prep/fltv/`, 500 canales):
    `RESULT n=500`, primer canal «Canal Caribe | Cuba», **sin descargas**. El mismo harness
    con el backend ORIGINAL en idénticas condiciones: `n=0` (ignora el local y la red no
    responde en el sandbox) → la diferencia es solo el parche.
  - Caso B — sin archivo local: `n=0`, exit limpio, sin crash (cae al código original de red).
  - Caso C — JSON corrupto: `n=0`, exit limpio, sin crash (mismo camino).
- **Arranque GUI headless:** parcheado y original idénticos — `Can't open display: `, exit 1
  (sin X, esperado; confirma enlace y arranque sin cuelgues).

## 5. Tamaños

| Artefacto | Bytes |
|---|---|
| fltv.tcz parcheado | 28,672 |
| fltv.tcz original (repo) | 36,864 |
| fltv parcheado (stripped) | 53,164 |
| fltv original (stripped) | 71,592 |

Nota de despliegue: el `.tcz` no incluye `channels.json`/`accounts.json` (misma estructura
que el original); esos van instalados en el `$HOME` del usuario (`~/.config/fltv/`), como ya
está previsto en `prep/fltv/`.
