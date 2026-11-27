#!/usr/bin/env python3
"""V08 · Black Friday: el libro FÍSICO en manos de Francisco (Mi goloso negocio).
Material: libro_fisico/IMG_7477_720.mp4 y IMG_7478_720.mp4 (grabados por Francisco, 26 nov; versiones 720×1280 de los .MOV).
Sin IA. Sonido = las páginas reales (audio original subido) + SFX suaves. Cierre variante 2.
Uso: v08_libro_fisico.py <build> <salida.mp4>"""
import sys, os, subprocess
from PIL import Image
from lib import *
kit = Kit(sys.argv[1]); OUT = sys.argv[2]
LF = os.path.join(REPO, 'libro_fisico'); TMPS = []

def tramo(src, a, b, speed):
    """Fotogramas y audio del tramo a-b del vídeo, acelerado ×speed."""
    p = os.path.join(LF, src); dur = (b - a) / speed; n = int(round(dur * FPS))
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(a), '-t', str(b - a), '-i', p, '-vf', f'setpts=PTS/{speed},fps={FPS},scale={W}:{H}',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    fr = [Image.frombuffer('RGB', (W, H), raw[i*W*H*3:(i+1)*W*H*3]) for i in range(len(raw) // (W*H*3))]
    while len(fr) < n: fr.append(fr[-1])
    t = os.path.abspath(OUT + f'.{len(TMPS)}.wav'); TMPS.append(t)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(a), '-t', str(b - a), '-i', p, '-vn', '-af', f'atempo={speed},volume=12',
                    '-ac', '2', '-ar', '44100', t], check=True)
    return fr[:n], dur, t

def seg(src, a, b, speed, overlays, z=1.22, cy=.75):
    fr, dur, au = tramo(src, a, b, speed)
    def fn(i, n):
        t = i / FPS; f = zoom(fr[i], z, .5, cy).convert('RGBA')
        for o in overlays:
            ov, y, t0 = o[:3]
            if len(o) < 4 or t < o[3]: place(f, ov, CX, y, t - t0)
        return f
    t = kit.t0(len(kit.segments)); kit.add(dur, fn); kit.sfx_at(t, au, 1.0)
    return t

# 1 · Gancho (texto ya visible en el fotograma 0): portada sobre la mesa
bf = kit.pill('IDEA DE REGALO · BLACK FRIDAY', 30, OSCURO, AMARILLO)
h1 = kit.text([('¿Regalo para tu peque', BLANCO), ('de 8 a 12 años?', AMARILLO)], 74)
h2 = kit.pill('Ni tablet ni consola', 44, ROSA)
seg('IMG_7478_720.mp4', 0.2, 2.4, 1.0, [(bf, 22, -1, 0.9), (h2, 18, 0.9), (h1, 835, -1)], z=1.15, cy=.8)
kit.sfx_at(0.8, 'arcade/coupon.mp3', .25)

# 2-5 · Hojeando: lo que trae dentro (todo verificado en guia_contenido.md)
labs = [('Cómic de aventuras', NARANJA, 'IMG_7478_720.mp4', 7.2, 10.6, 1.7),
        ('Juego online con QR', AZUL, 'IMG_7477_720.mp4', 8.3, 10.0, 1.2),
        ('Retos de cuentas por niveles', VERDE, 'IMG_7478_720.mp4', 15.0, 19.0, 2.0),
        ('94 páginas de aventura', ROSA, 'IMG_7477_720.mp4', 11.5, 16.0, 2.2)]
tit = kit.text([('Mira lo que', BLANCO), ('trae dentro', AMARILLO)], 70)
for k, (txt, col, src, a, b, sp) in enumerate(labs):
    t = seg(src, a, b, sp, [(tit, 80, -1 if k else 0), (kit.pill(txt, 40, col), 900, 0.1)])
    kit.sfx_at(t, 'arcade/swipe.mp3', .2); kit.sfx_at(t + .1, 'arcade/coupon.mp3', .15)

# 6 · Portada en la mano
f1 = kit.text([('Un regalo que no', BLANCO), ('acaba en 5 minutos', AMARILLO)], 70)
t = seg('IMG_7477_720.mp4', 18.8, 22.0, 1.35, [(f1, 835, -1)], z=1.2, cy=.7)
kit.sfx_at(t, 'arcade/swipe.mp3', .2)

cierre(kit, dur=2.5, variante=2)
kit.render(OUT)
for f in TMPS: os.remove(f)
