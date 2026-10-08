# Programas propios y de terceros en la v1.5

Los créditos completos de las aplicaciones y componentes integrados
están en [CREDITOS.md](CREDITOS.md).

## Con repositorio propio (código GPL-3.0)

- **FLConnect** (gestor VPN WireGuard/OpenVPN): https://github.com/jcarlosrf26/flconnect
- **flskin** (temas claro/oscuro GTK+FLTK con interruptores ON/OFF): https://github.com/jcarlosrf26/flskin

## En este repositorio

- `apps/flwm/frame-degradado.patch` — parche del gestor de ventanas FLWM
  para el degradado de 3 colores de flinux-jc; `apps/flwm/INSTALAR.txt`
  trae sus instrucciones.
- `build/flbg.c` — utilidad propia que fija el fondo de la ventana raíz
  X11 desde un BMP (escalado «cover»).
- `build/prep/FLTV-PATCH-NOTES.md` — qué se parcheó y por qué en FLTV.

## Programas FLinux aguas arriba

**FLFM, FLWriter, FLRadio y FLTV** son aplicaciones de Facundo Adorno,
autor de FLinux; en la v1.5 entran como paquetes `.tcz` de su
repositorio y sus fuentes no formaban parte del árbol de construcción
local de esta remasterización (al cierre de esta publicación no se
localizaron en el workspace). FLTV conserva su licencia GPL-3.0 y su
crédito aguas arriba.
