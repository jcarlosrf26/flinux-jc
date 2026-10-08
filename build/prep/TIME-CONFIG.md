# v1.5 — Hora de La Habana: mecanismo ya existe, faltan 2 boot codes + zonefile

Verificado 2026-10-05 sobre `build/rootfs-v14` (base de la v1.5).

## Hallazgo (corrige el ítem 4 de V15-CHECKLIST.md)

`getTime.sh` **ya puede correr solo en cada arranque**: es la propia base
Tiny Core. `etc/init.d/tc-config`:

- `nortc) NORTC=1 ;;` — el boot code `nortc` activa el modo NTP.
- Línea ~163: con NORTC se salta el `hwclock` desde el RTC.
- Línea 634: `[ -z "$NORTC" ] || /etc/init.d/settime.sh &` — `settime.sh`
  solo se lanza **si va `nortc`**. Espera red (Bcast, máx. 60 s), luego
  reintenta `getTime.sh` → `ntpd -q` contra `pool.ntp.org`.

La v1.4 **no lleva `nortc`** (APPEND: `loglevel=3 cde showapps desktop=flwm
waitusb=5`), así que hoy el reloj sale del RTC y `getTime.sh` nunca corre.
No hay que "añadir" el script al arranque: hay que añadir los boot codes.

## Cambio exacto para la v1.5

APPEND de isolinux/extlinux:

```
loglevel=3 cde showapps desktop=flwm waitusb=5 nortc tz=America/Havana
```

- `nortc` → dispara `settime.sh` → `getTime.sh` en cada inicio (2.º plano).
- `tz=America/Havana` → tc-config exporta `TZ` y escribe
  `/etc/sysconfig/timezone`.

## Falta la data de zona (sin esto, TZ cae a UTC)

Confirmado: el rootfs no trae `/etc/localtime`, ni `/etc/TZ`, ni
`/usr/share/zoneinfo` (en `usr/share` solo hay doc/i18n/kmap/locale/misc/
syslinux/tabset/terminfo/udhcpc). Sin el zonefile, `America/Havana` no
resuelve y Conky mostraría UTC (4–5 h menos).

Listo en esta carpeta: `zoneinfo-America-Havana` (copia de
`/usr/share/zoneinfo/America/Havana`, md5 `0f73e648aacfef75f13d8cf1b5cf12c5`).
Al construir, instalarlo como `/usr/share/zoneinfo/America/Havana`
(y opcionalmente enlace `/etc/localtime` → ese archivo).

Reglas verificadas (zdump 2026–2027): CST=UTC−5, CDT=UTC−4; entra horario
de verano el 2.º domingo de marzo 00:00 local, sale el 1.er domingo de
noviembre 01:00→00:00. Alternativa sin archivo (glibc/musl la aceptan):
`TZ=CST5CDT,M3.2.0/0,M11.1.0/1`. Preferir el zonefile: menos error.

## Ítem 5 (Conky) — depende de lo anterior

`.conkyrc` (skel, línea 38) ya trae la cabecera `FLINUX-JC`; no hay
`${time}`. Añadir bajo la cabecera, en color lava:

```
${time %d/%m/%Y}  ${time %H:%M:%S}
```

Ojo: con fecha en palabras (`%A %e de %B`) y locale C salen los meses en
inglés («5 de October»). La forma numérica `%d/%m/%Y` es segura sin tocar
locale; si Juanca quiere el día/mes en español, hay que empaquetar locale
`es` — decidir con él, no asumir.

## Verificación obligatoria en QEMU (antes de darlo por bueno)

1. Arrancar la ISO de prueba con los boot codes nuevos.
2. Esperar a que haya red y comprobar `date`: debe dar hora de La Habana
   (CDT, UTC−4 en octubre), no UTC.
3. Confirmar que el `TZ` llega a la sesión gráfica (Conky con la hora
   correcta en pantalla). Si la sesión X no hereda el TZ de tc-config,
   añadir `TZ=America/Havana` a `~/.profile` del skel o el enlace
   `/etc/localtime` — el zonefile ya lo cubre por la vía de glibc.
4. Riesgo residual: `settime.sh` espera red máx. 60 s; si el WiFi
   BCM4312 de la Dell asocia más tarde, la sync no ocurre en ese arranque.
   Si pasa en la prueba, extender el reintento en bootsync con el patrón
   ya usado para ALSA/WireGuard. **No afirmarlo resuelto hasta verlo en
   la Dell.**

## Lo que NO se ha hecho

- No se tocó la ISO v1.4, ni el rootfs, ni los boot codes (Juanca pidió
  no construir la v1.5 hasta su señal; esto es solo preparación).
- La grabación del video de vista previa no se tocó.
