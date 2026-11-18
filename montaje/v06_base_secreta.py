#!/usr/bin/env python3
"""V06 · Descargables y base secreta. Material real: QR secreto (p.94, difuminado), web «La base secreta de R-04» (index.html,
capturas de móvil) y los 4 PDF descargables del repo. Clip: G3c (R-04 sorpresa). Gancho con edad. Cierre variante 2.
Uso: v06_base_secreta.py <build> <carpeta_capturas> <salida.mp4>
Capturas (390x780 @2x, Playwright): web_<vista>.png y full_<vista>.png; PDF a 80 ppp con pdftoppm (<nombre>-N.jpg)."""
import sys, os, glob
from PIL import Image, ImageDraw, ImageFilter
from lib import *
kit = Kit(sys.argv[1]); SH = sys.argv[2]; OUT = sys.argv[3]
NAVY = (22, 20, 58)

def estrellas(seed=1, col=NAVY):
    import random; r = random.Random(seed); bg = Image.new('RGB', (W, H), col); d = ImageDraw.Draw(bg)
    for _ in range(140):
        x, y, s = r.randint(0, W), r.randint(0, H), r.choice((1, 1, 2, 3)); d.ellipse((x, y, x + s, y + s), fill=(255, 255, 255 - r.randint(0, 80)))
    return bg

def movil(shot, w=400, h=760, scroll=0.0):
    """Captura dentro de un marco de móvil. scroll = 0..1 recorre la captura de página completa."""
    im = Image.open(shot).convert('RGB'); k = w / im.width; im = im.resize((w, int(im.height * k)), Image.LANCZOS)
    y0 = int(max(0, im.height - h) * scroll); scr = im.crop((0, y0, w, y0 + h))
    fr = Image.new('RGBA', (w + 28, h + 28), (0, 0, 0, 0)); d = ImageDraw.Draw(fr)
    d.rounded_rectangle((0, 0, w + 27, h + 27), radius=46, fill=(15, 15, 22), outline=(90, 90, 110), width=3)
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=34, fill=255)
    fr.paste(scr, (14, 14), m); return fr

def con_sombra(fr, ov, x, y):
    sh = Image.new('RGBA', ov.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 120), mask=ov.split()[3])
    fr.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)), (x + 6, y + 10)); fr.alpha_composite(ov, (x, y))

# 1 · Gancho (1,8 s): R-04 sorprendido + QR secreto
f1 = clip_frames('G3c_r04_sorpresa.mp4', 0.2, 1.8)
g1 = kit.text([('Este libro esconde', BLANCO), ('un QR secreto', AMARILLO)], 92)
g2 = kit.pill('Para niños de 8 a 12 años', 38, NARANJA)
def s1(i, n):
    t = i / FPS; fr = zoom(f1[i], 1.05 + .08 * i / n, .5, .55).convert('RGBA')
    place(fr, g1, CX, 110, t); place(fr, g2, CX, 940, t - .3); return fr
kit.add(1.8, s1); kit.sfx_at(0, 'arcade/unlock.mp3', .7); kit.sfx_at(.2, 'bip', .6)

# 2 · El QR de la p.94 (difuminado: es para quien tiene el libro) (2,0 s)
p94 = Image.open(os.path.join(REPO, 'libro', 'paginas', 'pag_94.jpg')).convert('RGB')
qa = p94.crop((35, 750, 890, 1160)); qx = (375 - 35, 945 - 750, 550 - 35, 1117 - 750)
q = qa.copy(); q.paste(q.crop(qx).filter(ImageFilter.GaussianBlur(9)), qx[:2])
q = q.resize((600, int(q.height * 600 / q.width)), Image.LANCZOS)
c1 = kit.text([('Al final del libro…', BLANCO)], 80); c2 = kit.text([('solo para quien abre', BLANCO), ('la caja fuerte de X', AMARILLO)], 74)
bg2 = estrellas(2)
def s2(i, n):
    t = i / FPS; fr = bg2.copy().convert('RGBA'); z = 1 + .07 * i / n
    im = q.resize((int(q.width * z), int(q.height * z)), Image.LANCZOS); shadowed(fr, im, CX - im.width // 2, 420 - (im.height - q.height) // 2)
    place(fr, c1, CX, 150, t); place(fr, c2, CX, 420 + q.height + 50, t - .5); return fr
t = kit.t0(1); kit.add(2.0, s2); kit.sfx_at(t, 'arcade/swipe.mp3', .6); kit.sfx_at(t + .5, 'arcade/lock.mp3', .7)

# 3-5 · La base secreta en el móvil
def escena_movil(shot, titulo, sub, dur, col, scroll=(0, 0), sfx='arcade/swipe.mp3'):
    bg = estrellas(len(shot), col)
    def fn(i, n):
        t = i / FPS; k = i / max(1, n - 1); fr = bg.copy().convert('RGBA')
        m = movil(shot, scroll=scroll[0] + (scroll[1] - scroll[0]) * k * k * (3 - 2 * k))
        kk = ease_pop(t, .28); mm = m if kk >= 1 else m.resize((max(1, int(m.width * kk)), max(1, int(m.height * kk))))
        con_sombra(fr, mm, CX - mm.width // 2, 300 + (m.height - mm.height) // 2)
        place(fr, titulo, CX, 90, t - .05)
        if sub: place(fr, sub, CX, 930, t - .35)
        return fr
    t = kit.t0(len(kit.segments)); kit.add(dur, fn); kit.sfx_at(t, sfx, .6); kit.sfx_at(t + .1, 'arcade/open.mp3', .5)
    return t

escena_movil(os.path.join(SH, 'full_inicio.png'), kit.text([('…la base secreta', BLANCO), ('de R-04', AMARILLO)], 84), None, 2.0, (40, 25, 90), (0, .35))
t = escena_movil(os.path.join(SH, 'full_jugar.png'), kit.text([('Un juego: vender', BLANCO), ('más que MegaSnack', AMARILLO)], 80), None, 2.0, (25, 60, 110), (0, .3))
kit.sfx_at(t + .8, 'arcade/purchase.mp3', .6)
t = escena_movil(os.path.join(SH, 'web_diploma.png'), kit.text([('Cromos, misión secreta', BLANCO), ('y diploma con su nombre', AMARILLO)], 70), None, 2.0, (80, 30, 100))
kit.sfx_at(t + .6, 'arcade/achievement.mp3', .5)

# 6 · Descargables (2,6 s): las portadas de los 4 PDF entran en abanico
pdfs = [('material-recortable-01', 'Recortables'), ('cuaderno-de-cuentas-30-dias-1', 'Cuaderno de cuentas'),
        ('carteles-para-colorear-1', 'Para colorear'), ('sucesos-galacticos-locos-1', 'Cartas extra')]
cards = []
for name, lab in pdfs:
    im = Image.open(os.path.join(SH, name + '.jpg')).convert('RGB'); im = im.resize((250, int(im.height * 250 / im.width)), Image.LANCZOS)
    cards.append((im, kit.pill(lab, 28, OSCURO)))
d1 = kit.text([('Y descargables', BLANCO), ('para imprimir', AMARILLO)], 90)
bg6 = Image.new('RGB', (W, H), (255, 214, 64)); ImageDraw.Draw(bg6).polygon([(0, 0), (W, 0), (W, 300), (0, 360)], fill=NAVY)
pos = [(40, 380), (330, 380), (40, 720), (330, 720)]
def s6(i, n):
    t = i / FPS; fr = bg6.copy().convert('RGBA'); place(fr, d1, CX, 90, t)
    for j, ((im, lab), (x, y)) in enumerate(zip(cards, pos)):
        k = ease_pop(t - .25 - .22 * j, .25)
        if k > 0:
            c = im.crop((0, 0, im.width, 300)).resize((max(1, int(im.width * k)), max(1, int(300 * k))))
            shadowed(fr, c, x + (im.width - c.width) // 2, y + (300 - c.height) // 2)
            place(fr, lab, x + im.width // 2, y + 300 - 20, t - .4 - .22 * j)
    return fr
t = kit.t0(len(kit.segments)); kit.add(2.6, s6); kit.sfx_at(t, 'arcade/swipe.mp3', .6)
for j in range(4): kit.sfx_at(t + .25 + .22 * j, 'arcade/drop.mp3', .6)

# 7 · La puerta secreta (2,0 s): pide la contraseña de 6 letras (NO se revela)
t = escena_movil(os.path.join(SH, 'full_puerta.png'), kit.text([('¿La contraseña?', BLANCO), ('Está en el libro', AMARILLO)], 86),
                 kit.pill('¿Tu peque la sacaría?', 38, ROSA), 2.0, (40, 25, 90), (0, .25))
kit.sfx_at(t + .5, 'arcade/progress-step.mp3', .7); kit.sfx_at(t + .8, 'arcade/progress-step.mp3', .7)

cierre(kit, variante=2); kit.render(OUT)
