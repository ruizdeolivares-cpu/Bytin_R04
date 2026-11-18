#!/usr/bin/env python3
"""V05 · Enigma de X: el precio. SOLO escenas reales: nota de X (p.16), Misión 4 «El precio justo… ¡o el precio loco!» (p.17)
y consejo del Sr. Tornillo + precio de 2 € (p.18). Sin clips de IA. Cierre variante 1.
Uso: v05_enigma_x_precio.py <build> <salida.mp4>"""
import sys, os
from PIL import Image, ImageDraw, ImageFilter
from lib import *
kit = Kit(sys.argv[1]); OUT = sys.argv[2]
PG = os.path.join(REPO, 'libro', 'paginas')
p16, p17, p18 = (Image.open(os.path.join(PG, f'pag_{n}.jpg')).convert('RGB') for n in (16, 17, 18))
MORADO = (120, 70, 200)

def panel(src, box, w=600):
    c = src.crop(box); h = int(c.height * w / c.width)
    return c.resize((w, h), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 80, 2))

def pan(src, box, h, y, rev=False, blur=True, bgcol=None):
    """Viñeta ancha a gran tamaño con barrido horizontal (izq→der, o der→izq si rev)."""
    c = src.crop(box); w = int(c.width * h / c.height)
    im = c.resize((w, h), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 80, 2))
    bg = fill_bg(c, 28, .45) if blur else Image.new('RGB', (W, H), bgcol)
    def draw(i, n):
        fr = bg.copy().convert('RGBA'); k = i / max(1, n - 1); k = k * k * (3 - 2 * k)
        if rev: k = 1 - k
        x = int(16 + (620 - 16 - w) * k); fr.paste(im, (x, y)); return fr
    return draw, h

def escena(pn, bgcol, y, zmax=.06, blur=True):
    """Viñeta centrada en la zona segura con zoom lento; fondo = viñeta desenfocada o color."""
    bg = fill_bg(pn, 28, .45) if blur else Image.new('RGB', (W, H), bgcol)
    def draw(i, n):
        fr = bg.copy().convert('RGBA'); z = 1 + zmax * i / n
        im = pn.resize((int(pn.width * z), int(pn.height * z)), Image.LANCZOS)
        shadowed(fr, im, CX - im.width // 2, y - (im.height - pn.height) // 2); return fr
    return draw

# 1 · Gancho (1,8 s): Bityn y su batido de 50 €
P1 = panel(p17, (85, 250, 478, 545), 560)
g1 = kit.text([('¿Tu hijo o hija', BLANCO), ('sabría poner precio?', AMARILLO)], 88)
d1 = escena(P1, None, 400, .10)
def s1(i, n):
    fr = d1(i, n); place(fr, g1, CX, 110, i / FPS); return fr
kit.add(1.8, s1); kit.sfx_at(0, 'arcade/swipe.mp3', .7); kit.sfx_at(.15, 'bip', .6)

# 2 · Nota de X (3,0 s) — p.16 (el libro dice «vendréis»: errata; en pantalla, «venderéis»)
NX = panel(p16, (588, 152, 814, 294), 420)
n0 = kit.pill('X les dejó una nota…', 40, MORADO)
n1 = kit.text([('«Si cobráis mucho,', BLANCO), ('no venderéis nada…', BLANCO)], 70)
n2 = kit.text([('…si cobráis poco,', AMARILLO), ('trabajaréis gratis»', AMARILLO)], 70)
n3 = kit.pill('Tic, tac', 34, OSCURO)
def s2(i, n):
    t = i / FPS; fr = Image.new('RGBA', (W, H), (45, 25, 85, 255))
    k = ease_pop(t, .3)
    if k > 0:
        im = NX.resize((max(1, int(NX.width * k)), max(1, int(NX.height * k))))
        shadowed(fr, im, CX - im.width // 2, 250 + (NX.height - im.height) // 2)
    place(fr, n0, CX, 150, t - .05); place(fr, n1, CX, 590, t - .4); place(fr, n2, CX, 770, t - 1.4); place(fr, n3, CX, 960, t - 2.2)
    return fr
t = kit.t0(1); kit.add(3.0, s2)
kit.sfx_at(t, 'arcade/notification.mp3', .7); kit.sfx_at(t + .4, 'arcade/typing.mp3', .5); kit.sfx_at(t + 1.4, 'arcade/typing.mp3', .5)
kit.sfx_at(t + 2.2, 'arcade/progress-step.mp3', .7); kit.sfx_at(t + 2.55, 'arcade/progress-step.mp3', .7)

# 3 · Enigma A/B (3,0 s) con cuenta atrás
A = panel(p17, (320, 300, 470, 480), 280); B = panel(p17, (400, 600, 620, 864), 280)
q = kit.text([('Bityn probó 2 precios.', BLANCO), ('¿Cuál salió PEOR?', AMARILLO)], 80)
la, lb = kit.pill('A · 50 €', 44, ROSA), kit.pill('B · 0,10 €', 44, AZUL)
cm = kit.pill('Comenta A o B', 42, NARANJA)
nums = [kit.text([(s, BLANCO)], 150, stroke=12) for s in ('3', '2', '1')]
def s3(i, n):
    t = i / FPS; fr = Image.new('RGBA', (W, H), (255, 214, 64, 255)); d = ImageDraw.Draw(fr)
    d.polygon([(0, 0), (W, 0), (W, 380), (0, 470)], fill=(45, 25, 85))
    place(fr, q, CX, 120, t)
    for j, (im, lab, x) in enumerate(((A, la, 22), (B, lb, 326))):
        k = ease_pop(t - .15 - .15 * j, .25)
        if k > 0:
            c = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))))
            shadowed(fr, c, x + (im.width - c.width) // 2, 400 + (im.height - c.height) // 2)
        place(fr, lab, x + im.width // 2, 400 + max(A.height, B.height) + 12, t - .35 - .15 * j)
    place(fr, cm, CX, 860, t - .6)
    if t >= 1.0:
        k = min(2, int((t - 1.0) / .66)); place(fr, nums[k], CX, 920, (t - 1.0) - k * .66, .15)
    return fr
t = kit.t0(2); kit.add(3.0, s3)
kit.sfx_at(t, 'arcade/swipe.mp3', .6); kit.sfx_at(t + .15, 'arcade/select.mp3', .6); kit.sfx_at(t + .3, 'arcade/select.mp3', .6)
for j in range(3): kit.sfx_at(t + 1.0 + .66 * j, 'arcade/progress-step.mp3', .8)

# 4 · A) 50 €: huyeron (1,8 s)
P2 = panel(p17, (488, 250, 862, 545), 560)
r1 = kit.text([('A) 50 €:', ROSA), ('¡huyeron todos!', BLANCO)], 90)
d4 = escena(P2, None, 420, .10)
def s4(i, n):
    fr = d4(i, n); place(fr, r1, CX, 120, i / FPS); return fr
t = kit.t0(3); kit.add(1.8, s4); kit.sfx_at(t, 'arcade/swipe.mp3', .6); kit.sfx_at(t + .1, 'arcade/error.mp3', .7)

# 5 · B) 0,10 €: cola de 47 (1,6 s)
d5, h5 = pan(p17, (85, 585, 862, 870), 520, 400)
r2 = kit.text([('B) 0,10 €:', AZUL), ('¡cola de 47 clientes!', BLANCO)], 84)
def s5(i, n):
    fr = d5(i, n); place(fr, r2, CX, 140, i / FPS); return fr
t = kit.t0(4); kit.add(1.6, s5); kit.sfx_at(t, 'arcade/swipe.mp3', .6); kit.sfx_at(t + .1, 'arcade/purchase.mp3', .6); kit.sfx_at(t + .6, 'bip', .5)

# 6 · …y perdieron 3,40 € (1,8 s)
d6, h6 = pan(p17, (85, 872, 862, 1128), 500, 380)
r3 = kit.text([('…¡y PERDIERON', BLANCO), ('3,40 €!', NARANJA)], 96)
r4 = kit.pill('Los dos, un desastre', 40, OSCURO)
def s6(i, n):
    t = i / FPS; fr = d6(i, n); place(fr, r3, CX, 120, t); place(fr, r4, CX, 380 + h6 + 40, t - .5); return fr
t = kit.t0(5); kit.add(1.8, s6); kit.sfx_at(t, 'arcade/swipe.mp3', .6); kit.sfx_at(t + .1, 'arcade/error.mp3', .8); kit.sfx_at(t + .5, 'bip', .5)

# 7 · Precio justo (Sr. Tornillo, p.18) (2,4 s)
d7, h7 = pan(p18, (70, 300, 850, 555), 500, 300, blur=False, bgcol=(30, 90, 70))
j1 = kit.text([('El precio justo:', AMARILLO)], 84)
j2 = kit.text([('cubre lo que gastas', BLANCO), ('+ paga tu tiempo', BLANCO), ('+ el cliente, contento', BLANCO)], 66, maxw=590)
def s7(i, n):
    t = i / FPS; fr = d7(i, n); place(fr, j1, CX, 140, t); place(fr, j2, CX, 300 + h7 + 30, t - .3); return fr
t = kit.t0(6); kit.add(2.4, s7); kit.sfx_at(t, 'arcade/swipe.mp3', .6); kit.sfx_at(t + .3, 'arcade/unlock.mp3', .6)

# 8 · Solución: 2 € (p.18) (1,8 s)
d8, h8 = pan(p18, (120, 565, 850, 830), 520, 360, rev=True)
k1 = kit.text([('Solución: ¡2 €!', AMARILLO)], 100)
k2 = kit.pill('¿Tu hijo o hija lo habría acertado?', 30, ROSA)
def s8(i, n):
    t = i / FPS; fr = d8(i, n); place(fr, k1, CX, 150, t); place(fr, k2, CX, 360 + h8 + 40, t - .3); return fr
t = kit.t0(7); kit.add(1.8, s8); kit.sfx_at(t, 'arcade/swipe.mp3', .6); kit.sfx_at(t + .1, 'arcade/success.mp3', .8)

cierre(kit, variante=1, color=(150, 95, 235)); kit.render(OUT)
