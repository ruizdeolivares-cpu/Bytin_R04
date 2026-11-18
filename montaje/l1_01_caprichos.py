#!/usr/bin/env python3
"""L1-01 · Libro 1 «Mi primer dinero» · Misión 4 «Por dónde se escapa el dinero» (páginas impresas 13-16 = archivos pag_017-020).
SOLO viñetas reales. Sin clips de IA. Cierre variante 0 con la portada del libro 1.
Uso: l1_01_caprichos.py <build> <salida.mp4>"""
import sys, os
from PIL import Image, ImageDraw, ImageFilter
from lib import *
kit = Kit(sys.argv[1]); OUT = sys.argv[2]
PG = os.path.join(REPO, 'libro1', 'paginas')
pg = {n: Image.open(os.path.join(PG, f'pag_{n:03d}.jpg')).convert('RGB') for n in (17, 18, 19, 20)}
PORTADA1 = os.path.join(REPO, 'libro1', 'portada_frontal.png')

def vineta(n, box, w=None, y=380, zmax=None, bgcol=None, h=560, rev=False):
    """Viñeta grande (alto h) con barrido horizontal dentro de la zona segura y leve zoom."""
    c = pg[n].crop(box); ww = int(c.width * h / c.height); pn = c.resize((ww, h), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
    bg = fill_bg(c, 28, .5) if bgcol is None else Image.new('RGB', (W, H), bgcol)
    def draw(i, n_):
        fr = bg.copy().convert('RGBA'); k = i / max(1, n_ - 1); k = k * k * (3 - 2 * k)
        if rev: k = 1 - k
        x = int(16 + (620 - 16 - ww) * k); fr.paste(pn, (x, y)); return fr
    return draw, h

def escena(n, box, textos, dur, sfx, y=380, w=None, bgcol=None, extra=None, rev=False, h=560):
    d, h = vineta(n, box, y=y, bgcol=bgcol, rev=rev, h=h)
    def fn(i, n_):
        t = i / FPS; fr = d(i, n_)
        for ov, yy, dt in textos: place(fr, ov, CX, yy if yy >= 0 else y + h + 25, t - dt)
        if extra: extra(fr, t)
        return fr
    t0 = kit.t0(len(kit.segments)); kit.add(dur, fn)
    for dt, s, v in sfx: kit.sfx_at(t0 + dt, s, v)

# 1 · Gancho (2,0 s): la bebida de 2 €
escena(17, (85, 181, 829, 506), [(kit.text([('¿En qué se le va', BLANCO), ('el dinero a tu peque?', AMARILLO)], 84), 110, 0)], 2.0,
       [(0, 'arcade/swipe.mp3', .6), (.15, 'arcade/purchase.mp3', .6)])  # gancho
# 2 · «GASTO PEQUEÑO DETECTADO» (1,8 s)
escena(17, (85, 514, 829, 792), [(kit.pill('Bebida: 2 €', 44, NARANJA), 150, 0), (kit.pill('Total: 2 €', 40, OSCURO), -1, .3)], 1.8,
       [(0, 'arcade/swipe.mp3', .5), (.1, 'bip', .6)])
# 3 · Trayecto corto (1,6 s)
escena(17, (85, 801, 829, 1123), [(kit.pill('+ Trayecto: 2 €', 44, NARANJA), 150, 0), (kit.pill('Total: 4 €', 40, OSCURO), -1, .3)], 1.6,
       [(0, 'arcade/swipe.mp3', .5), (.2, 'arcade/coupon.mp3', .6)])
# 4 · Juego de puntería (1,6 s)
escena(18, (64, 60, 877, 409), [(kit.pill('+ Una partida: 2 €', 44, NARANJA), 150, 0), (kit.pill('Total: 6 €', 40, OSCURO), -1, .3)], 1.6,
       [(0, 'arcade/swipe.mp3', .5), (.2, 'arcade/coupon.mp3', .6)])
# 5 · «6 € parecen poco… hasta que recuerdas que voy camino de 280» (2,2 s)
escena(18, (64, 738, 877, 1123), [(kit.text([('«6 € parecen poco…»', BLANCO)], 80), 150, 0),
                                  (kit.text([('…hasta que recuerdas', BLANCO), ('que voy camino de 280»', AMARILLO)], 64), -1, .6)], 2.2,
       [(0, 'arcade/swipe.mp3', .5), (.6, 'arcade/typing.mp3', .5)], y=330, h=480)
# 6 · La simulación de R-04 (2,4 s): 2 € × 5 días = 10 €
escena(19, (69, 433, 845, 740), [(kit.text([('Una bebida de 2 €', BLANCO), ('cinco días…', BLANCO)], 78), 110, 0),
                                 (kit.text([('¡10 € solo', AMARILLO), ('en bebidas!', AMARILLO)], 84), -1, .9)], 2.4,
       [(0, 'arcade/swipe.mp3', .5), (.1, 'bip', .6)] + [(.25 + .12 * k, 'arcade/progress-step.mp3', .6) for k in range(5)] + [(.9, 'arcade/error.mp3', .7)], y=330, h=480)
# 7 · Lo que aprende Bityn (2,2 s)
escena(19, (69, 750, 845, 1125), [(kit.text([('No se trata de', BLANCO), ('prohibírselo todo…', BLANCO)], 78), 110, 0),
                                  (kit.text([('…sino de elegir', AMARILLO), ('en qué gastar', AMARILLO)], 78), -1, .5)], 2.2,
       [(0, 'arcade/swipe.mp3', .5), (.5, 'arcade/unlock.mp3', .6)], y=330, h=480)
# 8 · Pregunta (1,6 s)
escena(20, (64, 63, 877, 409), [(kit.text([('¿Tu hijo o hija', BLANCO), ('lleva la cuenta?', AMARILLO)], 92), 110, 0),
                                (kit.pill('Comenta su edad', 40, ROSA), -1, .3)], 1.6,
       [(0, 'arcade/swipe.mp3', .5), (.2, 'bip', .6)])
cierre(kit, variante=0, portada=PORTADA1); kit.render(OUT)
