#!/usr/bin/env python3
"""«Cuando Dios creó la Navidad» · montaje estilo fábula (palabra a palabra, medallas, destellos).
Uso: python3 dios_navidad_build.py CLIPS_DIR FONT.woff PORTADA.png SALIDA.mp4
CLIPS_DIR contiene c1.mp4 … c8.mp4 (orden del guion)."""
import sys, os, re, math, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

CL, FONT, PORTADA, OUT = sys.argv[1:5]
from scipy import ndimage
W, H, FPS = 720, 1280, 30
TMP = os.path.join(os.path.dirname(OUT), 'dios_tmp'); os.makedirs(TMP, exist_ok=True)
SR = 44100

# ---------- guion: segmentos de voz medidos (s) y texto ----------
SEGS = {
 1: [(0.04, 2.21, 'HOOK'), (2.93, 5.37, 'le dio a cada uno su *tarea*')],
 2: [(0.58, 0.93, '*Pavo*'), (1.37, 3.13, 'serás la cena de *Nochebuena*'), (3.52, 3.88, '¿Yo?'),
     (4.22, 4.86, '¡Ni *hablar!*'), (5.15, 6.38, 'Que pidan *langostinos*')],
 3: [(0.00, 0.54, 'Siguiente'), (1.03, 1.67, '*Presentador*'), (2.00, 4.55, 'pelarás las *uvas* de toda España'),
     (4.77, 7.87, '*Demasiado* Yo solo cuento hasta doce… y me lío con los *cuartos*')],
 4: [(0.10, 0.64, 'Siguiente'), (1.05, 1.40, '*Reyes*'), (1.84, 3.49, 'esconderéis los *regalos* por la casa'),
     (3.88, 4.89, '*Demasiado*'), (5.21, 7.29, 'Nosotros saludamos en la *cabalgata*')],
 5: [(0.10, 0.60, '*Abuela*'), (0.92, 2.16, 'tú solo pondrás la mesa'), (3.31, 4.00, '¿Solo eso?'),
     (4.42, 6.63, 'Dame también lo que no han querido *esos*'), (7.49, 8.12, '*Concedido*')],
 6: [(0.09, 1.89, 'Por eso la abuela cocina el *pavo*'), (2.48, 3.83, 'pela las *uvas* de todos')],
 7: [(0.11, 2.45, 'y esconde los *regalos* de Reyes por el salón'), (2.90, 4.33, 'Y cuando por fin se sienta…'),
     (4.67, 6.14, 'le preguntan qué hay de *postre*')],
 9: [(0.09, 0.57, '¿Postre?'), (1.34, 2.45, 'Hoy, de postre…'), (3.06, 4.00, '*pasatiempos*'),
     (4.73, 6.14, 'Y el que pierda, *friega*')],
}
# piezas: (clip, audio_ini, audio_fin, desfase_video, zoom_base, destello)
PIECES = [
 (1, 0.00, 2.35, 0, 1.00, False), (1, 2.80, 5.50, 0, 1.08, False),
 (2, 0.45, 3.25, 0, 1.00, True), (2, 3.42, 6.60, 0, 1.09, False),
 (4, 0.05, 1.50, 0, 1.00, True), (4, 1.75, 5.05, 0, 1.06, False), (4, 5.12, 7.50, 0, 1.10, False),
 (5, 0.05, 2.30, 0, 1.00, True), (5, 3.15, 6.75, 0, 1.07, False), (5, 7.35, 8.40, 0, 1.12, False),
 (6, 0.00, 4.10, 0, 1.00, True),
 (7, 0.05, 2.60, 0, 1.00, True), (7, 2.75, 6.35, 3.55, 1.06, False),
 (9, 0.00, 7.70, 0, 1.00, False),
]
END_DUR = 1.9

# ---------- utilidades ----------
def syl(w):
    return max(1, len(re.findall(r'[aeiouáéíóúü]+', w.lower())))

def words_timed():
    """Devuelve lista (clip, t_ini, t_fin, palabra, clave)."""
    out = []
    for c, segs in SEGS.items():
        for a, b, txt in segs:
            if txt == 'HOOK':
                continue
            toks = txt.split()
            ws = [syl(t) + 0.6 for t in toks]
            tot = sum(ws); t = a
            for tok, wgt in zip(toks, ws):
                d = (b - a) * wgt / tot
                key = tok.startswith('*')
                out.append([c, t, t + d, tok.strip('*'), key])
                t += d
    # cada palabra se queda hasta la siguiente si el hueco es corto
    for i in range(len(out) - 1):
        if out[i + 1][0] == out[i][0] and out[i + 1][1] - out[i][2] < 0.35:
            out[i][2] = out[i + 1][1]
        else:
            out[i][2] += 0.15
    return out

# mapa tiempo fuente (clip, t) -> tiempo de salida
piece_out = []
acc = 0.0
for p in PIECES:
    piece_out.append(acc); acc += p[2] - p[1]
MAIN_DUR = acc
TOTAL = MAIN_DUR + END_DUR

def src2out(c, t):
    for (pc, a, b, *_), o in zip(PIECES, piece_out):
        if pc == c and a - 0.05 <= t <= b + 0.05:
            return o + min(max(t, a), b) - a
    return None

WORDS = []
for c, a, b, wd, k in words_timed():
    oa, ob = src2out(c, a), src2out(c, b)
    if oa is None:
        continue
    if ob is None:
        ob = oa + (b - a)
    WORDS.append((oa, ob, wd, k, c))

def wtime(clip, word, nth=0):
    n = 0
    for oa, ob, wd, k, c in WORDS:
        if c == clip and wd.strip('¿?¡!.,…').lower() == word.lower():
            if n == nth:
                return oa
            n += 1
    raise KeyError((clip, word))

# ---------- gráficos ----------
FBIG = lambda s: ImageFont.truetype(FONT, s)
WHITE, ORANGE, DARK = (255, 255, 255), (255, 170, 30), (35, 22, 10)
_cache = {}

def word_img(txt, key):
    k = (txt, key)
    if k in _cache:
        return _cache[k]
    size = 124
    while True:
        f = FBIG(size)
        bb = f.getbbox(txt, stroke_width=9)
        if bb[2] - bb[0] <= 560 or size < 60:
            break
        size -= 6
    im = Image.new('RGBA', (bb[2] - bb[0] + 30, bb[3] - bb[1] + 30), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # sombra
    d.text((15 - bb[0] + 4, 15 - bb[1] + 6), txt, font=f, fill=(0, 0, 0, 120), stroke_width=9, stroke_fill=(0, 0, 0, 120))
    d.text((15 - bb[0], 15 - bb[1]), txt, font=f, fill=ORANGE if key else WHITE, stroke_width=9, stroke_fill=DARK)
    _cache[k] = im
    return im

def halo():
    im = Image.new('L', (W, 420), 0)
    d = ImageDraw.Draw(im)
    d.ellipse((60, 90, 600, 330), fill=135)
    im = im.filter(ImageFilter.GaussianBlur(55))
    out = Image.new('RGBA', im.size, (0, 0, 0, 0)); out.putalpha(im)
    return out
HALO = halo()
CAP_Y = 500   # centro vertical del texto
CAP_X = 340   # centro horizontal (zona segura x<620)

def badge(label, r=78):
    s = r * 2 + 20
    im = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    c = s // 2
    for i in range(16):  # escarapela
        ang = i * math.pi / 8
        x, y = c + math.cos(ang) * (r + 4), c + math.sin(ang) * (r + 4)
        d.ellipse((x - 14, y - 14, x + 14, y + 14), fill=(205, 140, 20))
    for k in range(r, 0, -1):  # degradado dorado
        t = k / r
        col = (int(255 - 40 * t), int(220 - 70 * t), int(90 - 60 * t))
        d.ellipse((c - k, c - k, c + k, c + k), fill=col)
    d.ellipse((c - r + 10, c - r + 10, c + r - 10, c + r - 10), outline=(150, 95, 10), width=5)
    size = 40 if len(label) <= 5 else 30
    f = FBIG(size)
    bb = f.getbbox(label)
    d.text((c - (bb[2] + bb[0]) / 2, c - (bb[3] + bb[1]) / 2), label, font=f, fill=(95, 50, 5))
    return im
BADGE = {k: badge(k) for k in ('CENA', 'UVAS', 'REGALOS')}
BADGE_S = {k: v.resize((v.width * 62 // 100, v.height * 62 // 100), Image.LANCZOS) for k, v in BADGE.items()}

def tick(im):
    im = im.copy(); d = ImageDraw.Draw(im); w = im.width
    d.ellipse((w - 46, w - 46, w - 2, w - 2), fill=(40, 170, 70), outline='white', width=4)
    d.line([(w - 36, w - 24), (w - 27, w - 14), (w - 12, w - 34)], fill='white', width=6)
    return im
BADGE_T = {k: tick(v) for k, v in BADGE_S.items()}

def ease(x):
    x = min(max(x, 0), 1); return 1 - (1 - x) ** 3

def paste_c(base, im, cx, cy, scale=1.0, alpha=1.0, rot=0):
    if scale != 1.0:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    if rot:
        im = im.rotate(rot, resample=Image.BILINEAR, expand=True)
    if alpha < 1.0:
        a = im.getchannel('A').point(lambda v: int(v * alpha)); im = im.copy(); im.putalpha(a)
    base.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))

# ---------- eventos de medallas ----------
T = {}
T['cena_in'] = wtime(2, 'Pavo'); T['cena_out'] = wtime(2, 'Ni')
T['reg_in'] = wtime(4, 'regalos'); T['reg_out'] = wtime(4, 'Demasiado')
T['d1'] = wtime(5, 'Dame'); T['d2'] = wtime(5, 'no'); T['d3'] = wtime(5, 'esos')
T['conc'] = wtime(5, 'Concedido')
T['k1'] = wtime(6, 'pavo'); T['k2'] = wtime(6, 'uvas'); T['k3'] = wtime(7, 'regalos')
T['postre'] = wtime(7, 'postre')
T['pasa'] = wtime(9, 'pasatiempos'); T['friega'] = wtime(9, 'friega')
c5_end = piece_out[10]; c7_end = piece_out[13]

def draw_badges(fr, t):
    # rechazos: aparece junto al personaje y sale volando hacia la mano
    for key, tin, tout, pos in (('CENA', T['cena_in'], T['cena_out'], (520, 840)),
                                ('REGALOS', T['reg_in'], T['reg_out'], (520, 800))):
        if tin <= t < tout + 0.5:
            if t < tout:
                k = ease((t - tin) / 0.25)
                paste_c(fr, BADGE[key], pos[0], pos[1], 0.3 + 0.7 * k + 0.12 * math.sin(min(1, (t - tin) / 0.25) * math.pi))
            else:
                k = ease((t - tout) / 0.5)
                x = pos[0] + (560 - pos[0]) * k; y = pos[1] + (120 - pos[1]) * k
                shake = 14 * math.sin((t - tout) * 60) * (1 - k)
                paste_c(fr, BADGE[key], x + shake, y, 1 - 0.6 * k, 1 - 0.8 * k, rot=40 * k)
    # la abuela se las queda todas
    if T['d1'] - 0.1 <= t < c5_end:
        for key, td, pos in (('CENA', T['d1'], (110, 720)), ('REGALOS', T['d3'], (555, 720))):
            if t >= td:
                k = ease((t - td) / 0.4)
                y = 60 + (pos[1] - 60) * k
                glow = 1 + 0.08 * math.sin((t - td) * 8) if t > T['conc'] else 1
                paste_c(fr, BADGE[key], pos[0], y, (0.45 + 0.3 * k) * glow)
    # lista de tareas de la abuela (c6-c7)
    if T['k1'] - 0.05 <= t < c7_end:
        for i, (key, tk) in enumerate((('CENA', T['k1']), ('UVAS', T['k2']), ('REGALOS', T['k3']))):
            if t >= tk:
                k = ease((t - tk) / 0.3)
                img = BADGE_T[key] if t > tk + 0.35 else BADGE_S[key]
                dx = 6 * math.sin((t - T['postre']) * 50) if T['postre'] <= t < T['postre'] + 0.5 else 0
                paste_c(fr, img, 120 + i * 150 + dx, 190, 0.4 + 0.6 * k + 0.15 * math.sin(min(1, (t - tk) / 0.3) * math.pi))

def draw_caption(fr, t):
    # gancho: frase completa visible desde el fotograma 0
    if t < piece_out[1]:
        lines = [('CUANDO DIOS', False), ('CREÓ LA', False), ('NAVIDAD…', True)]
        paste_c(fr, HALO.resize((W, 600)), CAP_X, CAP_Y)
        for i, (ln, k) in enumerate(lines):
            im = word_img(ln, k)
            paste_c(fr, im, CAP_X, CAP_Y - 130 + i * 125, min(1.0, 560 / im.width) if ln != 'CUANDO DIOS' else 560 / im.width)
        return
    if T['postre'] <= t < c7_end:
        paste_c(fr, HALO, CAP_X, CAP_Y)
        k = ease((t - T['postre']) / 0.2)
        paste_c(fr, word_img('¿POSTRE?', True), CAP_X, CAP_Y, 1.25 - 0.25 * k)
        return
    for oa, ob, wd, key, c in WORDS:
        if oa <= t < ob:
            paste_c(fr, HALO, CAP_X, CAP_Y)
            pop = 1.0 + 0.18 * (1 - ease((t - oa) / 0.12))
            paste_c(fr, word_img(wd, key), CAP_X, CAP_Y, pop)
            return

# ---------- audio ----------
def load_wav(path):
    w = wave.open(path); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    return x.reshape(-1, w.getnchannels()).mean(axis=1)

def sfx_pop():
    t = np.arange(int(SR * 0.12)) / SR
    f = 700 + 900 * t / 0.12
    return 0.5 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 30)

def sfx_whoosh():
    n = int(SR * 0.45); rng = np.random.default_rng(1)
    x = rng.standard_normal(n); env = np.sin(np.pi * np.arange(n) / n) ** 2
    y = np.convolve(x, np.ones(30) / 30, 'same')
    return 0.6 * y * env / np.abs(y).max()

def sfx_ding():
    t = np.arange(int(SR * 1.0)) / SR
    return 0.35 * (np.sin(2 * np.pi * 1568 * t) + 0.6 * np.sin(2 * np.pi * 2349 * t)) * np.exp(-t * 4)

def sfx_scratch():
    t = np.arange(int(SR * 0.35)) / SR
    f = 900 * np.exp(-t * 6) + 120
    rng = np.random.default_rng(2)
    return 0.45 * (np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.6 + 0.4 * rng.standard_normal(len(t))) * np.exp(-t * 5)

def build_audio(path):
    total = np.zeros(int(SR * (TOTAL + 0.5)), np.float32)
    for (c, a, b, *_), o in zip(PIECES, piece_out):
        src = os.path.join(TMP, f'c{c}.wav')
        if not os.path.exists(src):
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(CL, f'c{c}.mp4'), '-ac', '1', '-ar', str(SR), src], check=True)
        x = load_wav(src)
        seg = x[int(a * SR):int(b * SR)].copy()
        # igualar volumen entre clips: RMS de la voz a -18 dBFS
        act = seg[np.abs(seg) > 0.02]
        rms = np.sqrt(np.mean(act ** 2)) if len(act) else 0.1
        seg *= (10 ** (-18 / 20)) / max(rms, 1e-4)
        fade = int(SR * 0.012)
        seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
        i = int(o * SR); total[i:i + len(seg)] += seg
    def add(snd, t, g):
        i = int(t * SR); total[i:i + len(snd)] += g * snd[:len(total) - i]
    for k in ('cena_in', 'reg_in', 'd1', 'd3', 'k1', 'k2', 'k3'):
        add(sfx_pop(), T[k], 0.35)
    for k in ('cena_out', 'reg_out'):
        add(sfx_whoosh(), T[k], 0.35)
    add(sfx_ding(), T['conc'], 0.45)
    add(sfx_scratch(), T['postre'], 0.5)
    add(sfx_ding(), T['pasa'], 0.4)
    add(sfx_pop(), T['friega'], 0.4)
    add(sfx_ding(), MAIN_DUR + 0.05, 0.35)
    for o, p in zip(piece_out, PIECES):
        if p[5]:
            add(sfx_whoosh(), max(0, o - 0.15), 0.18)
    total = total[:int(SR * TOTAL)]
    total *= (10 ** (-3 / 20)) / np.abs(total).max()   # pico a -3 dB
    out = (total * 32767).astype(np.int16)
    w = wave.open(path, 'w'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes()); w.close()

# ---------- vídeo ----------
def clip_frames(c, start, dur):
    """Fotogramas 30 fps, escalados para cubrir 720x1280 (centrado)."""
    vf = f'fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}'
    p = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{start:.3f}', '-t', f'{dur + 0.2:.3f}', '-i', os.path.join(CL, f'c{c}.mp4'),
                        '-vf', vf, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True)
    n = len(p.stdout) // (W * H * 3)
    return [Image.frombuffer('RGB', (W, H), p.stdout[i * W * H * 3:(i + 1) * W * H * 3]) for i in range(n)]

_COVER = None
def book_overlay(fr):
    """Pone la portada real sobre el libro amarillo de Grok, respetando los dedos."""
    global _COVER
    if _COVER is None:
        _COVER = Image.open(PORTADA).convert('RGB')
    hsv = np.array(fr.convert('HSV')).astype(int)
    m = (hsv[..., 0] > 28) & (hsv[..., 0] < 48) & (hsv[..., 1] > 120) & (hsv[..., 2] > 170)
    m = ndimage.binary_closing(m, iterations=4)
    lab, n = ndimage.label(m)
    if n == 0:
        return fr
    sz = ndimage.sum(m, lab, range(1, n + 1)); k = int(np.argmax(sz)) + 1
    if sz[k - 1] < 28000:
        return fr
    comp = ndimage.binary_fill_holes(lab == k)
    ys, xs = np.nonzero(comp)
    x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    if not 0.55 < (x1 - x0) / (y1 - y0) < 1.05:
        return fr
    cov = _COVER.resize((x1 - x0, y1 - y0), Image.LANCZOS)
    alpha = Image.fromarray((comp[y0:y1, x0:x1] * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
    out = fr.copy(); out.paste(cov, (int(x0), int(y0)), alpha)
    return out

def end_card(last):
    bg = last.filter(ImageFilter.GaussianBlur(18)).convert('RGBA')
    bg.alpha_composite(Image.new('RGBA', (W, H), (255, 214, 0, 150)))
    cov = Image.open(PORTADA).convert('RGBA')
    ch = 720; cw = int(cov.width * ch / cov.height)
    cov = cov.resize((cw, ch), Image.LANCZOS)
    sh = Image.new('RGBA', (cw + 40, ch + 40), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((20, 20, cw + 20, ch + 20), fill=(0, 0, 0, 120))
    sh = sh.filter(ImageFilter.GaussianBlur(14))
    return bg, cov, sh

def main():
    audio = os.path.join(TMP, 'audio.wav'); build_audio(audio)
    master = os.path.join(TMP, 'master.mp4')
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-pix_fmt', 'yuv420p', master], stdin=subprocess.PIPE)
    fi = 0; last = None
    for (c, a, b, voff, z0, flash), o in zip(PIECES, piece_out):
        dur = b - a
        frames = clip_frames(c, a + voff, dur)
        n_out = int(round((o + dur) * FPS)) - int(round(o * FPS))
        for j in range(n_out):
            t = (fi) / FPS
            fr = frames[min(j, len(frames) - 1)]
            if c == 9:
                fr = book_overlay(fr)
            z = z0 + 0.05 * (j / max(1, n_out))
            if T['conc'] <= t < T['conc'] + 0.4:
                z += 0.06 * (1 - (t - T['conc']) / 0.4)
            if T['postre'] <= t < T['postre'] + 0.35:
                z += 0.05
            cw, chh = W / z, H / z
            x0, y0 = (W - cw) / 2, (H - chh) / 2
            img = fr.crop((int(x0), int(y0), int(x0 + cw), int(y0 + chh))).resize((W, H), Image.BILINEAR).convert('RGBA')
            draw_badges(img, t)
            # destellos
            fl = 0
            if flash and j < 6:
                fl = 0.85 * (1 - j / 6)
            if T['conc'] <= t < T['conc'] + 0.3:
                fl = max(fl, 0.7 * (1 - (t - T['conc']) / 0.3))
            if fl > 0:
                img.alpha_composite(Image.new('RGBA', (W, H), (255, 255, 240, int(255 * fl))))
            draw_caption(img, t)
            enc.stdin.write(img.convert('RGB').tobytes()); fi += 1
            last = fr
    bg, cov, sh = end_card(last)
    n_end = int(round(TOTAL * FPS)) - fi
    f1 = FBIG(64); f2 = FBIG(40)
    for j in range(n_end):
        img = bg.copy()
        k = ease(j / 8)
        s = 0.7 + 0.3 * k
        paste_c(img, sh, 340, 470, s); paste_c(img, cov, 330, 460, s)
        d = ImageDraw.Draw(img)
        if j >= 4:
            txt = 'Búscalo en Amazon'; bb = d.textbbox((0, 0), txt, font=f1, stroke_width=7)
            d.text((330 - (bb[2] + bb[0]) / 2, 868), txt, font=f1, fill=WHITE, stroke_width=7, stroke_fill=DARK)
            txt = 'Pasatiempos tóxicos · Navidad'; bb = d.textbbox((0, 0), txt, font=f2, stroke_width=5)
            d.text((330 - (bb[2] + bb[0]) / 2, 962), txt, font=f2, fill=ORANGE, stroke_width=5, stroke_fill=DARK)
        enc.stdin.write(img.convert('RGB').tobytes()); fi += 1
    enc.stdin.close(); enc.wait()
    vk = int((2.85 * 8 * 1024) / TOTAL - 96)   # kbit/s de vídeo para quedar < 3 MB
    log = os.path.join(TMP, 'pass')
    base = ['ffmpeg', '-v', 'error', '-y', '-i', master, '-i', audio, '-c:v', 'libx264', '-preset', 'slow', '-b:v', f'{vk}k',
            '-maxrate', f'{int(vk * 1.6)}k', '-bufsize', f'{vk * 3}k', '-pix_fmt', 'yuv420p', '-passlogfile', log]
    subprocess.run(base + ['-pass', '1', '-an', '-f', 'mp4', '/dev/null'], check=True)
    subprocess.run(base + ['-pass', '2', '-c:a', 'aac', '-b:a', '96k', '-af', 'loudnorm=I=-14:TP=-1.5', '-ar', '44100',
                           '-shortest', '-movflags', '+faststart', OUT], check=True)
    print('OK', OUT, f'{TOTAL:.2f}s')
    for k, v in sorted(T.items(), key=lambda x: x[1]):
        print(f'  {k}: {v:.2f}')

if __name__ == '__main__':
    main()
