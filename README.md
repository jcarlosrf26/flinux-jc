# flinux-jc

Versión personalizada de FLinux 17.1 (Tiny Core 17.1, 32 bits) para Dell Inspiron 1545: Xorg, audio ALSA, FLRadio/FLTV/FLTube, FLConnect, drivers BCM4312 y repo flinux.loc-os.com por defecto. Sin navegador.

La ISO instalable está en la Release v1.5 de este repositorio.

## Código fuente

Todo el código propio y de construcción de esta remasterización se
publica bajo la licencia GPL-3.0 (archivo `LICENSE`), como ya se hizo
con FLConnect y flskin:

- `build/` — scripts de reempaquetado del core (`repack_core_v15.py`,
  `repack_core.py`), el instalador parcheado y los scripts con los que
  se deriva la v1.5 (`build/install-fix/`), la configuración maestra de
  arranque (`build/boot/isolinux.cfg`, `build/boot/boot.msg`), la lista
  de extensiones que carga la ISO (`build/onboot-v1.5.lst`), la
  herramienta `build/flbg.c` y las notas de preparación en `build/prep/`.
- `kernel/` — nota sobre el kernel: la v1.5 usa el 6.18.35-tinycore de
  serie, sin recompilar.
- `apps/` — el parche del degradado de FLWM y las notas de FLTV; los
  programas con repositorio propio (FLConnect y flskin) se enlazan
  desde ahí en vez de duplicar su código.
- `INFORME.md` — el informe técnico completo del proyecto.
- `V15-CHECKLIST.md` — la especificación cerrada de la v1.5.

Los componentes de terceros (Tiny Core Linux, el kernel Linux y los
programas que la ISO empaqueta) conservan sus propias licencias y sus
fuentes viven en sus proyectos originales.

## Créditos

Esta remasterización se construyó sobre el trabajo de otras personas y
proyectos, a quienes corresponden el reconocimiento y las gracias:

- **Tiny Core Linux** — creado por [Robert Shingledecker](http://tinycorelinux.net/)
  y el equipo Tiny Core: es la base de esta remasterización.
  http://tinycorelinux.net/
- **Kernel Linux** — [Linus Torvalds](https://www.kernel.org/) y la
  comunidad del kernel Linux. https://www.kernel.org/
- **FLinux y sus aplicaciones FLFM, FLWriter, FLRadio, FLTV y FLTube** —
  **Facundo Adorno**: esta distro adapta su trabajo aguas arriba.
- **FLWM** (Fast Light Window Manager) — **Bill Spitzak**.
  http://flwm.sourceforge.net/
- **WireGuard** — **Jason A. Donenfeld**.
  https://www.wireguard.com/
- **Conky** — **Brenden Matthews** y el equipo Conky.
  https://github.com/brndnmtthws/conky
- **X.Org** — la [X.Org Foundation](https://www.x.org/).
  https://www.x.org/

Lo único que esta remasterización aporta es la integración de todo lo
anterior para un Dell Inspiron 1545 concreto; el mérito del sistema y
de sus programas es de sus autores.
