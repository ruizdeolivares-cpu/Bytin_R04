#!/usr/bin/env python3
"""V07 · ¿Todo el dinero que entra es tuyo? (beneficio). SOLO escenas reales: Misión 10 «La calculadora no miente» (p.41),
fórmula y R-04 sin batería (p.42), «Lo que aprenden» (p.44). Sin clips de IA. Cierre variante 0.
Uso: v07_beneficio.py <build> <salida.mp4>"""
import sys, os
from PIL import Image, ImageDraw, ImageFilter
from lib import *
kit = Kit(sys.argv[1]); OUT = sys.argv[2]
PG = os.path.join(REPO, 'libro', 'paginas')
p41, p42 = (Image.open(os.path.join(PG, f'pag_{n}.jpg')).convert('RGB') for n in (41, 42))
PIZARRA = (28, 70, 52)

def nitido(c): return c.filter(ImageFilter.UnsharpMask(2, 80, 2))

def pan(src, box, h, y, rev=False, bgcol=None, rango=(0, 1)):
    """Viñeta ancha grande con barrido dentro de la zona segura (x 16..620)."""
    c = src.crop(box); w = int(c.width * h / c.height); im = nitido(c.resize((w, h), Image.LANCZOS))
    bg = fill_bg(c, 28, .45) if bgcol is None else Image.new('RGB', (W, H), bgcol)
    def draw(i, n):
        fr = bg.copy().convert('RGBA'); k = i / max(1, n - 1); k = k * k * (3 - 2 * k)
        if rev: k = 1 - k
        k = rango[0] + (rango[1] - rango[0]) * k
        fr.paste(im, (int(16 + (620 - 16 - w) * k), y)); return fr
    return draw

def caja(src, box, w, y, zmax=.08, bgcol=None):
    """Viñeta vertical/cuadrada centrada con zoom lento."""
    c = src.crop(box); h = int(c.height * w / c.width); pn = nitido(c.resize((w, h), Image.LANCZOS))
    bg = fill_bg(c, 28, .45) if bgcol is None else Image.new('RGB', (W, H), bgcol)
    def draw(i, n):
        fr = bg.copy().convert('RGBA'); z = 1 + zmax * i / n
        im = pn.resize((int(pn.width * z), int(pn.height * z)), Image.LANCZOS)
        shadowed(fr, im, CX - im.width // 2, y - (im.height - pn.height) // 2); return fr
    return draw, h

# 1 · Gancho (2,0 s): Bityn vacía el bote de monedas
d1 = pan(p41, (150, 288, 795, 555), 560, 420, rango=(0, .45))
g1 = kit.text([('¿Todo el dinero', BLANCO), ('que entra es tuyo?', AMARILLO)], 90)
def s1(i, n):
    fr = d1(i, n); place(fr, g1, CX, 110, i / FPS); return fr
kit.add(2.0, s1); kit.sfx_at(0, 'arcade/reward.mp3', .6); kit.sfx_at(.1, 'arcade/purchase.mp3', .5)

# 2 · «¡164 €! ¡Nos sobra!» (1,6 s) — mismo plano, se para el barrido en Bityn y entra su frase
d2 = pan(p41, (150, 288, 795, 555), 560, 420, rango=(.12, 0))
b1 = kit.pill('Bityn', 36, NARANJA); b2 = kit.text([('«¡164 euros!', BLANCO), ('¡Nos sobra!»', AMARILLO)], 84)
def s2(i, n):
    t = i / FPS; fr = d2(i, n); place(fr, b1, CX, 165, t); place(fr, b2, CX, 215, t - .1); return fr
t = kit.t0(1); kit.add(1.6, s2); kit.sfx_at(t, 'arcade/swipe.mp3', .5); kit.sfx_at(t + .15, 'arcade/coupon.mp3', .6)

# 3 · R-04 con la calculadora (2,2 s)
d3, h3 = caja(p41, (152, 557, 425, 838), 450, 235)
r1 = kit.pill('R-04', 36, AZUL); r2 = kit.text([('«Bip. Estar en tu bote', BLANCO), ('no significa', BLANCO), ('que sea tuyo»', AMARILLO)], 74)
def s3(i, n):
    t = i / FPS; fr = d3(i, n); place(fr, r1, CX, 165, t); place(fr, r2, CX, 235 + h3 + 25, t - .15); return fr
t = kit.t0(2); kit.add(2.2, s3); kit.sfx_at(t, 'arcade/swipe.mp3', .5); kit.sfx_at(t + .1, 'bip', .7); kit.sfx_at(t + .5, 'arcade/typing.mp3', .5)

# 4 · La cuenta de la verdad (2,6 s): 164 − 56 − 14 = 94 (p.41)
filas = [('Entra', '164 €', BLANCO), ('− Frutería', '56 €', (255, 150, 150)), ('− Brillo', '14 €', (255, 150, 150)), ('= Vuestro', '94 €', AMARILLO)]
fn_ = kit.font(78)
def fila(a, b, col):
    im = Image.new('RGBA', (560, 110), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((10, 8), a, font=fn_, fill=col, stroke_width=6, stroke_fill=OSCURO)
    wb = fn_.getbbox(b, stroke_width=6)[2]; d.text((550 - wb, 8), b, font=fn_, fill=col, stroke_width=6, stroke_fill=OSCURO); return im
F = [fila(*f) for f in filas]
c0 = kit.text([('La cuenta', BLANCO), ('de verdad', AMARILLO)], 92)
def s4(i, n):
    t = i / FPS; fr = Image.new('RGBA', (W, H), PIZARRA + (255,)); d = ImageDraw.Draw(fr)
    d.rounded_rectangle((22, 330, 614, 900), radius=24, outline=(140, 95, 55), width=14)
    place(fr, c0, CX, 100, t)
    for j, im in enumerate(F):
        if j == 3 and t > .3 + .4 * 3: d.line((50, 380 + 3 * 120 - 8, 590, 380 + 3 * 120 - 8), fill=(240, 240, 220), width=5)
        place(fr, im, CX, 380 + j * 120, t - .3 - .4 * j)
    return fr
t = kit.t0(3); kit.add(2.6, s4)
for j in range(4): kit.sfx_at(t + .3 + .4 * j, 'arcade/progress-step.mp3' if j < 3 else 'arcade/error.mp3', .7)

# 5 · Bityn con las manos en la cabeza (1,8 s) (p.41)
d5, h5 = caja(p41, (290, 850, 640, 1052), 600, 400)
e1 = kit.text([('«¿¡Solo 94!?»', BLANCO)], 100); e2 = kit.pill('Faltan 56 € y quedan 10 días', 34, ROSA)
def s5(i, n):
    t = i / FPS; fr = d5(i, n); place(fr, e1, CX, 150, t); place(fr, e2, CX, 400 + h5 + 30, t - .3); return fr
t = kit.t0(4); kit.add(1.8, s5); kit.sfx_at(t, 'arcade/swipe.mp3', .5); kit.sfx_at(t + .1, 'arcade/error.mp3', .7)

# 6 · La fórmula (p.42) (2,2 s)
d6, h6 = caja(p42, (147, 180, 520, 450), 560, 330, bgcol=(255, 214, 64))
f1 = kit.text([('Ingresos − gastos', BLANCO), ('= BENEFICIO', NARANJA)], 92)
f2 = kit.pill('Lo que de verdad es tuyo', 38, OSCURO)
def s6(i, n):
    t = i / FPS; fr = d6(i, n); place(fr, f1, CX, 90, t); place(fr, f2, CX, 330 + h6 + 30, t - .35); return fr
t = kit.t0(5); kit.add(2.2, s6); kit.sfx_at(t, 'arcade/swipe.mp3', .5); kit.sfx_at(t + .15, 'arcade/unlock.mp3', .7)

# 7 · Tensión final: R-04 se apaga (p.42) (1,8 s)
d7, h7 = caja(p42, (522, 180, 780, 450), 470, 360, zmax=.12, bgcol=(30, 25, 60))
z1 = kit.text([('Y a R-04 se le', BLANCO), ('acaba la batería…', AMARILLO)], 80)
z2 = kit.pill('¿Tu hijo o hija sabría hacer la cuenta?', 29, NARANJA)
def s7(i, n):
    t = i / FPS; fr = d7(i, n); place(fr, z1, CX, 110, t); place(fr, z2, CX, 360 + h7 + 30, t - .35); return fr
t = kit.t0(6); kit.add(1.8, s7); kit.sfx_at(t, 'arcade/swipe.mp3', .5); kit.sfx_at(t + .1, 'bip', .5); kit.sfx_at(t + .5, 'arcade/sleep.mp3', .6)

cierre(kit, variante=0); kit.render(OUT)
