#!/usr/bin/env python3
"""L1-03b · Versión CORTA (15 s) de la carta a los Reyes: cifra en el 1.er segundo, sin pantallas quietas. Premium: clips de Grok (GK9 saludo, GK11 escaneo, voz GK10),
viñetas reales (pág. 2: vehículo 280 €, «¡Es mucho! Pero no es imposible. Solo necesito un plan.») y la página real
«Mis metas de ahorro» (pág. 96) rellenándose. Cierre 0 con portada del libro 1 (el 2 dice «enlace en el perfil» y la bio es del libro 2).
Uso: l1_03_carta_reyes.py <build> <salida.mp4>"""
import sys, os, subprocess, math
from PIL import Image, ImageDraw, ImageFilter
from lib import *
kit = Kit(sys.argv[1]); OUT = sys.argv[2]
PG = os.path.join(REPO, 'libro1', 'paginas'); PORTADA1 = os.path.join(REPO, 'libro1', 'portada_frontal.png')
TMPS = []

def frames(name, start, dur, w=W, h=None):
    """Fotogramas de un clip escalados a ancho w (alto proporcional)."""
    p = os.path.join(CLIPS, name)
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(start), '-i', p, '-t', str(dur + .2), '-vf', f'fps={FPS},scale={w}:-2:flags=lanczos',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    hh = int(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', p],
                            capture_output=True, text=True).stdout.split(',')[1].split()[0])
    ww0 = int(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width', '-of', 'csv=p=0', p],
                             capture_output=True, text=True).stdout.split()[0])
    hgt = int(round(hh * w / ww0 / 2) * 2); n = len(raw) // (w * hgt * 3)
    fr = [Image.frombuffer('RGB', (w, hgt), raw[i*w*hgt*3:(i+1)*w*hgt*3]) for i in range(n)]
    need = int(round(dur * FPS)); fr += [fr[-1]] * max(0, need - len(fr)); return fr[:need]

def audio(name, start, dur):
    t = os.path.abspath(OUT + f'.{len(TMPS)}.wav'); TMPS.append(t)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(start), '-t', str(dur), '-i', os.path.join(CLIPS, name), '-vn', '-ac', '2', '-ar', '44100', t], check=True)
    return t

def full(fr, i, cy=.45):
    """Fotograma de clip a pantalla completa (recorte vertical centrado)."""
    f = fr[min(i, len(fr) - 1)]
    if f.height < H: f = f.resize((int(f.width * H / f.height), H), Image.LANCZOS)
    x0 = (f.width - W) // 2; y0 = int((f.height - H) * cy)
    return f.crop((x0, y0, x0 + W, y0 + H)).convert('RGBA')

# 1 · Gancho (3,2 s): R-04 escanea y la cifra sale YA
g11 = frames('GK11_r04_escanea_original.mp4', 0, 3.2)
a11 = audio('GK11_r04_escanea_original.mp4', 0, 3.2)
regalos_tot = 781
h1 = kit.text([('Tu peque pide a', BLANCO), ('los Reyes…', AMARILLO)], 84)
def s1(i, n):
    t = i / FPS; fr = full(g11, i, .35); place(fr, h1, CX, 130, t)
    v = int(regalos_tot * min(1, t / 1.2)); ov = kit.text([(f'{v} €', (255, 90, 90) if t > 1.2 else BLANCO)], 150)
    fr.alpha_composite(ov, (CX - ov.width // 2, 800))
    if t > 1.5: place(fr, kit.pill('R-04: TOTAL DEMASIADO', 40, (200, 40, 50)), CX, 990, t - 1.5)
    return fr
kit.add(3.2, s1); kit.sfx_at(0, a11, 2.0); kit.sfx_at(0, 'arcade/scanning.mp3', .5); kit.sfx_at(1.2, 'arcade/error.mp3', .7)

p6 = Image.open(os.path.join(PG, 'pag_006.jpg')).convert('RGB')
def pan_panel(box, h=560, y=380, rev=False):
    c = p6.crop(box); ww = int(c.width * h / c.height); pn = c.resize((ww, h), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
    bg = fill_bg(c, 28, .5)
    def draw(i, n):
        fr = bg.copy().convert('RGBA'); k = i / max(1, n - 1); k = k * k * (3 - 2 * k)
        if rev: k = 1 - k
        fr.paste(pn, (int(16 + (620 - 16 - ww) * k), y)); return fr
    return draw
# 2 · Bityn (4,0 s): «¡Es mucho! Pero no es imposible. Solo necesito un plan.» (pág. 2) + su voz
a10 = audio('GK10_bityn_plan_original.mp4', 0, 4.0)
d5 = pan_panel((64, 467, 878, 772))
t5 = kit.text([('Bityn quería 280 €', BLANCO), ('y tenía 50…', AMARILLO)], 80)
t5b = kit.text([('«Solo necesito', BLANCO), ('un plan»', AMARILLO)], 80)
def s2(i, n):
    t = i / FPS; fr = d5(i, n)
    place(fr, t5 if t < 1.8 else t5b, CX, 120, t if t < 1.8 else t - 1.8)
    place(fr, kit.pill('280 € − 50 € = 230 €', 46, VERDE), CX, 380 + 560 + 25, t - 1.0); return fr
t = kit.t0(1); kit.add(4.0, s2); kit.sfx_at(t, a10, 2.0); kit.sfx_at(t, 'arcade/swipe.mp3', .5)

# 6 · El truco: «Mis metas de ahorro» (pág. 96) en grande, rellenándose
fL = kit.font(46); fV = kit.font(66)
def meta(t):
    im = Image.new('RGBA', (600, 720), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, 599, 719), radius=30, fill=(255, 248, 225), outline=(240, 150, 40), width=8)
    d.text((30, 26), 'Mis metas de ahorro', font=fL, fill=(40, 30, 70))
    filas = [('Quiero:', 'el vehículo', (30, 90, 200), .4), ('Cuesta:', '280 €', (30, 90, 200), .9), ('Tengo:', '50 €', (30, 90, 200), 1.4), ('Me faltan:', '230 €', (210, 40, 40), 1.9)]
    for j, (lab, val, col, t0) in enumerate(filas):
        y = 110 + j * 105; d.text((30, y + 14), lab, font=fL, fill=(90, 80, 110)); d.line((250, y + 82, 570, y + 82), fill=(210, 190, 160), width=3)
        if t > t0: d.text((255, y), val, font=fV, fill=col)
    k = int(max(0, (t - 2.5) / .12))
    for c in range(10):
        x = 50 + c * 54; y = 590; on = c < min(k, 6)
        d.ellipse((x - 22, y - 22, x + 22, y + 22), fill=(255, 196, 40) if on else (255, 248, 225), outline=(200, 150, 40), width=4)
    return im
h6 = kit.text([('El truco del libro:', BLANCO), ('una meta con su número', NARANJA)], 74)
p6b = kit.pill('Página «Mis metas de ahorro» del libro', 30, OSCURO)
def s6(i, n):
    t = i / FPS; fr = Image.new('RGBA', (W, H), (255, 214, 64, 255)); im = meta(t)
    shadowed(fr, im, CX - 300, 300); place(fr, h6, CX, 110, t); place(fr, p6b, CX, 300 + 720 + 25, t - 2.6); return fr
t = kit.t0(2); kit.add(3.8, s6)
for dt in (.4, .9, 1.4, 1.9): kit.sfx_at(t + dt, 'arcade/typing.mp3', .5)
for k in range(6): kit.sfx_at(t + 2.5 + .12 * k, 'arcade/coupon.mp3', .35)

# 4 · Final (2,2 s)
g9 = frames('GK9_saluda_festival_original.mp4', 0, 6.0)
h7 = kit.text([('Este año, carta', BLANCO), ('con plan', AMARILLO)], 92)
def s7(i, n):
    t = i / FPS; fr = full(g9, 60 + i); place(fr, h7, CX, 140, t); place(fr, kit.pill('¿Cuánto pide tu peque?', 40, ROSA), CX, 930, t - .3); return fr
t = kit.t0(3); kit.add(2.2, s7); kit.sfx_at(t, 'arcade/swipe.mp3', .5); kit.sfx_at(t + .3, 'arcade/reward.mp3', .5)

cierre(kit, variante=0, portada=PORTADA1); kit.render(OUT)
for f in TMPS: os.remove(f)
