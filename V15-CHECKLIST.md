# FLinux-JC v1.5 — especificación consolidada (NO construida)

Estado general: **en pausa por instrucción de Juanca (2026-10-05). No armar la ISO hasta que él lo diga.**
Base: v1.4 publicada (flinux-jc-v1.4.iso, 294,649,856 B, MD5 efb5de414fafe11cd7a6c6aa2b327e06, confirmada en la Dell).

> **Actualización (autorización posterior):** el usuario dijo «Ok haz la versión 1.5 con todo lo nuevo, por ahora sería la versión final». Por tanto, esta pausa ya no se aplica a esta build: se construye v1.5 con los puntos 1–8 y con **flskin preinstalado** (punto 8 incluido). El vídeo de 20 s ya fue entregado y aceptado; se publica como Release v1.5 tras la verificación completa, incluida instalación en disco virtual con el instalador de la ISO y arranque desde disco.

## Cambios pedidos y su estado

1. **Letras de arranque «flinux-jc» en minúsculas** (en lugar de FLINUX), con degradado rojo sangre → naranja fluorescente → amarillo. Deben verse en la ISO, tras la instalación y en cada reinicio.
   - Estado: imagen de vista previa entregada y aprobada en diseño (v15-preview/flinux-jc-degradado-sobre-lava.png). Pendiente aplicar al construir.
2. **Fondo de arranque/GRUB con la imagen del robot** enviada por Juanca el 2026-10-05, manteniendo abajo las letras «flinux-jc» en minúsculas con el degradado.
   - Estado: aplicado y verificado solo en la ISO de prueba (isoroot-prueba-degradado/). La v1.4 publicada no se tocó.
3. **FLWM con degradado de 3 colores** en la barra de título.
   - Estado: probado; parche suelto flwm.tcz de 32 KB ya entregado para la 1.4 instalada (2026-10-05). Listo para integrar.
4. **Icono de FLConnect en el wbar**, clic = ejecutar como root.
   - Estado: verificado en la ISO de prueba. Lanzador correcto: `sudo /usr/local/bin/flconnect` (sudo sin clave para tc; HOME=/root para que se vean los perfiles). NO basta el setuid: con HOME=/home/tc la lista de perfiles sale vacía. Icono PNG (el wbar no pinta SVG).
5. **LXTask** (monitor de tareas) preinstalado.
   - Estado: pedido, pendiente de integrar al construir.
6. **getTime.sh automático en cada inicio** para ajustar hora y fecha a La Habana.
   - Estado: pedido, pendiente de integrar al construir.
7. **Fecha y hora en el Conky**.
   - Estado: pedido, pendiente de integrar al construir. (El vídeo de vista previa de 58 s ya lo muestra.)
8. **flskin** — programa FLTK (workspace/flinux-jc/flskin/): interruptor tema FLinux-JC por defecto ON/OFF (fondo lava + Conky naranja ↔ fondo neutro + Conky gris-azulado) e interruptor «Modo oscuro (Adwaita-dark)» ON/OFF, manteniendo siempre la barra de 3 colores. El oscuro se aplica a cada app al abrirla.
   - Estado: **construido y probado en QEMU** (flskin.tcz 49,152 B, MD5 4b6a28c9ab15cf81338e6287f9c9560f, .dep = fltk-1.3.tcz, directorios 755, icono PNG y .desktop incluidos). Vídeo de 20 s: videos/flskin-20s.mp4. Paquete suelto entregado el 2026-10-05 para probarlo en la 1.4.
   - **DECISIÓN PENDIENTE DE JUANCA:** ¿entra preinstalado en la v1.5? (pregunta ya hecha el 2026-10-05; sin respuesta aún).

## Entregables ya dados de la v1.5 (sin construir la ISO)

- Vídeo de vista previa de 58 s con todos los cambios (videos/v15-vista-previa.mp4), entregado.
- Imagen del degradado sobre lava, entregada.
- flwm.tcz con degradado para la 1.4 instalada, entregado con su .dep.
- flskin.tcz suelto para la 1.4, entregado con MD5.

## Al construir (cuando Juanca lo autorice)

- [ ] Partir de la v1.4 verificada; aplicar los puntos 1–7 (+ 8 si lo aprueba).
- [ ] Probar en QEMU i386: arranque con letras nuevas, escritorio, Conky con fecha/hora, LXTask, getTime.sh, wbar con FLConnect como root, FLWM degradado.
- [ ] Generar la ISO entera en un solo archivo (nada de trozos: su teléfono trunca a ~8 MB por adjunto, pero la ISO va por GitHub Release).
- [ ] Verificar que el SHA-256 de GitHub coincide con la ISO probada antes de pasarle el enlace.
- [ ] Enviarle la imagen final cuando esté terminada (pedido expreso).

## Notas que no hay que perder

- FLConnect v1.5 (el programa en sí) sigue en pausa aparte; aquí solo entra su icono/lanzador en el wbar.
- Cerrar la ventana de FLConnect no baja la interfaz WireGuard; se desconecta con el interruptor.
- La v1.4 publicada no se modifica: todo cambio va en la v1.5 nueva.

## Hecho (2026-10-05) — v1.5 construida, verificada y publicada

- [x] Construida sobre la v1.4 con los puntos 1–7 + flskin (punto 8; Juanca autorizó «todo lo nuevo»).
- [x] Probada en QEMU i386: menú robot+letras, escritorio lava, Conky fecha/hora numérica, hora CDT (nortc + zonefile; hallazgo: el unpacker del kernel exige entradas de directorio explícitas en el cpio para ficheros nuevos), degradado FLWM medido por píxeles, FLConnect desde el wbar como root viendo perfiles de /root, LXTask, flskin (neutro/oscuro/reversible).
- [x] Instalación en disco virtual con el instalador GUI de la ISO (CD de utilidades CorePlus como fuente de paquetes sin Internet): frugal/ext4/bootloader. El instalador deja el `extlinux.conf` plano → ajuste aplicado (vesamenu.c32 + libcom32/libutil + fjcbg.png + 4 líneas `UI/MENU TITLE/MENU BACKGROUND/TIMEOUT`), verificado en 2 reinicios (menú tematizado) + escritorio instalado completo.
- [x] ISO única: flinux-jc-v1.5.iso, 295,698,432 B, MD5 2446335f0a18ba48e7778e3b5ddc7984, SHA-256 7e85e0e9e97674294d52ee9051b033243768e00e1768295d7a40db62acd10f07.
- [x] Release v1.5 publicado: https://github.com/jcarlosrf26/flinux-jc/releases/tag/v1.5 — digest SHA-256 de GitHub idéntico al local verificado.
- [x] INFORME.md §12 escrito.

Desviaciones reportadas: flskin.tcz con MD5 nuevo (119a5aded07354329d0370c21a921ff3) por la fecha numérica en sus conkyrc; el menú tematizado en disco instalado requiere el ajuste documentado (el instalador stock lo deja plano).
