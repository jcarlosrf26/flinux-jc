# Kernel de FLinux-JC v1.5 (32 bits)

La v1.5 usa el kernel **6.18.35-tinycore de serie, sin recompilar**: no hay
una config propia que publicar. Los módulos del hardware de la Dell
Inspiron 1545 (b43 para la Broadcom BCM4312 LP-PHY, i915 para la GMA
4500MHD, snd-hda-intel para el audio IDT y tg3 para Ethernet) llegan en
las extensiones normales del cierre de la ISO
(`graphics-6.18.35-tinycore.tcz`, `wireless-6.18.35-tinycore.tcz`,
`alsa-modules-6.18.35-tinycore.tcz`, ver `build/onboot-v1.5.lst`), tal
como las distribuyen Tiny Core y el repositorio FLinux.

Linux es GPL-2.0; su código fuente vive en https://kernel.org y el árbol
de Tiny Core en http://tinycorelinux.net.
