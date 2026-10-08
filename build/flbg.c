// flbg: fija el fondo de la ventana raiz X11 desde un BMP de 24 bits
// sin comprimir (escalado "cover": llena la pantalla recortando el
// exceso, centrado). Solo depende de libX11.
// Uso: DISPLAY=:0 flbg /ruta/imagen.bmp
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <X11/Xlib.h>
#include <X11/Xatom.h>

static unsigned int rd16(const unsigned char *p)
{
    return (unsigned int)p[0] | ((unsigned int)p[1] << 8);
}
static unsigned long rd32(const unsigned char *p)
{
    return (unsigned long)p[0] | ((unsigned long)p[1] << 8) |
           ((unsigned long)p[2] << 16) | ((unsigned long)p[3] << 24);
}

/* Carga un BMP Windows 24-bit sin comprimir a memoria RGB (fila 0 = arriba) */
static int load_bmp(const char *path, unsigned char **rgb, int *w, int *h)
{
    FILE *f = fopen(path, "rb");
    if (!f) { fprintf(stderr, "flbg: no puedo abrir %s\n", path); return 1; }
    fseek(f, 0, SEEK_END);
    long len = ftell(f);
    fseek(f, 0, SEEK_SET);
    unsigned char *buf = (unsigned char *)malloc((size_t)len);
    if (!buf || fread(buf, 1, (size_t)len, f) != (size_t)len) {
        fclose(f); return 1;
    }
    fclose(f);
    if (len < 54 || buf[0] != 'B' || buf[1] != 'M') {
        fprintf(stderr, "flbg: no es un BMP valido\n"); free(buf); return 1;
    }
    unsigned long dataoff = rd32(buf + 10);
    unsigned long hdrsize = rd32(buf + 14);
    int width, height;
    int topdown = 0;
    if (hdrsize >= 40) {
        width = (int)(long)rd32(buf + 18);
        height = (int)(long)rd32(buf + 22);
        if (height < 0) { topdown = 1; height = -height; }
        unsigned int bpp = rd16(buf + 28);
        unsigned long comp = rd32(buf + 30);
        if (bpp != 24 || comp != 0) {
            fprintf(stderr, "flbg: BMP no soportado (bpp=%u comp=%lu)\n",
                    bpp, comp);
            free(buf); return 1;
        }
    } else {
        fprintf(stderr, "flbg: cabecera BMP antigua\n"); free(buf); return 1;
    }
    *w = width; *h = height;
    *rgb = (unsigned char *)malloc((size_t)width * height * 3u);
    if (!*rgb) { free(buf); return 1; }
    long rowsize = ((long)width * 3 + 3) & ~3L;
    for (int y = 0; y < height; y++) {
        int srcrow = topdown ? y : (height - 1 - y);
        const unsigned char *s = buf + dataoff + (long)srcrow * rowsize;
        unsigned char *d = *rgb + (size_t)y * width * 3u;
        for (int x = 0; x < width; x++) {
            d[x * 3 + 0] = s[x * 3 + 2]; /* BGR -> RGB */
            d[x * 3 + 1] = s[x * 3 + 1];
            d[x * 3 + 2] = s[x * 3 + 0];
        }
    }
    free(buf);
    return 0;
}

int main(int argc, char **argv)
{
    if (argc < 2) { fprintf(stderr, "uso: flbg imagen.bmp\n"); return 2; }
    unsigned char *src = NULL;
    int sw = 0, sh = 0;
    if (load_bmp(argv[1], &src, &sw, &sh) != 0) {
        fprintf(stderr, "flbg: error leyendo el BMP\n");
        return 1;
    }

    Display *dpy = XOpenDisplay(NULL);
    if (!dpy) { fprintf(stderr, "flbg: no puedo abrir el display\n"); return 1; }
    int scr = DefaultScreen(dpy);
    Window root = RootWindow(dpy, scr);
    int dw = DisplayWidth(dpy, scr);
    int dh = DisplayHeight(dpy, scr);
    Visual *vis = DefaultVisual(dpy, scr);
    int depth = DefaultDepth(dpy, scr);

    /* escala cover: factor = max(dw/sw, dh/sh), recorte centrado */
    double fx = (double)dw / sw, fy = (double)dh / sh;
    double f = fx > fy ? fx : fy;
    int vw = (int)(dw / f), vh = (int)(dh / f);
    int ox = (sw - vw) / 2, oy = (sh - vh) / 2;

    char *data = (char *)malloc((size_t)dw * dh * 4u);
    if (!data) return 1;
    for (int y = 0; y < dh; y++) {
        int sy = oy + (int)((double)y / f);
        if (sy >= sh) sy = sh - 1;
        const unsigned char *srow = src + (size_t)sy * sw * 3u;
        char *drow = data + (size_t)y * dw * 4u;
        for (int x = 0; x < dw; x++) {
            int sx = ox + (int)((double)x / f);
            if (sx >= sw) sx = sw - 1;
            const unsigned char *p = srow + (size_t)sx * 3u;
            drow[x * 4 + 0] = (char)p[2];
            drow[x * 4 + 1] = (char)p[1];
            drow[x * 4 + 2] = (char)p[0];
            drow[x * 4 + 3] = 0;
        }
    }
    free(src);

    XImage *img = XCreateImage(dpy, vis, (unsigned)depth, ZPixmap, 0,
                               data, (unsigned)dw, (unsigned)dh, 32, 0);
    if (!img) { fprintf(stderr, "flbg: XCreateImage fallo\n"); return 1; }
    Pixmap pm = XCreatePixmap(dpy, root, (unsigned)dw, (unsigned)dh, (unsigned)depth);
    GC gc = XCreateGC(dpy, pm, 0, NULL);
    XPutImage(dpy, pm, gc, img, 0, 0, 0, 0, (unsigned)dw, (unsigned)dh);
    XFreeGC(dpy, gc);

    XSetWindowBackgroundPixmap(dpy, root, pm);
    Atom a1 = XInternAtom(dpy, "_XROOTPMAP_ID", False);
    Atom a2 = XInternAtom(dpy, "ESETROOT_PMAP_ID", False);
    XChangeProperty(dpy, root, a1, XA_PIXMAP, 32, PropModeReplace,
                    (unsigned char *)&pm, 1);
    XChangeProperty(dpy, root, a2, XA_PIXMAP, 32, PropModeReplace,
                    (unsigned char *)&pm, 1);
    XClearWindow(dpy, root);
    XFlush(dpy);
    /* conservar el pixmap tras cerrar (lo posee el servidor) */
    XSetCloseDownMode(dpy, RetainTemporary);
    XCloseDisplay(dpy);
    free(data);
    return 0;
}
