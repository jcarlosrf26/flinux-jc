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
