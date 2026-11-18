#!/usr/bin/env python3
"""V04 · La batería de R-04 — SOLO escenas reales: viñeta p.3 (libro 2) + clip GK2 (Sr. Tornillo, p.4) + Cohete Goloso.
Uso: v04_bateria_r04.py <build> <pag3_300ppp.png> <pag4_300ppp.png> <salida.mp4>"""
import sys, os, subprocess
from PIL import Image
from lib import *
kit = Kit(sys.argv[1]); p3 = Image.open(sys.argv[2]).convert('RGB'); p4 = Image.open(sys.argv[3]).convert('RGB'); OUT = sys.argv[4]
k = p3.width / 935  # coords medidas a 110 ppp
pan = p3.crop((int(175*k), int(440*k), int(770*k), int(760*k)))  # Bityn atrapa a R-04 (¡ZAS!)
def s1(i, n):
    t = i / FPS; fr = Image.new('RGBA', (W, H), (255, 214, 64, 255)); z = 1 + .15 * i / n
    h = int(1280 * .62); w = int(pan.width * h / pan.height); im = pan.resize((int(w * z), int(h * z)), Image.LANCZOS)
    x = int(-(im.width - W) * (0.15 + .5 * i / n)); fr.paste(im, (x, 330)); place(fr, t1, CX, 90, t); return fr
t1 = kit.text([('¡A R-04 se le', BLANCO), ('acaba la batería!', AMARILLO)], 86)
kit.add(2.0, s1); kit.sfx_at(0, 'bip', .7); kit.sfx_at(.3, 'arcade/error.mp3', .6)

GK = os.path.join(CLIPS, 'GK2_tornillo_chip_original.mp4'); A, D = 0.6, 5.2
raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(A), '-i', GK, '-t', str(D + .2), '-vf', f'fps={FPS},scale={W}:-2:flags=lanczos,crop={W}:{H}',
                      '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
g = [Image.frombuffer('RGB', (W, H), raw[i*W*H*3:(i+1)*W*H*3]) for i in range(len(raw)//(W*H*3))]
g += [g[-1]] * max(0, int(D * FPS) - len(g))
TMP = OUT + '.gk.wav'; subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(A), '-t', str(D), '-i', GK, '-vn', '-ac', '2', '-ar', '44100', TMP], check=True)
a1 = kit.pill('El Sr. Tornillo lo sabe', 34, (120, 80, 200)); a2 = kit.text([('Solo lo salva', BLANCO), ('un Chip Estelar', AMARILLO)], 86)
a3 = kit.text([('Cuesta 150 €…', BLANCO), ('¡y Bityn tiene 18!', NARANJA)], 86)
def s2(i, n):
    t = i / FPS; fr = g[i].convert('RGBA')
    if t < 2.8: place(fr, a1, CX, 95, t); place(fr, a2, CX, 150, t - .1)
    else: place(fr, a3, CX, 110, t - 2.8)
    return fr
t = kit.t0(1); kit.add(D, s2); kit.sfx_at(t, os.path.abspath(TMP), 1.0); kit.sfx_at(t, 'arcade/swipe.mp3', .5); kit.sfx_at(t + 2.8, 'arcade/error.mp3', .5)

f3 = clip_frames('G2d_trio_cohete.mp4', 0, 2.0); b = kit.text([('Su plan: un food truck', BLANCO), ('de batidos galácticos', AMARILLO)], 74)
def s3(i, n):
    fr = zoom(f3[i], 1 + .06 * i / n, .5, .7).convert('RGBA'); place(fr, b, CX, 110, i / FPS); return fr
t = kit.t0(2); kit.add(2.0, s3); kit.sfx_at(t, 'arcade/swipe.mp3', .7); kit.sfx_at(t + .1, 'arcade/purchase.mp3', .7)

k4 = p4.width / 2550; pp = p4.crop((int(400*k4), int(2016*k4), int(2100*k4), int(2870*k4)))  # «Tranquilo, R-04... Te lo prometo»
q = kit.text([('30 días para', BLANCO), ('salvar a R-04', AMARILLO)], 92); q2 = kit.pill('¿Lo conseguirán? Comenta 👇'.replace(' 👇', ''), 38, ROSA)
def s4(i, n):
    t = i / FPS; fr = Image.new('RGBA', (W, H), (40, 30, 90, 255)); z = 1 + .08 * i / n
    w = 640; h = int(pp.height * w / pp.width); im = pp.resize((int(w * z), int(h * z)), Image.LANCZOS)
    shadowed(fr, im, CX - im.width // 2, 360); place(fr, q, CX, 100, t); place(fr, q2, CX, 360 + h + 30, t - .25); return fr
t = kit.t0(3); kit.add(2.0, s4); kit.sfx_at(t, 'arcade/swipe.mp3', .7); kit.sfx_at(t + .2, 'bip', .6)
cierre(kit, variante=0); kit.render(OUT); os.remove(TMP)
