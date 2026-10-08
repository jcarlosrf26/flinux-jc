# INFORME — flinux-jc

**Fecha:** 2026-10-04
**Entregable:** `flinux-jc.iso` — 216,006,656 bytes — MD5 `e9be72b618cb09144b90bc77b080d0b2` (verificado con `md5sum -c`)
**Base:** Tiny Core Linux 17.1 x86 (32 bits), estilo CorePlus (arranque `cde`, extensiones en la ISO, sin necesitar red para instalar), kernel **6.18.35-tinycore** stock, sin recompilar. Objetivo: Dell Inspiron 1545 (BCM4312 LP-PHY, Intel GMA 4500MHD, Intel HDA, ethernet Broadcom).

---

## 1. Qué contiene

- **Escritorio:** Xorg-7.7 (+ xorg-server, driver `xf86-video-intel` para la GMA 4500MHD), FLWM topside y wbar, como FLinux. Aterm, fluff (archivos), beaver (editor).
- **190 extensiones** en `cde/optional` (set completo con dependencias), cargadas en el arranque desde la ISO.
- **Audio:** ALSA completo (`alsa`, `alsa-config`, módulos del kernel, `libasound`) listo para Intel HDA. `alsa.tcz` de TC 17 incluye alsa-utils (`aplay`, `alsamixer`), por eso no existe un `alsa-utils.tcz` separado en el repo.
- **FLRadio** (repo FLinux) con la lista de emisoras **ya cargada**: `~/webstations.lst` con **216 emisoras en 15 secciones** (formato nativo de FLRadio).
- **FLTV 2.1.0 parcheado** (ver §5) con **500 canales** precargados desde `~/.config/fltv/channels.json` (iptv-org, selección LatAm/España/Cuba, sin credenciales de terceros: `accounts.json` vacío).
- **FLTube 2.2.0** del repo FLinux (con yt-dlp 2026.08.19, python3.11, ffmpeg4, mplayer-cli).
- **FLConnect 1.0-4** preinstalado como extensión de arranque: paquete autocontenido verificado de `flconnect-full` (binario setuid root, wg/wg-quick, openvpn, resolvconf, firmware b43), con copia de permisos internos normalizados (ver §6).
- **Drivers Dell 1545:** `b43.ko.gz` + firmware LP-PHY completo (`ucode15.fw` y 154 ficheros más en `/usr/local/lib/firmware/b43/`), `i915.ko.gz`, `snd_hda_intel`, `tg3`, wireless extensions del kernel, `wireless_tools` (`iwconfig`) y `wpa_supplicant-dbus`.
- **Repositorio por defecto:** `https://flinux.loc-os.com/` en `/opt/tcemirror` (tce-load y Apps apuntan al repo FLinux 17.x x86; verificado: el repo servía 2804 extensiones y responde HTTPS 200).
- **Tema de iconos:** Adwaita (paquete `adwaita-icon-theme`, configurado en GTK2 y GTK3).
- **Fondo de pantalla:** logo oficial de FLinux derritiéndose en lava volcánica, 1366×768, como fondo por defecto.
- **Nombre de la versión:** ISO `flinux-jc`, etiqueta de arranque «flinux-jc» y hostname **flinux-jc**.
- **Navegador: NINGUNO** (por decisión del usuario; ver §5).

## 2. Cómo se construyó

- Remaster tipo CorePlus sobre `CorePlus-17.1.iso` (ISO base verificada por MD5): rootfs `core.gz` reempaquetado con el mirror, el hostname, el firmware b43, el fondo y el esqueleto de usuario (lista de radio, canales de TV, tema).
- Descarga recursiva de extensiones desde el repo FLinux (resolver propio, sustitución `KERNEL`→`6.18.35-tinycore`, 0 fallos).
- ISO híbrida El Torito construida con xorriso.
- Verificación con una variante gemela de desarrollo (idéntico contenido + consola serie para diagnóstico); la ISO entregada **no** lleva esa consola.

## 3. Verificado de verdad (QEMU i386: Intel HDA emulada, e1000+DHCP, 1024 MB)

Capturas en `~/workspace/flinux-jc/shots/`:

| Comprobación | Resultado | Evidencia |
|---|---|---|
| Arranque completo al escritorio FLWM+wbar con el fondo de lava | ✅ | `shots/finalC.png` |
| Carga de las 190 extensiones sin errores de permisos | ✅ | consola de arranque limpia |
| hostname = `flinux-jc` | ✅ | «Setting hostname to flinux-jc Done» + prompt |
| Menú FLWM Applications con FLConnect, FLTV, FLTube, Flradio, Terminal, beaver, fluff | ✅ | `ls ~/.wmx/Applications` |
| FLRadio abre y carga sus 216 emisoras | ✅ | `shots/app-flradio.png` |
| FLTV (parcheado) abre y muestra **«500 canales en línea»** con categorías LatAm desde la lista local | ✅ | `shots/app-fltv5.png` |
| FLTube 2.2.0 abre su ventana principal (yt-dlp 2026.08.19 responde) | ✅ | `shots/app-fltube3.png` |
| FLConnect abre su GUI completa (ON/OFF, Importar WireGuard/OpenVPN) | ✅ | `shots/app-flconnect.png` |
| ALSA detecta la HDA emulada: `aplay -l` → `card 0: Intel [HDA Intel]` | ✅ | salida serie |
| Módulos `snd_hda_intel` cargados; `b43.ko.gz` e `i915.ko.gz` presentes para 6.18.35 | ✅ | `lsmod` / rutas en tcloop |
| Firmware `ucode15.fw` en `/usr/local/lib/firmware/b43/` | ✅ | `ls` |
| Kernel `6.18.35-tinycore`; `/opt/tcemirror` = `https://flinux.loc-os.com/` | ✅ | serie |
| `iwconfig` y `wpa_supplicant` instalados | ✅ | serie |
| Sin navegador: 0 rastros de SeaMonkey | ✅ | serie |
| Tamaño y MD5 de la ISO | ✅ | 216,006,656 B, `md5sum -c` OK |

## 4. Lo que NO se pudo verificar (y por qué)

- **WiFi real en la Dell:** imposible en QEMU (no emula la BCM4312). Sí verificado: módulo b43 del kernel correcto, firmware LP-PHY en su sitio y herramientas de conexión. En la Dell, `lsmod` debería mostrar b43 cargado al detectar la tarjeta; la prueba real es suya.
- **Gráfica GMA 4500MHD real:** QEMU usa VGA estándar; el módulo i915 y el driver Xorg intel están incluidos (son los que FLinux usa para este chip).
- **Consulta en línea del mirror con `tce-load`, reproducción de streams de radio/TV y búsqueda de FLTube:** la VM de este banco de pruebas no tiene salida a Internet (todo el egreso del host pasa por un proxy HTTP autenticado que no se puede pasar al invitado), así que DNS/Internet del invitado no existe aquí. Sí verificado: la red local del invitado funciona (DHCP, IP 10.0.2.15, gateway), la configuración del mirror es la correcta y el servidor `flinux.loc-os.com` responde 200 en la ruta exacta que usa tce-load (`/17.x/x86/tcz/...`) hoy desde el host. Las listas de radio y TV están precargadas en la ISO, por lo que no dependen de la red para cargarse.
- Tampoco se probó la instalación en disco (arranque live + modo `cde` es el diseño pedido); CorePlus conserva sus ficheros `.instlist` de stock por si se quiere instalar con la herramienta de TC.

## 5. Desviaciones respecto a la especificación inicial

1. **Navegador: ninguno.** Se había empaquetado SeaMonkey 2.53.21 oficial i686 (la actual 2.53.24 ya es solo x86_64; upstream abandonó i686 en esa versión, verificado por HEAD 404) y se verificó con `--version` en un sysroot TC, pero el usuario decidió que la ISO quede **sin navegador**: se retiró de la ISO junto con sus dependencias exclusivas (gtk3, dbus-glib, libXcomposite, libxkbcommon, at-spi2-core). Los artefactos quedan en `build/prep/` por si se quiere añadir después.
2. **FLTV parcheado, no el binario tal cual del repo.** El FLTV 2.1.0 original **ignora cualquier lista local**: descarga siempre sus canales del GitLab de su autor (verificado en su código, `src/backend.c`) y la pestaña «Local» dice «Proximamente…». Para cumplir «lista de GitHub configurada», se recompiló 2.1.0 (i386, mismo empaquetado) con un parche aditivo mínimo: primero intenta leer `~/.config/fltv/channels.json` local (500 canales de iptv-org en formato nativo) y solo si falta descarga, con el comportamiento original intacto. Detalle completo en `build/prep/fltv-patched/FLTV-PATCH-NOTES.md`. Nota: FLTV no respeta `http-referrer`/user-agent de iptv-org, así que algunos streams concretos pueden fallar en reproducción (en la muestra del investigador, 3/6 OK); eso es una limitación del reproductor (mplayer), no de la lista.
3. **Lista de radio de junguler, no de iptv-org.** iptv-org ya no mantiene listas de radio (su `categories/radio.m3u` devuelve 404, verificado): hoy es solo TV. Se usó el repo de GitHub **junguler/m3u-radio-music-playlists** (streams comprobados uno a uno: las 216 finales respondían; muestra 10/10 HTTP 200). Cuba solo incluyó 3 emisoras porque las estatales `icecast.teveo.cu` no respondieron desde esta red (posible geo-restricción; documentado en `radio-NOTES.md`).
4. **Tema Adwaita en vez de Papirus:** Papirus no existe en el repo TC 17.x x86. Adwaita 3.16.2 es la alternativa moderna disponible y quedó configurado en GTK2/GTK3.
5. **Herramienta de fondo propia (`flbg`) en vez de `hsetroot`:** en este sistema, Imlib2 no carga ninguna imagen (`hsetroot` devuelve «Bad image» incluso con los PNG del propio sistema y `imlib2_conv` falla con Error 3, con loaders presentes y enlazados). Se escribió `flbg` (C, solo libX11, lee un BMP 24-bit y fija el pixmap raíz con escala «cover»), compilado i386 y verificado fijando el fondo real. Código en `build/flbg.c`; la imagen se guarda como `flinux-lava.bmp` en `/opt/backgrounds/`. El fondo es el logo oficial de FLinux (de la web de plantillas de FLinux) derretido en lava.
6. **Hostname vía `bootsync.sh`:** TC fija el hostname con `/usr/bin/sethostname box` en cada arranque, ignorando `/etc/hostname`; se cambió esa llamada a `flinux-jc` (y se dejó `/etc/hostname` coherente).

## 6. Avisos importantes

- **El `flconnect.tcz` original de `~/workspace/flconnect-full/` tiene los directorios internos del squashfs con modo 2770 (root:nogroup).** Dentro de esta ISO va una **copia saneada** (directorios 755, binario setuid 4755 intacto, MD5 `36ccba67407db60cb8422af8a67addc9`). Si el paquete suelto de `flconnect-full` se instala en la Dell con `tce-load -i` como usuario `tc`, puede fallar igual que falló aquí («Permission denied» al copiar desde el loop). Conviene aplicar el mismo saneado al paquete suelto o instalarlo como root. (El `fltv.tcz` parcheado recibió el mismo saneado: MD5 `66a26057a636c8fe3ade94e0894d46ad`.)
- La ISO es híbrida (grabable en USB con `dd`) y arranca en modo live `cde`: todo el sistema funciona desde la propia ISO sin disco.
- Primera conexión recomendada en la Dell: por cable (tg3) para probar `tce-load` y las apps con red; después el WiFi con FLConnect/`wpa_supplicant`.

## 7. Ficheros de trabajo

- `~/workspace/flinux-jc/flinux-jc.iso` + `flinux-jc.iso.md5.txt` — entregable.
- `~/workspace/flinux-jc/INFORME.md` — este informe.
- `~/workspace/flinux-jc/shots/` — capturas de verificación.
- `~/workspace/flinux-jc/build/` — scripts de construcción/control (`qctl.py`, `ser.py`, `resolve.py`) y código (`flbg.c`), notas de subagentes en `build/prep/` (`radio-NOTES.md`, `fltv-NOTES.md`, `FLTV-PATCH-NOTES.md`, `SEAMONKEY-NOTES.md`, `wallpaper-NOTES.md`, listas y paquetes intermedios).
- `~/workspace/flinux-jc/isoroot/` y `~/workspace/flinux-jc/build/core2/` — árbol de la ISO y del rootfs (fuente de verdad para remasters futuros; `build/core2/etc/inittab` **no** contiene la línea serie de diagnóstico).

---

## 8. v1.1 (2026-10-04) — Arreglo del audio al arrancar

**Problema reportado:** Juanca probó la v1.0 en la Dell 1545 real: «el audio no me arranca de inicio». Su `aplay -l` mostraba la tarjeta bien detectada (card 0 Intel [HDA Intel], device 0: 92HD71B7X Analog, device 1: 92HD71B7X Digital), es decir, driver y hardware correctos: el fallo era el **estado del mezclador ALSA al arrancar** (Tiny Core deja los canales en silencio `[off]` o a 0 por defecto).

**Cambio (único fichero tocado):** `/opt/bootsync.sh` del core.gz. Al final se añade un bloque en segundo plano que, en cada boot y ya cargadas las extensiones: espera (máx. ~10 s) a que exista `/dev/snd/controlC0`, ejecuta `alsactl init 0` y desmutea al 80 % los controles Master, PCM, Speaker y Headphone con `amixer -c 0 sset … 80% unmute` (cada línea tolera que el control no exista). Verificado por comparación de árboles: el core de la v1.1 difiere del de la v1.0 **solo** en `opt/bootsync.sh`. Se empaquetó desde `build/core2` (sin la consola serie de `core2dev`) y la ISO se reconstruyó con xorriso (El Torito e isohybrid idénticos a la v1.0).

**Entregable:** `flinux-jc-v1.1.iso` — 216,006,656 bytes — MD5 `bff2a650f54935dee7191751fc4966e0` (+ `flinux-jc-v1.1.iso.md5.txt`). Mismo tamaño exacto que la v1.0.

**Verificación (QEMU i386, Intel HDA emulada, sobre la ISO v1.1 entregable, sin tocar el mezclador a mano):**

| Comprobación | Resultado | Evidencia |
|---|---|---|
| `aplay -l` ve la HDA | ✅ `card 0: Intel [HDA Intel], device 0: Generic Analog [Generic Analog]` | `shots/v11-aplay2.png` |
| `amixer -c 0 sget Master` >0 y `[on]` solo al arrancar | ✅ `Front Left/Right: Playback 59 [80%] [-15.00dB] [on]` (el 80 % es justo el valor que fija el bloque de bootsync) | `shots/v11-alsa1.png` |
| `amixer -c 0 sget PCM` | ⚠️ No verificable en QEMU: el códec HDA genérico emulado solo expone `Master` y `Capture` (`amixer: Unable to find simple control 'PCM'`). En la Dell (IDT 92HD71B7X) PCM, Speaker y Headphone sí existen y el mismo bloque los deja al 80 % desmuteados | `shots/v11-alsa2.png`, `shots/v11-alsa3.png` |
| Escritorio FLWM con el fondo de lava | ✅ intacto | `shots/v11-desk4.png` |

**Pendiente (solo hardware real):** que Juanca confirme en la Dell que el sonido sale por los altavoces al arrancar sin tocar nada.

---

## 9. v1.2 (2026-10-04) — Tema lava completo, apps FLinux, wifi, Conky y FLPicSee

**Entregable:** `flinux-jc-v1.2.iso` — 291,504,128 bytes — MD5 `d53fbfecb9cd82a95e9e78a40f93a831` (+ `flinux-jc-v1.2.iso.md5.txt`). Base = v1.1 (incluye el arreglo de audio de §8) + lo siguiente. No subida a GitHub (la sube el agente principal).

### Cambios

1. **Menú de arranque con temática FLinux.** Ojo: esta ISO arranca con **isolinux/syslinux, no GRUB** (así arranca Tiny Core; no hay GRUB que tematizar en el medio live). Se tematizó el menú vesamenu de isolinux: fondo `lavaboot.png` (640×480, derivado del mismo fondo lava del escritorio), título «flinux-jc», etiquetas «Boot flinux-jc (FLWM topside, Xorg)» y «Boot Core (command line only)», colores lava (selección `#cc8c3a10`, textos crema/naranja) y autoboot a los 10 s. `vesamenu.c32` es de syslinux 4.05, la misma versión que el `isolinux.bin` de TC 17.1.
2. **Fuera Beaver y FLuff:** eliminados `beaver.tcz` y `fluff.tcz` de `cde/optional` y de `onboot.lst`; ya no aparecen en menú ni wbar (verificado en captura del menú).
3. **Entran del repo FLinux por defecto** (`https://flinux.loc-os.com/17.x/x86/tcz`, descargados con el resolver y cierre de dependencias completo, 0 fallos), todos con `.desktop` propio → icono automático en menú FLWM y en wbar:
   - **FLWriter 1.1** (Anddy Cort) — procesador de textos FLTK.
   - **FLFM 1.0.6** (Anddy Cort) — gestor de archivos (sustituye a FLuff).
   - **FLPlayer 1.0** (Nicolas Longardi) — reproductor (mplayer ya estaba en la ISO).
   - **SeaMonkey 2.53.24** (Nicolas Longardi, build comunitario del repo) — ver desviación 2.
   - **FileZilla 3.18.0** (bmarkus) — cliente FTP (wxWidgets/gtk3 y demás deps añadidos al cierre).
   - **FLPicSee 1.3.1** (Michael A. Losh, recompilado contra fltk-1.3 por juanito en 2025) — visor de imágenes.
   - **wifi 1.8** (roberts/bmarkus) — paquete WiFi de Tiny Core con `wifi.sh`; dependencia única `wpa_supplicant-dbus` (la ISO ya traía `wireless_tools` y wpa_supplicant, sin conflicto). Trae `wifi.desktop` → entrada «Wifi» en el menú, y funciona por terminal.
4. **FLWM topside color lava tipo macOS:** `FLWM_TITLEBAR_COLOR=8C:3A:10` (marrón volcánico quemado) en `/etc/skel/.profile` del core; barras de título oscuras coherentes con el fondo. wbar reempaquetada con iconos grandes `-isize 48` (dock inferior estilo macOS).
5. **Conky «ultra moderno» con autostart:** paquete `conky.tcz` 1.9.0 (juanito) + `dejavu-fonts-ttf` para tipografía limpia. Config `~/.conkyrc` propia, arrancado desde `~/.setbackground` justo después de `flbg` (fondo ya fijado) y `wbar.sh`:
   - **Texto principal en blanco** (`default_color FFFFFF`); acentos lava solo en títulos de sección (`FF7A1A` negrita), reglas (`FF3300`) y barras/gráficas (gradientes `FF3300→FF7A1A`).
   - Pseudo-transparencia sobre el fondo (`own_window yes`, tipo `desktop`, `own_window_transparent yes`), alineado arriba a la derecha sin tapar el logo central.
   - Datos: sistema (flinux-jc), kernel, tiempo activo; CPU (modelo desde `/proc/cpuinfo`, % + `cpubar` + `cpugraph`; núcleos 1-2 con guarda `if_existing /sys/devices/system/cpu/cpu1`); RAM (uso/total/% + `membar` + `memgraph`) y swap; disco raíz (`fs_used`/`fs_size` + barra); red eth0 (IP, bajada/subida + `downspeedgraph`/`upspeedgraph`) y wlan0 completo **solo si existe** (`if_existing /sys/class/net/wlan0`), para la Dell con la BCM4312.
6. **Nota de construcción:** el árbol `isoroot-v12` se creó copiando el de v1.1 con tar y quedó con permisos 750/640 (root:nogroup), ilegibles para el usuario `tc`: la primera ISO de prueba arrancaba **sin cargar ninguna extensión**. Corregido con `chmod -R a+rX isoroot-v12` antes de xorriso (la ISO final graba 755/644, como la v1.1).

### Verificación (QEMU i386, HDA emulada, e1000; sobre la ISO v1.2 entregable salvo que se indique)

| Comprobación | Resultado | Evidencia |
|---|---|---|
| Menú de arranque isolinux tematizado (fondo lava, «flinux-jc», etiquetas) | ✅ | `shots/v12-bootmenu.png` |
| Escritorio FLWM lava + wbar iconos 48 + Conky en blanco con gráficas vivas (CPU 100 % bajo carga, red con ping) | ✅ | `shots/v12F-desktop-final2.png`, `v12F-desktop-final.png` |
| Menú Applications sin Beaver/FLuff y con filezilla, FLConnect, FLFM, flpicsee, FLPlayer, Flradio, FLTube, FLTV, FLWriter, seamonkey, Terminal, Wifi | ✅ | `shots/v12F-appsmenu2.png`, `v12F-navterm-crop.png` |
| FLWriter 1.1 abre (documento, toolbar) | ✅ | `shots/v12-app-flwriter.png` |
| FLFM 1.0.6 abre en `/home/tc` | ✅ | `shots/v12-app-flfm3.png` |
| SeaMonkey 2.53.24 abre (URL de la release visible; «Server Not Found» = sin Internet en la VM) | ✅ | `shots/v12-app-seamonkey.png` |
| FileZilla 3.18.0 abre (diálogo de bienvenida con versión) | ✅ | `shots/v12-app-filezilla2.png` |
| FLPlayer 1.0 abre con controles | ✅ | `shots/v12-app-flplayer2.png` |
| FLPicSee 1.3.1 abre el propio fondo `/opt/backgrounds/flinux-lava.bmp` (título «54% flinux-lava.bmp - FL-PicSee 1.3.1») | ✅ | `shots/v12F-picsee1.png` |
| Mezclador al arrancar sin tocar nada: `Master 59 [80%] [on]` en ambos canales | ✅ | `shots/v12b-mixer-crop.png`, `v12F-desktop-final.png` |
| FLRadio abre con su lista de emisoras | ✅ | `shots/v12-app-flradio2.png` |
| FLConnect abre («FLConnect 1.0 - listo») | ✅ | `shots/v12-app-flconnect1.png` |
| `sudo wifi.sh` arranca, escanea y sale limpio sin hardware WiFi: «No wifi devices found!» | ✅ | `shots/v12-wifi2-crop.png` |
| Conky muestra datos reales de la VM (kernel 6.18.35-tinycore, eth0 10.0.2.15, RAM/disco) y wlan0 oculto por guarda | ✅ | `shots/v12F-desktop-final2.png` |

### Desviaciones y notas

1. **Bootloader:** se tematizó **isolinux/syslinux** (el único arranque del medio live). No existe GRUB en esta ISO; si algún día se genera una variante instalable con GRUB habrá que tematizarlo aparte.
2. **SeaMonkey: el del repo (2.53.24) en vez del oficial 2.53.21 i686 de `build/prep/`.** El 2.53.24 comunitario del repo FLinux abre verificado en QEMU sobre TC 17.1 x86 (perfil, diálogos y navegación hasta donde la red de la VM permite) y es más nuevo; se prefirió ese. El oficial queda en `build/prep/` como referencia documentada.
3. **Conky sin ARGB real:** en este Xorg/FLWM el visual ARGB no mezcló (el panel salía negro opaco), así que se usa pseudo-transparencia (`own_window_transparent`), que copia el fondo ya puesto por `flbg`: efecto de panel oscuro sobre la zona sombreada del wallpaper, con el texto blanco legible.
4. **Control PCM inexistente en el códec HDA emulado** (solo Master/Capture): el amixer de la VM no lo expone; es la limitación ya documentada en §8, en la Dell sí existe.
5. **No verificado aquí (límites del banco, igual que v1.0/v1.1):** WiFi real BCM4312 de la Dell (`wifi.sh` queda instalado y probado sin tarjeta; la asociación real con wpa_supplicant es prueba suya), navegación/streams con Internet (la VM no tiene salida; SeaMonkey funcionó hasta el DNS), y reproducción real de medios en FLPlayer (abre; sin ficheros de prueba ni red en la VM).

---

## 10. v1.3 (2026-10-05) — FLWM clásico con barra izquierda naranja fuego

**Entregable:** `flinux-jc-v1.3.iso` — 291,504,128 bytes — MD5 `11c917eee09a3d133bc5db69b0b07724` (+ `flinux-jc-v1.3.iso.md5.txt`, `md5sum -c` OK). Base = v1.2 (que ya incluye el arreglo de audio de §8 y todo lo de §9); **único cambio: el gestor de ventanas**.

### Cambio

1. **Fuera `flwm_topside.tcz`, dentro `flwm.tcz` 1.20** (el FLWM clásico, descargado del repo FLinux por defecto `https://flinux.loc-os.com/17.x/x86/tcz`, dep única `fltk-1.3.tcz`, ya presente). Cambiado en `cde/optional` y en `onboot.lst`; también en las listas de instalación `xfbase.lst`, `xibase.lst` y `xwbase.lst` para que una futura instalación en disco quede coherente.
2. **Arranque:** el parámetro de isolinux pasa de `desktop=flwm_topside` a **`desktop=flwm`** (la etiqueta del menú de arranque ahora dice «Boot flinux-jc (FLWM clasico, Xorg)»; el resto del menú lava de la v1.2 no se toca). `tc-config` escribe `/etc/sysconfig/desktop` con ese valor y `startx` ejecuta ese binario; el menú de aplicaciones y wbar funcionan igual porque la maquinaria es genérica (`flwm_initmenu`/`flwm_makemenu`).
3. **Color de la barra de título:** ambos binarios (clásico y topside) leen la variable de entorno **`FLWM_TITLEBAR_COLOR`** en formato `RR:GG:BB` (confirmado con `strings` en los dos ELF). Queda en `/etc/skel/.profile` del core: se cambia `8C:3A:10` (marrón volcánico de la v1.2) por **`FF:08:00`**.
   - **Matiz medido, no supuesto:** flwm aclara el color configurado mezclándolo ~40 % hacia blanco al dibujar la barra activa. Con el valor ingenuo `FF:5A:00` (#FF5A00) el píxel real de la barra salió `#FF9B65` (naranja pastel). Por eso se pre-compensa a `FF:08:00` y el color **visible medido** en la ventana activa es **`#FF6A65`** (R=FF, G=0x6A — dentro del rango pedido #FF5A00–#FF6A00; el azul residual ~0x65 es el suelo que impone esa mezcla hacia blanco, no se puede bajar más con B=00). El texto del título se lee en claro sobre ese naranja (en la captura se lee «FLFM 1.0.6» y «FLTube 2.2.0» en vertical).

### Verificación (QEMU i386, HDA emulada, e1000; sobre la ISO v1.3 entregable)

| Comprobación | Resultado | Evidencia |
|---|---|---|
| Escritorio FLWM + fondo lava + wbar 48 px | ✅ | `shots/v13F-desktop.png`, `v13F2-desktop2.png` |
| Conky en blanco con gráficas, autostart, datos reales (kernel 6.18.35-tinycore, eth0 10.0.2.15) | ✅ | `shots/v13F-desktop.png` |
| Proceso del WM es el clásico: `5608 tc flwm` (`ps`) | ✅ | `shots/v13F-home.png` |
| `/home/tc/.profile` en el sistema vivo: `export FLWM_TITLEBAR_COLOR="FF:08:00"` | ✅ | `shots/v13F-home.png` |
| **FLFM 1.0.6 abierto** (`/home/tc`, webstations.lst): barra de título **a la izquierda**, vertical, color medido `#FF6A65` | ✅ | `shots/v13F-flfm-final.png` |
| FLTube 2.2.0 abierto: misma barra izquierda naranja, título vertical legible | ✅ | `shots/v13F2-flfm2.png` |
| Menú FLWM clásico (clic derecho en escritorio): Conky/ventanas, Applications, SystemTools, New desktop, Exit; Applications lista las 12 apps (filezilla, FLConnect, FLFM, flpicsee, FLPlayer, Flradio, FLTube, FLTV, FLWriter, seamonkey, Terminal, Wifi) | ✅ | `shots/v13F2-keys2.png` |
| Mezclador al arrancar **sin tocar nada**: `Front Left/Right: Playback 59 [80%] [-15.00dB] [on]` (el arreglo de la v1.1 intacto) | ✅ | `shots/v13F-mixer.png` |
| Extensiones cargan todas (en el log de arranque se ve `flwm` en la lista y ningún error nuevo) | ✅ | `shots/v13F-boot-desktop.png` |

### Notas

1. **Tamaño idéntico a la v1.2** (291,504,128 B): el swap de extensiones difiere en ~13 KB y la imagen ISO queda alineada al mismo total; el MD5 es distinto, como debe ser.
2. En las primeras pruebas el core reempaquetado dio «No working init found»: causa ajena a la ISO (empaquetado cpio con `find -depth`, que deja los directorios tras sus ficheros); corregido empaquetando sin `-depth` y verificado el contenido (árbol idéntico al de la v1.2 salvo la línea del color).
3. **No verificado aquí (igual que v1.0–v1.2):** WiFi real BCM4312 de la Dell y navegación/streams con Internet (la VM no tiene salida).

## 11. v1.4 (2026-10-05) — FLConnect no conectaba WireGuard: causa raíz y corrección

**Entregable:** `flinux-jc-v1.4.iso` — 294,649,856 B — MD5 `efb5de414fafe11cd7a6c6aa2b327e06` (+ `flinux-jc-v1.4.iso.md5.txt`). Base: v1.3 (mismo escritorio, Conky, apps y audio de la v1.1).

### Síntoma (Dell real, v1.3)

En FLConnect, al activar un perfil WireGuard: `stat: command not found` (×2, con error aritmético de wg-quick en la línea 47), `ip link add dev X type wireguard` → «Error: Unknown device type», caída al respaldo wireguard-go y estado final Desconectado. En terminal normal, `sudo modprobe wireguard` también fallaba: «unknown symbol in module, or unknown parameter». La causa **no** era el PATH de FLConnect (incluye /sbin y /usr/local).

### Causa raíz (reproducida en QEMU sobre la v1.3, idéntico core)

1. `dmesg` tras `modprobe wireguard` da exactamente dos símbolos desconocidos: **`ipv6_mod_enabled` e `ipv6_chk_addr`**. En este árbol IPv6 no va integrado en el kernel ni existe `net/ipv6/` en el core (no hay `ipv6.ko.gz` en `/lib/modules/6.18.35-tinycore/`; `modules.dep` de wireguard solo lista sus libs crypto, que sí cargan). El módulo `wireguard.ko` fue compilado contra una config con IPv6 y es **incargable tal cual en este kernel**. El `ipv6.ko` sí existe en el repo FLinux, dentro de la extensión `ipv6-netfilter-6.18.35-tinycore.tcz` (201 módulos: ipv6, nf_tables, xt_*…).
2. **`stat` no existe** en la base (lo instala `coreutils.tcz`). Es el error de la línea 47 de wg-quick (no detiene el script, pero ensucia el registro y forma parte del fallo reportado).
3. La ruta por defecto de un perfil de túnel completo (AllowedIPs 0.0.0.0/0) en wg-quick usa **nft o iptables-restore**: los módulos clásicos de iptables (`x_tables`, `ip_tables`, `iptable_*`) **no existen** en este kernel ni en el repo, así que iptables jamás funcionaría; la vía viable es **nft** (`nftables.tcz` + `nf_tables.ko`, presente en ipv6-netfilter).
4. **DNS**: wg-quick llama `resolvconf -a`, y openresolv **rechaza cualquier alta mientras `/etc/resolv.conf` exista sin su firma** («signature mismatch», incluso con el fichero vacío de 0 bytes que trae el core). TC escribe ese fichero directamente desde el hook de udhcpc, sin pasar por resolvconf.
5. La vía wireguard-go (respaldo) sí crea la interfaz (`/dev/net/tun` existe, tun integrado) y llegó a completar handshake en las pruebas, pero wg-quick moría después en el paso de DNS/rutas igualmente.

### Corrección (nivel ISO; binario FLConnect intacto)

- **Extensiones nuevas en `cde/optional/` + `onboot.lst`** (del repo flinux.loc-os.com, con su cierre completo, cada una con su `.tcz` + `.tcz.dep` + `.tcz.md5.txt`): `ipv6-netfilter-6.18.35-tinycore.tcz` (trae `ipv6.ko` y `nf_tables.ko`), `coreutils.tcz` (→ `stat`; dep `gmp.tcz`, ya presente), `nftables.tcz` (→ `nft`; deps `libnftnl`, `libmnl`, `jansson`, `libedit`, `libxtables`, `ncursesw` — también incluidas; `gmp`/`ncursesw` ya estaban en la ISO). **`iptables.tcz` NO se incluye**: sin `ip_tables`/`x_tables` en el kernel no puede funcionar; se documenta para que no se reintente.
- **`/opt/bootsync.sh`**: bloque en segundo plano, tolerante a fallos: `modprobe ipv6`, `modprobe wireguard`, `modprobe nf_tables`. Así el módulo WireGuard queda cargado desde el arranque (además, la autocarga del kernel por `ip link add` también funciona ya con ipv6 disponible).
- **`/usr/share/udhcpc/default.script`** (hook DHCP): si `resolvconf` está presente, primero adopta `/etc/resolv.conf` cuando no lleve la firma (`resolvconf -u`) y después registra el DNS de la concesión vía `resolvconf -a <iface> -m 0`; si no está, escritura directa como siempre. Resultado: resolv.conf nace firmado y el paso DNS de wg-quick funciona en cable y en WiFi (wifi.sh también pasa por udhcpc).

Núcleo (core.gz) derivado del de la v1.3 por sustitución de solo esos 2 ficheros (verificado por diff de árboles: `opt/bootsync.sh` y `usr/share/udhcpc/default.script`, nada más; los modos setuid tipo `usr/bin/sudo` quedan byte a byte).

### Verificación (QEMU i386 sobre la ISO v1.4 entregable; perfil WireGuard de prueba con servidor gemelo en loopback, claves desechables)

| Comprobación | Resultado | Evidencia |
|---|---|---|
| Arranque fresco: `lsmod` ya trae `ipv6`, `wireguard`, `nf_tables` cargados (bootsync) | ✅ | salida netcat (diag) |
| `stat` y `nft` presentes; `sudo ip link add dev wg0 type wireguard` rc=0 (y borrado limpio) | ✅ | salida netcat |
| `/etc/resolv.conf` recién arrancado: `# Generated by resolvconf` + `nameserver 10.0.2.3` (hook nuevo) | ✅ | salida netcat |
| Mezclador al arrancar sin tocar nada: `[80%] [on]`; escritorio FLWM + Conky en blanco igual que v1.3 | ✅ | `shots/v14-90-desk.png` + salida netcat |
| **FLConnect: conectar `wgtest`** — registro limpio (`ip link add type wireguard`, setconf, address, mtu, `resolvconf -a`, fwmark…), sin errores de stat, sin «Unknown device type», sin wireguard-go; estado **Conectado** | ✅ | `shots/v14-97-on.png` |
| Handshake real tras conectar desde la GUI (ambas interfaces, con transferencia de bytes) | ✅ | `shots/v14-98-handshake.png` |
| **FLConnect: desconectar** — registro de bajada limpio (reglas, `resolvconf -d`, nft), estado Desconectado | ✅ | `shots/v14-99-off.png` |
| Pre-chequeo de la misma cadena en la v1.3 con el arreglo aplicado en vivo (tce-load manual) | ✅ | `shots/v14-71-conn.png`, `v14-78-off.png`, `diag-net.txt` |

### Notas

1. En el laboratorio QEMU la conexión de prueba usa un «servidor» WireGuard en la misma máquina (endpoint 127.0.0.1:51820) porque la VM no sale a Internet; el handshake y el ping por el túnel (0 % de pérdida) confirman el plano de datos real.
2. FLConnect, al cerrar su ventana, **no baja** la interfaz activa (comprobado: sigue en `wg show`): es su comportamiento normal; la bajada se hace con el interruptor.
3. **No verificado aquí:** la Dell real (WiFi BCM4312 + su servidor WireGuard por Internet con el perfil de Juanca) — la prueba final la hace Juanca en su máquina, igual que en versiones anteriores. OpenVPN en FLConnect no se ha tocado ni probado en esta versión.

## 12. v1.5 (2026-10-05) — Todo lo nuevo: degradado FLWM, FLConnect en wbar, LXTask, hora de La Habana, menú robot y flskin

Base v1.4. Contenido nuevo: (1) FLWM clásico con degradado de 3 colores (rojo sangre `#880808` → naranja fluorescente `#FF6700` → amarillo `#FFFF00`; activa viva, inactiva mezclada al 50% hacia gris 0x90) — `flwm.tcz` recompilado (MD5 `0372d3e3803cb4af33bffbe0ff16abca`); (2) FLConnect en el wbar con icono PNG 8-bit 644 y lanzador `Exec=sudo /usr/local/bin/flconnect` — `flconnect.tcz` corregido (MD5 `04bd082430d22ed7b20fef3213b9833f`)—, porque con solo el setuid el proceso heredaba `HOME=/home/tc` y no veía los perfiles de `/root`; (3) `lxtask.tcz` (MD5 `1486d069d04bcb16bb70d4ff86d8d666`); (4) hora de La Habana: APPEND `nortc tz=America/Havana` (la base lanza getTime vía settime.sh solo con `nortc`) + zonefile `/usr/share/zoneinfo/America/Havana` y symlink `/etc/localtime` en el core; (5) Conky con `${time %d/%m/%Y} ${time %H:%M:%S}` numérico (en locale C, `%A` saldría en inglés); (6) menú de arranque vesamenu.c32 con el fondo del robot «No usen Windows» y las letras «flinux-jc» en minúsculas con degradado (en la pantalla de texto `boot:` el ANSI es imposible: isolinux imprime los escapes en crudo — verificado; la vía es el fondo gráfico 640×480, PNG paleta 256 minimalista, nombre corto `fjcbg.png`); (7) flskin preinstalado — `flskin.tcz` reconstruido (MD5 nuevo `119a5aded07354329d0370c21a921ff3`; único cambio frente al entregado por chat: la fecha numérica en sus dos conkyrc).

### Hallazgos corregidos durante la construcción

- **El zonefile no entraba en el rootfs vivo**: al reconstruir el `core.gz` por stream cpio (vía `build/repack_core_v15.py`) sin entradas de directorio explícitas, el unpacker del kernel descarta los ficheros cuyos directorios padre no existen; `/etc/localtime` sí entró (su padre existía) pero `/usr/share/zoneinfo/America/Havana` no, y la sesión quedaba en UTC. Corregido añadiendo las entradas `usr/share/zoneinfo` y `usr/share/zoneinfo/America` antes del fichero. Verificado en vivo: `date` da CDT (UTC−4) contra `date -u`.
- **El `.dep` de 0 bytes no puede ser asset de GitHub** (HTTP 400): en el repo flconnect quedó en la raíz además de dentro del ZIP.
- **El instalador de Tiny Core no copia el menú tematizado** (ver abajo): lo deja plano, hay ajuste.

### Verificación (QEMU i386)

| Comprobación | Resultado | Evidencia |
|---|---|---|
| Menú de arranque ISO: fondo robot + «flinux-jc» degradado + cuenta atrás | ✅ | `shots/v15-00-menu.png` |
| Escritorio lava; Conky con fecha/hora numérica; `date` CDT (−4h vs UTC); zonefile presente | ✅ | `shots/v15-08b-desktop.png`; salida netcat |
| Ventanas solapadas: barra activa con degradado vivo (medido: (144,14,7)→(249,98,0)→(255,182,0)), inactiva opaca | ✅ | `shots/v15-09-ventanas.png`, `v15-11-solape2.png` |
| Un clic en FLConnect del wbar: sin clave, proceso `root` (Uid 0 0 0 0), perfil PRUEBA de `/root` visible | ✅ | `shots/v15-13-flconnect.png`; `ps` |
| LXTask abre y lista procesos | ✅ | `shots/v15-14-flskin-lxtask.png` |
| flskin: tema neutro (fondo+Conky), oscuro Adwaita-dark real en app GTK nueva (la ya abierta queda clara), reversible a lava | ✅ | `shots/v15-15/16/17-*.png` |
| **Instalación en disco** (instalador GUI de TC desde 2º CD CorePlus): frugal sda, ext4, bootloader aplicado | ✅ | `shots/v15-49-installing.png`, `v15-63-installing2.png` |
| Menú tematizado persistente tras la instalación (2 reinicios) + escritorio instalado completo (FLConnect root, LXTask, flskin, CDT) | ✅ (con el ajuste de abajo) | `shots/v15-71-diskmenu2.png`, `v15-80-diskmenu-r2.png`, `v15-90-instps2.png` |

### La instalación y el ajuste del menú (importante)

El instalador (GUI → `tc-install.sh`) particiona (sda1 ext4, flag activa), escribe MBR (`mbr.bin`) y aplica extlinux, copiando `vmlinuz`+`core.gz`, todo `cde/optional` y `onboot.lst` a `tce/`. Su `extlinux.conf` resultante es plano — `DEFAULT/LABEL/KERNEL/INITRD/APPEND quiet … waitusb=5:UUID=… tce=UUID=…`— sin menú gráfico (solo añade vesamenu si detecta otro SO con partición activa — `LOCALOS` — y MARKACTIVE=1). Sin «Install boot loader» marcado no escribe ni el MBR (en la primera pasada lo desmarqué yo por error de clic; en la segunda, marcada, lo aplicó correctamente: no es un fallo del instalador).

**Ajuste aplicado** (tras instalar, con el disco montado en `/mnt/drive`): copiar `vesamenu.c32`, `libcom32.c32`, `libutil.c32` (de `/usr/local/share/syslinux`) y `fjcbg.png` (de `/mnt/sr0/boot/isolinux/`) a `tce/boot/extlinux/` y anteponer al `extlinux.conf` —dejando intacto el APPEND—:

```
UI vesamenu.c32
MENU TITLE flinux-jc
MENU BACKGROUND fjcbg.png
TIMEOUT 50
```

Resultado: el sistema instalado arranca con el mismo menú (robot + letras) en cada reinicio, verificado dos veces. Si Juanca reinstala desde cero, hay que repetir este ajuste de 4 ficheros + 4 líneas.

### Publicación

- `flinux-jc-v1.5.iso`: 295,698,432 bytes; MD5 `2446335f0a18ba48e7778e3b5ddc7984`; SHA-256 `7e85e0e9e97674294d52ee9051b033243768e00e1768295d7a40db62acd10f07`.
- Release v1.5: https://github.com/jcarlosrf26/flinux-jc/releases/tag/v1.5 (ISO + `.md5.txt`), digest SHA-256 de GitHub idéntico al local.

## 13. v1.5 corregida (2026-10-06) — El fallo de instalación y su arreglo en la propia ISO

> Juanca instaló la v1.5 publicada y, al arrancar de disco, no había ningún programa preinstalado ni ninguna de las configuraciones nuevas. Reportado el 2026-10-05 22:39 CDT. La verificación anterior no fue fiel: había usado un segundo CD (CorePlus) y lecturas del live; este apartado reproduce el fallo tal cual y documenta el arreglo. La ISO corregida **sustituye** los assets del Release v1.5 (mismo tag).

### Reproducción fiel del fallo (R0)

QEMU i386 **solo con la ISO v1.5 como CD** (nada de segundo CD ni paquetes externos): el live arranca al escritorio, pero no hay instalador:

- el submenú Applications **no tiene ninguna entrada de instalador** (captura `shots/v15fix-03-submenu.png`);
- por tty: `ls /mnt/sr0/cde/optional/tc-install-GUI.tcz` → «No such file or directory» y `ls /usr/local/bin/tc-install` → «No such file or directory» (captura `shots/v15fix-08-ev1.png`);
- `tce-load -wi tc-install-GUI` sin red falla (`wget: bad address 'flinux.loc-os.com'`, captura `shots/v15fix-09-sinred.png`).

**Causa raíz nº 1 (la v1.5 no traía el instalador).** El `cde/optional` de la v1.5 es idéntico al árbol `isoroot-v15` y le faltaban todas las extensiones del instalador: `tc-install-GUI.tcz`, `tc-install.tcz`, `syslinux.tcz`, `dosfstools.tcz`, `mtools.tcz`, `perl5.tcz`, `glibc_gconv.tcz` (cierre completo del instalador: 19 paquetes; faltaban 7). `cde/installer.instlist` nombraba `tc-install-GUI.tcz`, pero el fichero no estaba en la ISO.

### Intermedia R1: el instalador stock no instala nada en disco

Se montó una ISO intermedia (v1.5 + los 7 paquetes stock del CorePlus, sin parchear) y se instaló con el motor interactivo (el mismo que ejecuta la GUI), con el campo **«Install Extensions from this TCE/CDE Directory» vacío**, que es lo que le ocurre a un usuario normal:

1. Al cargar `tc-install-GUI.tcz` por `onboot.lst`, la GUI abre pero con la **lista de discos vacía**: Tiny Core no resuelve dependencias al cargar por `onboot.lst`; el GUI necesita `tc-install.sh`/`fetch_devices` y estos no venían con la GUI. (En TinyCorePlus el instalador vive **dentro del core.gz**, por eso allí sí funciona.)
2. La instalación "termina" («Installation has completed») sin copiar ninguna extensión: en el disco, `tce/` contiene solo `boot/` y un `mydata.tgz` de 0 B; no existen `tce/optional/` ni `onboot.lst`. El `extlinux.conf` es plano: `DEFAULT core / LABEL core / KERNEL /tce/boot/vmlinuz / INITRD /tce/boot/core.gz / APPEND quiet waitusb=5:UUID=… tce=UUID=…`.
3. Al arrancar **solo del disco** (sin CD) cae directo a la consola de texto, sin X ni escritorio (capturas `shots/v15fix-54-diskmenu.png`, `shots/v15fix-55-pelado.png`).

**Causa raíz nº 2 (el instalador no copia el `cde` en instalaciones normales).** En `tc-install.sh`: `getCOREPLUS()` busca «plus» en `isolinux.cfg` y nuestra cfg no lo contiene ⇒ `COREPLUS=no`; con `COREPLUS=no`, la copia de extensiones (`copy_tce()`) solo ocurre si el directorio `TCE/CDE` indicado es válido **o** si existe `/mnt/staging/cde` (que solo aparece instalando desde un fichero `.iso` montado, no desde CD/USB real). Si el campo queda vacío —la GUI solo lo autorrellena si ve el `cde` en `/mnt/sr0..sr3/cde`; un USB grabado con `dd` aparece como `/mnt/sdX` y **no lo detecta**— no se copia absolutamente nada. Además `extlinux_setup()` escribe un APPEND plano y solo tematiza el menú en el caso `LOCALOS` (otra partición activa), así que jamás salía `vesamenu`/`MENU TITLE`/`MENU BACKGROUND` ni los bootcodes `desktop=flwm`, `nortc`, `tz=America/Havana`.

**Grieta adicional.** El `/opt/.filetool.lst` de la v1.5 persistía solo `opt` y `home`: los perfiles de FLConnect (que como root vive en `/root/.flconnect/profiles`) no habrían sobrevivido a un reinicio del sistema instalado.

> La verificación de la v1.5 original pasó porque se instaló con un segundo CD (CorePlus) como apoyo: eso maquilló las dos causas raíz. La prueba de aceptación de esta corregida no usa nada fuera de la propia ISO.

### El arreglo (todo dentro de la ISO; ningún paso manual)

1. **El instalador vive en el core** (como en TinyCorePlus). Se integraron en `boot/core.gz` (derivado del core de la v1.5 por stream de cpio, resto byte a byte):
   - `/usr/local/bin/tc-install.sh`, versión **parcheada** (script stock MD5 `4e38962e256e8d3ebc3cdb189978c10f` + bloques «FJC»):
     - `copy_tce()`: si no se ha producido `tce/onboot.lst` en el disco, se localiza automáticamente el `cde` empaquetado en el medio de instalación (`$BOOT/../cde`, `/mnt/sr0..sr3/cde` y, por último, `/mnt/sd*/cde`) y se copia entero a `tce/` (`onboot.lst`, `optional/` y los `.lst` incluidos). Mensaje visible: `Copying bundled extensions from …`.
     - `extlinux_setup()`: sobre el APPEND ya escrito inserta `nortc tz=America/Havana desktop=flwm` delante de `quiet`; antepone la cabecera `UI vesamenu.c32 / MENU TITLE flinux-jc / MENU BACKGROUND fjcbg.png / TIMEOUT 50` si aún no existe (no duplica en el caso `LOCALOS`); copia `vesamenu.c32`, `libcom32.c32`, `libutil.c32` y `fjcbg.png` a `tce/boot/extlinux/`.
     - El mismo tratamiento se aplicó a los `syslinux.cfg` de los modos USB-ZIP y USB-HDD (`zip_update`/`syslinux_setup`).
   - `/usr/local/bin/fetch_devices` (stock) para que la GUI pueda listar los discos.
2. **`cde/optional` completo**: se añaden `tc-install-GUI.tcz` (+`.dep`, +`.md5.txt`), `syslinux.tcz`, `dosfstools.tcz`, `mtools.tcz`, `perl5.tcz`, `glibc_gconv.tcz` (con sus `.dep`/`.md5.txt`) y `tc-install.tcz` **reempaquetado con el script parcheado** (MD5 `bdd16c121c0adcc607f6376d634ed743`). `cde/onboot.lst` añade al final `tc-install-GUI.tcz` y `syslinux.tcz`. Importante: `tc-install.tcz` no va en `onboot.lst`, porque su enlace `/usr/local/bin/tc-install` pisaría el script parcheado del core (el `.tcz` queda en `optional` por si se carga a mano).
3. **Persistencia de `/root`**: `opt/.filetool.lst` pasa de `opt\nhome\n` a `opt\nhome\nroot\n`; los perfiles de FLConnect sobreviven a los reinicios del sistema instalado.
4. La GUI (`tc-installGUI`, binario FLTK stock) queda sin tocar.

### Verificación de aceptación F1 (la ISO corregida, sola)

QEMU i386 con **solo** la ISO corregida como CD y un disco virtual vacío:

- La GUI del instalador abre desde el menú y **lista los discos** (`fd0`, `sda`) gracias a que `fetch_devices` viene en el core (en R1 la lista salía vacía). La instalación se ejecutó con el motor interactivo (mismos parámetros que la GUI: Frugal → disco completo `sda` → bootloader sí → **campo TCE/CDE vacío a propósito** → ext4 → sin boot options → confirmar).
- Salida: particionado, formateo, MBR, «Applying extlinux», **«Copying bundled extensions from /mnt/sr0/boot/../cde»**, «Installation has completed» (captura `shots/v15fix-A5-inst60.png`).
- Inspección del disco antes de arrancar (capturas `shots/v15fix-A7-disk2.png`, `shots/v15fix-A9-cfg2.png`): `tce/` con `onboot.lst`, `optional/` (todos los paquetes), `boot/core.gz`, y en `tce/boot/extlinux/`: `extlinux.conf` ya tematizado, `vesamenu.c32`, `libcom32.c32`, `libutil.c32`, `fjcbg.png`, `ldlinux.c32/sys`. El `extlinux.conf` resultante:

  ```
  UI vesamenu.c32
  MENU TITLE flinux-jc
  MENU BACKGROUND fjcbg.png
  TIMEOUT 50

  DEFAULT core
  LABEL core
  KERNEL /tce/boot/vmlinuz
  INITRD /tce/boot/core.gz
  APPEND nortc tz=America/Havana desktop=flwm quiet  waitusb=5:UUID="…" tce=UUID="…"
  ```

- **Arranque solo del disco** (sin ningún CD): menú vesamenu con el robot «No usen Windows» y las letras «flinux-jc» con cuenta atrás (capturas `shots/v15fix-B4-a.png`, `shots/v15fix-C0-menu.png`); «Setting Timezone to America/Havana», «Skipping rtc as requested…» y escritorio completo: fondo lava, Conky con fecha/hora numérica, wbar con todas las apps (capturas `shots/v15fix-B1-escritorio.png`, `v15fix-B6-esc2.png`). `date` → `Tue Oct  6 00:09:32 CDT 2026` frente a `date -u` → `04:09:32 UTC` (offset −4 h, La Habana) (captura `v15fix-B8-date.png`). El `.wbar` del instalado trae `c: exec sudo /usr/local/bin/flconnect` (captura `v15fix-B10-wbar.png`).
- FLConnect abierto como root («Perfiles en: /root/.flconnect/profiles», proceso con UID 0) — captura `v15fix-B19-fcmanual.png`.
- **Persistencia**: se creó `/root/.flconnect/profiles/PRUEBA.conf`, `filetool.sh -b` lo metió en `mydata.tgz` (lista del tar: `root/.flconnect/profiles/PRUEBA.conf`, captura `v15fix-B29-tgz.png`) y **tras reiniciar solo de disco**, FLConnect muestra «PRUEBA [WireGuard]» en su lista (captura `v15fix-C3-fc-after.png`).
- LXTask abierto con la lista de procesos (captura `v15fix-C27-ambas.png`) y flskin abierto con sus dos interruptores (captura `v15fix-C30-flskin-err.png`).
- Degradado FLWM medido por píxeles de la barra de título: ventana activa ≈ RGB (239, 135, 14); la misma barra inactiva atenuada a (191, 141, 86) mezclada 50 % hacia el gris; FLConnect activo (238, 134, 2) — activo vivo e inactiva apagada, como en el live.

### Publicación

- ISO corregida: `flinux-jc-v1.5.iso`, **318,767,104 bytes**, MD5 `a295c03ade6e8884758f9602811c3d35`, SHA-256 `ae232f60e24dfa94d3f02447bda83c16ea081c22b6d699cc817eb775a788cc13`.
- Se borraron los dos assets anteriores del Release **v1.5** (HTTP 204) y se subieron la ISO corregida (asset 614504422) y su `.md5.txt` (SHA-256 `29680ccad62562494884667958eb804177b9e6a29b6cb8fb04ea3dd3d66c6ae1`), manteniendo el tag **v1.5**. Los releases v1.1–v1.4 no se tocaron.
- **Digest SHA-256 de GitHub idéntico al local** (`ae232f60…cc13`), verificado tras la subida.
- Sin pasos manuales: instalar → reiniciar → todo puesto (programas, menú robot+letras, hora de La Habana, perfiles de FLConnect persistentes). El veredicto final sigue siendo la prueba de Juanca en la Dell.
