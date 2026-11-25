#!/usr/bin/env python3
"""L1-04 · Vídeo 1 de la campaña (25 nov): «¿Tu peque sabe lo que cuesta ganar dinero?» (Mi primer dinero).
Fórmula: problema de padres → sketch (Bityn quiere todo / R-04: 2 monedas y una galleta) → solución del libro → producto → Amazon.
Material: kling/v1 (imágenes de Grok P1-P3 animadas A1-A3, voces V1-V5) + páginas reales del libro 1. Cierre 1 con portada del libro 1.
Uso: l1_04_ganar_dinero.py <build> <salida.mp4>"""
import sys, os, subprocess
from PIL import Image, ImageFilter
from lib import *
kit = Kit(sys.argv[1]); OUT = sys.argv[2]
V = os.path.join(REPO, 'kling', 'v1'); PG = os.path.join(REPO, 'libro1', 'paginas')
PORTADA1 = os.path.join(REPO, 'libro1', 'portada_frontal.png'); TMPS = []

def frames(name, dur):
    p = os.path.join(V, name)
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-vf', f'fps={FPS},scale={W}:-2:flags=lanczos', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                         capture_output=True, check=True).stdout
    h = len(raw) // (W * 3) // max(1, len(raw) // (W * 3 * 1310)) if False else 1310
    n = len(raw) // (W * h * 3); fr = [Image.frombuffer('RGB', (W, h), raw[i*W*h*3:(i+1)*W*h*3]) for i in range(n)]
    fr = fr + fr[::-1]  # ida y vuelta para clips cortos
    need = int(round(dur * FPS)); return [fr[i % len(fr)] for i in range(need)]

def shot(fr, i, z=1.0, cx=.5, cy=.45):
    f = fr[i]; w, h = f.size; nw, nh = W / z, H / z
    x0 = (w - nw) * cx; y0 = (h - nh) * cy
    return f.crop((int(x0), int(y0), int(x0 + nw), int(y0 + nh))).resize((W, H), Image.LANCZOS).convert('RGBA')

def voz(name, a, b, tempo=1.0):
    t = os.path.abspath(OUT + f'.{len(TMPS)}.wav'); TMPS.append(t)
    af = f'atrim={a}:{b},asetpts=PTS-STARTPTS' + (f',atempo={tempo}' if tempo != 1 else '')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(V, name), '-vn', '-af', af, '-ac', '2', '-ar', '44100', t], check=True)
    return t, (b - a) / tempo

# 1 · Gancho con la voz del narrador (V1) sobre P1 en tres encuadres
v1, d1 = voz('V1_narrador.mp4', 0.40, 9.10, 1.2)
a1 = frames('A1.mp4', d1)
t1a = kit.text([('¿Tu peque sabe lo que', BLANCO), ('cuesta ganar dinero?', AMARILLO)], 80)
t1b = kit.text([('…¿o cree que sale', BLANCO), ('solo de tu cartera?', AMARILLO)], 80)
def s1(i, n):
    t = i / FPS; k = i / n
    if t < d1 * .4: fr = shot(a1, i, 1.0 + .06 * k); place(fr, t1a, CX, 120, t)
    elif t < d1 * .72: fr = shot(a1, i, 1.7, .25, .42); place(fr, t1b, CX, 120, t - d1 * .4)
    else: fr = shot(a1, i, 1.45, .62, .62); place(fr, t1b, CX, 120, 1)
    return fr
kit.add(d1, s1); kit.sfx_at(0, v1, 1.0); kit.sfx_at(0, 'arcade/coupon.mp3', .4); kit.sfx_at(d1 * .4, 'arcade/swipe.mp3', .4); kit.sfx_at(d1 * .72, 'arcade/swipe.mp3', .4)

# 2 · Bityn: «¡R-04, quiero comprármelo todo!» (V2) sobre P2
v2, d2 = voz('V2_bityn.mp4', 0.45, 3.20)
a2 = frames('A2.mp4', d2)
t2 = kit.text([('«¡Quiero', BLANCO), ('comprármelo todo!»', AMARILLO)], 92)
def s2(i, n):
    t = i / FPS; fr = shot(a2, i, 1.0 + .08 * i / n, .5, .4); place(fr, t2, CX, 120, t); return fr
t = kit.t0(1); kit.add(d2, s2); kit.sfx_at(t, v2, 1.0); kit.sfx_at(t, 'arcade/swipe.mp3', .5)

# 3 · R-04: «Bip. Saldo disponible: dos monedas… y una galleta.» (V3) sobre P3
v3, d3 = voz('V3_r04.mp4', 0.0, 4.30)
a3 = frames('A3.mp4', d3)
t3a = kit.pill('SALDO DISPONIBLE', 40, AZUL); t3b = kit.text([('2 monedas…', BLANCO), ('y una galleta', AMARILLO)], 100)
def s3(i, n):
    t = i / FPS; fr = shot(a3, i, 1.0 + .1 * i / n, .5, .45); place(fr, t3a, CX, 150, t - .3); place(fr, t3b, CX, 860, t - 1.6); return fr
t = kit.t0(2); kit.add(d3, s3); kit.sfx_at(t, v3, 1.0); kit.sfx_at(t + d3 - .5, 'arcade/error.mp3', .6)

# 4 · La solución: páginas REALES del libro 1 (V4)
v4, d4 = voz('V4_narrador.mp4', 0.0, 9.30, 1.2)
paginas = [(6, 'Un cómic con humor'), (17, 'Decisiones de compra'), (41, 'Trabajos y beneficios'), (79, 'Juego de mesa recortable'), (81, 'Para jugar en familia'), (57, 'Aventura «elige tu camino»')]
pags = [Image.open(os.path.join(PG, f'pag_{n:03d}.jpg')).convert('RGB') for n, _ in paginas]
labs = [kit.pill(l, 40, NARANJA) for _, l in paginas]
seg = d4 / len(paginas)
def s4(i, n):
    t = i / FPS; j = min(len(pags) - 1, int(t / seg)); tt = t - j * seg
    p = pags[j]; fr = fill_bg(p, 26, .45).convert('RGBA'); z = 1 + .08 * tt / seg
    w = int(560 * z); h = int(p.height * w / p.width); im = p.resize((w, h), Image.LANCZOS)
    shadowed(fr, im, CX - w // 2, 250 - (h - int(p.height * 560 / p.width)) // 2)
    place(fr, kit.text([('Mi primer dinero', AMARILLO)], 80), CX, 90, t)
    place(fr, labs[j], CX, 990, tt); return fr
t = kit.t0(3); kit.add(d4, s4); kit.sfx_at(t, v4, 1.0)
for j in range(len(paginas)): kit.sfx_at(t + j * seg, 'arcade/swipe.mp3', .35)

# 5 · Venta (V5) sobre el cierre con portada
v5, d5 = voz('V5_narrador.mp4', 0.38, 4.90, 1.1)
t = kit.t0(4); kit.sfx_at(t, v5, 1.0)
cierre(kit, dur=max(2.5, d5 + .2), variante=1, color=(255, 170, 60), portada=PORTADA1)
kit.render(OUT)
for f in TMPS: os.remove(f)
