# Créditos de las aplicaciones y componentes

Salvo lo indicado, los programas que integra flinux-jc v1.5 no fueron
escritos para esta remasterización: se agradece y acredita a sus autores.

## Aplicaciones FLinux

- **FLFM, FLWriter, FLRadio, FLTV y FLTube** — **Facundo Adorno**,
  autor de FLinux. En la v1.5 entran como paquetes `.tcz` de su
  repositorio (https://flinux.loc-os.com/); esta distro solo los
  adapta (notas en `build/prep/FLTV-PATCH-NOTES.md`, créditos y
  licencias según cada paquete aguas arriba).

## Gestor de ventanas

- **FLWM** (Fast Light Window Manager) — **Bill Spitzak**.
  http://flwm.sourceforge.net/
  Aquí se incluye parcheado con el degradado de 3 colores
  (`apps/flwm/frame-degradado.patch`); la base y su autoría son de
  Bill Spitzak.

## Red y VPN

- **WireGuard** — **Jason A. Donenfeld**.
  https://www.wireguard.com/
  En la v1.5 la conexión WireGuard la hace el módulo del kernel (sin
  wireguard-go).

## Base del sistema

- **Tiny Core Linux** — creado por **Robert Shingledecker** y el
  equipo Tiny Core; a través de él llegan la mayoría de paquetes de la
  ISO (X.Org, BusyBox, utilidades y el repositorio de extensiones).
  http://tinycorelinux.net/

## Programas con repositorio propio (de Juanca)

- **FLConnect** (gestor VPN WireGuard/OpenVPN):
  https://github.com/jcarlosrf26/flconnect
- **flskin** (temas claro/oscuro GTK+FLTK con interruptores ON/OFF):
  https://github.com/jcarlosrf26/flskin
