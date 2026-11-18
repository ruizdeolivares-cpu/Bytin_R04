#!/usr/bin/env python3
"""L1-02 · Libro 1 «Mi primer dinero» · Misión 9 «Cuando el plan se tuerce» (págs. impresas 33-36 = archivos pag_037-040).
Viñetas reales + clip GK6 (Grok, «CARIÑO DETECTADO», pág. 36). Se resuelve en el propio vídeo. Cierre 1 con portada del libro 1.
Uso: l1_02_carino.py <build> <salida.mp4>"""
import sys, os, subprocess
from PIL import Image, ImageFilter
from lib import *
kit = Kit(sys.argv[1]); OUT = sys.argv[2]
PG = os.path.join(REPO, 'libro1', 'paginas')
pg = {n: Image.open(os.path.join(PG, f'pag_{n:03d}.jpg')).convert('RGB') for n in (37, 38, 40)}
PORTADA1 = os.path.join(REPO, 'libro1', 'portada_frontal.png')

def vineta(n, box, y=380, h=560, rev=False):
    c = pg[n].crop(box); ww = int(c.width * h / c.height); pn = c.resize((ww, h), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
    bg = fill_bg(c, 28, .5)
    def draw(i, n_):
        fr = bg.copy().convert('RGBA'); k = i / max(1, n_ - 1); k = k * k * (3 - 2 * k)
        if rev: k = 1 - k
        fr.paste(pn, (int(16 + (620 - 16 - ww) * k), y)); return fr
    return draw

def escena(n, box, textos, dur, sfx, y=380, h=560, rev=False):
    d = vineta(n, box, y, h, rev)
    def fn(i, n_):
        t = i / FPS; fr = d(i, n_)
        for ov, yy, dt in textos: place(fr, ov, CX, yy if yy >= 0 else y + h + 25, t - dt)
        return fr
    t0 = kit.t0(len(kit.segments)); kit.add(dur, fn)
    for dt, s, v in sfx: kit.sfx_at(t0 + dt, s, v)

# 1 · Gancho (2,0 s): R-04 flota raro en pleno festival (pág. 33)
escena(37, (64, 191, 853, 490), [(kit.text([('Ahorraba para su sueño…', BLANCO), ('y su amigo se averió', AMARILLO)], 80), 110, 0)], 2.0,
       [(0, 'arcade/swipe.mp3', .6), (.1, 'bip', .7), (.4, 'arcade/error.mp3', .6)], rev=True)
# 2 · La reparación cuesta 10 € (1,8 s) (pág. 33)
escena(37, (64, 821, 853, 1123), [(kit.pill('Reparación: 10 €', 46, NARANJA), 150, 0), (kit.pill('Le faltan 120 € para su meta', 34, OSCURO), -1, .3)], 1.8,
       [(0, 'arcade/swipe.mp3', .5), (.2, 'arcade/coupon.mp3', .6)])
# 3 · El dilema (2,2 s) (pág. 34)
escena(38, (72, 56, 870, 404), [(kit.text([('¿Qué harías tú?', BLANCO)], 92), 130, 0),
                               (kit.text([('¿Guardar los 10 €…', BLANCO), ('o arreglar a R-04?', AMARILLO)], 72), -1, .4)], 2.2,
       [(0, 'arcade/swipe.mp3', .5), (.4, 'arcade/progress-step.mp3', .6), (.8, 'arcade/progress-step.mp3', .6)], y=330, h=480)

# 4 · Clip GK6 a pantalla completa (6,6 s): la respuesta de Bityn y «CARIÑO DETECTADO» (pág. 36)
GK = os.path.join(CLIPS, 'GK6_carino_original.mp4'); A, D = 1.0, 6.6
GW, GH = 612, 1126  # clip a 612 px de ancho: R-04 queda dentro de la zona segura (x≤620)
raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(A), '-i', GK, '-t', str(D + .2), '-vf', f'fps={FPS},scale={GW}:{GH}:flags=lanczos',
                      '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
g = [Image.frombuffer('RGB', (GW, GH), raw[i*GW*GH*3:(i+1)*GW*GH*3]) for i in range(len(raw)//(GW*GH*3))]
GBG = fill_bg(g[0], 30, .35)
g += [g[-1]] * max(0, int(D * FPS) - len(g))
TMP = OUT + '.gk.wav'; subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(A), '-t', str(D), '-i', GK, '-vn', '-ac', '2', '-ar', '44100', TMP], check=True)
s1 = kit.text([('«Prefiero tenerte', BLANCO), ('funcionando que', BLANCO), ('10 € más sin ti»', AMARILLO)], 76)
s2 = kit.text([('CARIÑO DETECTADO.', NARANJA), ('NO SÉ DÓNDE', BLANCO), ('GUARDARLO.', BLANCO)], 76)
def s4(i, n):
    t = i / FPS; fr = GBG.copy().convert('RGBA'); fr.paste(g[i], (8, 154))
    if t < 3.6: place(fr, s1, CX, 120, t - .1)
    else: place(fr, s2, CX, 120, t - 3.6)
    return fr
t = kit.t0(3); kit.add(D, s4); kit.sfx_at(t, os.path.abspath(TMP), 2.2); kit.sfx_at(t, 'arcade/swipe.mp3', .4)

# 5 · La lección (2,0 s): reserva para imprevistos (pág. 36)
escena(38, (72, 418, 870, 742), [(kit.text([('Los imprevistos existen:', BLANCO), ('guarda siempre una reserva', AMARILLO)], 70), 120, 0),
                                (kit.pill('¿Tu hijo o hija tiene la suya?', 34, ROSA), -1, .4)], 2.0,
       [(0, 'arcade/swipe.mp3', .5), (.3, 'arcade/unlock.mp3', .6)], y=360, h=500)
cierre(kit, variante=1, color=(255, 170, 60), portada=PORTADA1); kit.render(OUT); os.remove(TMP)
