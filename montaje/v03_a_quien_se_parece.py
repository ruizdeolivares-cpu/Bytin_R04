#!/usr/bin/env python3
"""V03 · ¿A quién se parece tu hijo o hija? (tarjetas de personajes; frases de p.2). Uso: v03_a_quien_se_parece.py <build> <salida.mp4>"""
import sys, os
from PIL import Image
from lib import *
kit = Kit(sys.argv[1]); OUT = sys.argv[2]
P = lambda n: Image.open(os.path.join(PERS, n)).convert('RGB')
cards = [('tarjeta_bityn.png', 'BITYN', 'El entusiasta', ('«¡Batidos galácticos', 'para todo el barrio!»'), AZUL),
         ('tarjeta_r04.png', 'R-04', 'El sensato', ('«Bip… batería baja…', 'pero ánimo alto»'), AZUL),
         ('tarjeta_lia.png', 'LÍA', 'La creativa', ('Inventora de sabores',), NARANJA),
         ('tarjeta_sr_tornillo.png', 'SR. TORNILLO', 'El sabio', ('«Sabe cuánto vale cada tornillo…', 'y cada persona»'), (120, 80, 200)),
         ('tarjeta_brillo.png', 'BRILLO', 'El vendedor', ('«¡MegaSnack!', '¡Todo a 1 €!»'), (220, 160, 0)),
         ('tarjeta_grunon_pepino.png', 'DON GRUÑÓN', 'El exigente', ('«Nada le gusta.', 'Casi nada.»'), VERDE)]
imgs = [P(c[0]) for c in cards]
# collage 2x3
cw, ch = 300, 256; col = Image.new('RGBA', (2 * cw + 12, 3 * ch + 24), (0, 0, 0, 0))
for k, im in enumerate(imgs): col.paste(im.resize((cw, ch), Image.LANCZOS), ((k % 2) * (cw + 12), (k // 2) * (ch + 12)))
bg0 = Image.new('RGB', (W, H), (255, 214, 64))
def collage_frame(i, n):
    fr = bg0.copy().convert('RGBA'); z = 1 + .04 * i / n
    c = col.resize((int(col.width * z), int(col.height * z)), Image.LANCZOS); fr.alpha_composite(c, (CX - c.width // 2, 440)); return fr
h1 = kit.pill('PADRES DE NIÑOS DE 8 A 12', 32, NARANJA); h2 = kit.text([('¿A quién se parece', BLANCO), ('tu hijo o hija?', NARANJA)], 88)
def s0(i, n):
    fr = collage_frame(i, n); t = i / FPS; place(fr, h1, CX, 170, t); place(fr, h2, CX, 225, t - .12); return fr
kit.add(1.8, s0); kit.sfx_at(0, 'arcade/notification.mp3'); kit.sfx_at(.1, 'bip', .5)

def card_scene(im, name, rasgo, cita, colr):
    bg = fill_bg(im, 35, .15); w = 600; h = int(im.height * w / im.width); base = im.resize((w, h), Image.LANCZOS)
    tn = kit.text([(name, BLANCO)], 96); tr = kit.pill(rasgo, 40, colr); tc = kit.text([(l, BLANCO) for l in cita], 50, stroke=7)
    def fn(i, n):
        t = i / FPS; fr = bg.copy().convert('RGBA'); z = 1 + .06 * i / n
        b = base.resize((int(w * z), int(h * z)), Image.LANCZOS); shadowed(fr, b, CX - b.width // 2, 330 - (b.height - h) // 2)
        place(fr, tn, CX, 95, t); place(fr, tr, CX, 230, t - .1); place(fr, tc, CX, 330 + h + 30, t - .25); return fr
    return fn
for k, c in enumerate(cards):
    t = kit.t0(len(kit.segments)); kit.add(1.5, card_scene(imgs[k], *c[1:]))
    kit.sfx_at(t, 'arcade/swipe.mp3', .6); kit.sfx_at(t + .1, 'bip' if c[1] == 'R-04' else 'rubber/select.mp3', .7)

e1 = kit.text([('¿Cuál es el tuyo?', BLANCO)], 84); e2 = kit.pill('Dínoslo en comentarios', 40, ROSA)
def s7(i, n):
    fr = collage_frame(i, n); t = i / FPS; place(fr, e1, CX, 120, t); place(fr, e2, CX, 245, t - .2); return fr
t = kit.t0(len(kit.segments)); kit.add(1.8, s7); kit.sfx_at(t, 'arcade/swipe.mp3', .6); kit.sfx_at(t + .2, 'arcade/notification.mp3')
cierre(kit, variante=2); kit.render(OUT)
