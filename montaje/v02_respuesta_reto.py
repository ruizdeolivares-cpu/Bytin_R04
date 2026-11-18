#!/usr/bin/env python3
"""V02 · Respuesta del reto de los batidos (p.69 #6). Uso: v02_respuesta_reto.py <build> <pagina69.png|jpg> <salida.mp4>"""
import sys
from PIL import Image, ImageDraw
from lib import *
kit = Kit(sys.argv[1]); pg = Image.open(sys.argv[2]).convert('RGB'); OUT = sys.argv[3]
sx = pg.width / 1700  # coordenadas medidas a 200 ppp

f = clip_frames('G2c_r04_interrogacion.mp4', 0.0, 1.8)
a1 = kit.pill('RESPUESTA DEL RETO', 34, NARANJA); a2 = kit.text([('¿Tu hijo', BLANCO), ('acertó?', AMARILLO)], 96)
def s1(i, n):
    fr = zoom(f[i], 1 + .06 * i / n).convert('RGBA'); t = i / FPS
    place(fr, a1, CX, 175, t); place(fr, a2, CX, 240, t - .12); return fr
kit.add(1.8, s1); kit.sfx_at(0, 'bip', .6); kit.sfx_at(.12, 'arcade/notification.mp3')

def opcion(clip, st, z0, cy, tag, col, l1, l2):
    fr_ = clip_frames(clip, st, 1.9); p = kit.pill(tag, 38, col); tx = kit.text([(l1, BLANCO), (l2, AMARILLO)], 84)
    def fn(i, n):
        fr = zoom(fr_[i], z0 + .05 * i / n, .5, cy).convert('RGBA'); t = i / FPS
        place(fr, p, CX, 105, t); place(fr, tx, CX, 175, t - .12); return fr
    return fn
t = kit.t0(1); kit.add(1.9, opcion('G3a_bityn_rasca_cabeza.mp4', .2, 1.1, .65, 'OPCIÓN A · 2 €', AZUL, '40 × 1 € =', '40 € de beneficio'))
kit.sfx_at(t, 'arcade/swipe.mp3', .7); kit.sfx_at(t + .15, 'arcade/purchase.mp3')
t = kit.t0(2); kit.add(1.9, opcion('G3b_bityn_idea.mp4', .1, 1.0, .75, 'OPCIÓN B · 3 €', ROSA, '25 × 2 € =', '50 € de beneficio'))
kit.sfx_at(t, 'arcade/swipe.mp3', .7); kit.sfx_at(t + .15, 'arcade/purchase.mp3')

f4 = clip_frames('G1b_bityn_monedas.mp4', 0, 1.6); g = kit.text([('¡Gana', BLANCO), ('la B!', AMARILLO)], 150, stroke=12)
def s4(i, n):
    fr = zoom(f4[i], 1.05 + .08 * i / n).convert('RGBA'); place(fr, g, CX, 150, i / FPS, .3); return fr
t = kit.t0(3); kit.add(1.6, s4); kit.sfx_at(t, 'arcade/swipe.mp3', .7); kit.sfx_at(t + .1, 'arcade/level-up.mp3', .9)

f5 = clip_frames('G3d_ambos_pulgar.mp4', 0, 2.2); q = kit.text([('Vender más', BLANCO), ('no siempre es', BLANCO), ('ganar más', NARANJA)], 92)
def s5(i, n):
    fr = zoom(f5[i], 1 + .05 * i / n, .5, .8).convert('RGBA'); place(fr, q, CX, 110, i / FPS); return fr
t = kit.t0(4); kit.add(2.2, s5); kit.sfx_at(t, 'bip', .7); kit.sfx_at(t + .1, 'rubber/select.mp3')

pw0 = 600; ph0 = int(pg.height * pw0 / pg.width); pgs = pg.resize((pw0, ph0), Image.LANCZOS); k = pw0 / pg.width
ImageDraw.Draw(pgs).rounded_rectangle((int(150*sx*k), int(1590*sx*k), int(1570*sx*k), int(1755*sx*k)), radius=10, outline=NARANJA, width=5)
p1 = kit.text([('Está en el libro', BLANCO), ('con 5 retos más', AMARILLO)], 84)
def s6(i, n):
    t = i / FPS; z = 1 + .12 * i / n; im = pgs.resize((int(pw0 * z), int(ph0 * z)), Image.LANCZOS)
    fr = Image.new('RGBA', (W, H), (255, 236, 200, 255)); y = 300 - int((z - 1) * 1670 * sx * k)
    shadowed(fr, im, CX - im.width // 2, y, 90); place(fr, p1, CX, 80, t); return fr
t = kit.t0(5); kit.add(1.9, s6); kit.sfx_at(t, 'arcade/swipe.mp3', .7)

cierre(kit); kit.render(OUT)
