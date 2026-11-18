#!/usr/bin/env python3
"""V04 · ¡A R-04 se le acaba la batería! (clip Grok GK1 + p.4). Uso: v04_bateria_r04.py <build> <salida.mp4>"""
import sys, os, subprocess
from PIL import Image
from lib import *
kit = Kit(sys.argv[1]); OUT = sys.argv[2]
GK = os.path.join(CLIPS, 'GK1_grok_original.mp4')

def grok_frames(start, dur):  # 480x624 -> escala a alto 1280 y recorta centro
    n = int(round(dur * FPS))
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(start), '-i', GK, '-t', str(dur + .2), '-vf',
                          f'fps={FPS},scale=-2:{H}:flags=lanczos,crop={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    fr = [Image.frombuffer('RGB', (W, H), raw[i*W*H*3:(i+1)*W*H*3]) for i in range(len(raw)//(W*H*3))]
    while len(fr) < n: fr.append(fr[-1])
    return fr[:n]

g = grok_frames(0, 2.9) + grok_frames(3.9, 2.1)  # se quita 2,9-3,9 s (Bityn saca boca)
TMP = OUT + '.gk%d.wav'
for k, (a, d) in enumerate(((0, 2.9), (3.9, 2.1))):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(a), '-t', str(d), '-i', GK, '-vn', '-ac', '2', '-ar', '44100', TMP % k], check=True)
t1 = kit.text([('¡A R-04 se le', BLANCO), ('acaba la batería!', AMARILLO)], 84)
t2 = kit.text([('Le quedan', BLANCO), ('30 días', NARANJA)], 110)
t3 = kit.text([('Y el chip que lo salva', BLANCO), ('cuesta 150 €', AMARILLO)], 80)
def s1(i, n):
    t = i / FPS; fr = g[i].convert('RGBA')
    if t < 2.2: place(fr, t1, CX, 120, t)
    elif t < 3.6: place(fr, t2, CX, 120, t - 2.2)
    else: place(fr, t3, CX, 120, t - 3.6)
    return fr
kit.add(5.0, s1); kit.sfx_at(0, os.path.abspath(TMP % 0), 1.0); kit.sfx_at(2.9, os.path.abspath(TMP % 1), 1.0); kit.sfx_at(2.2, 'rubber/select.mp3', .5); kit.sfx_at(3.6, 'rubber/select.mp3', .5)

f2 = clip_frames('G2d_trio_cohete.mp4', 0, 2.0); a = kit.text([('Su plan: un food truck', BLANCO), ('de batidos galácticos', AMARILLO)], 74)
def s2(i, n):
    fr = zoom(f2[i], 1 + .06 * i / n, .5, .7).convert('RGBA'); place(fr, a, CX, 110, i / FPS); return fr
t = kit.t0(1); kit.add(2.0, s2); kit.sfx_at(t, 'arcade/swipe.mp3', .7); kit.sfx_at(t + .1, 'arcade/purchase.mp3', .7)

f3 = clip_frames('G2a_lia_batido.mp4', 1.2, 1.9); b = kit.text([('Y tu hijo aprende', BLANCO), ('a hacer las cuentas', AMARILLO), ('con ellos', BLANCO)], 78)
def s3(i, n):
    fr = zoom(f3[i], 1.04 - .04 * i / n, .5, .6).convert('RGBA'); place(fr, b, CX, 100, i / FPS); return fr
t = kit.t0(2); kit.add(1.9, s3); kit.sfx_at(t, 'arcade/swipe.mp3', .7); kit.sfx_at(t + .1, 'rubber/select.mp3', .7)

last = g[-1]; q = kit.text([('¿Lo conseguirán?', BLANCO)], 96); q2 = kit.pill('Dínoslo en comentarios', 40, ROSA)
def s4(i, n):
    fr = zoom(last, 1.1 + .05 * i / n, .5, .55).convert('RGBA'); t = i / FPS
    place(fr, q, CX, 140, t); place(fr, q2, CX, 270, t - .2); return fr
t = kit.t0(3); kit.add(1.6, s4); kit.sfx_at(t, 'bip', .6); kit.sfx_at(t + .1, 'arcade/notification.mp3', .7)
cierre(kit, variante=0); kit.render(OUT)
for k in (0, 1): os.remove(TMP % k)
