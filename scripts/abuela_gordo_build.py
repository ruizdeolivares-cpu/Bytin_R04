#!/usr/bin/env python3
"""«Si nos toca el Gordo» · abuela 2D, palabra a palabra, pegatinas emoji y zooms en los remates.
Uso: python3 abuela_gordo_build.py CLIPS_DIR FONT.woff PORTADA.png SALIDA.mp4   (CLIPS_DIR con g1.mp4 g2.mp4 g3.mp4)"""
import sys, os, re, math, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

CL, FONT, PORTADA, OUT = sys.argv[1:5]
W, H, FPS, SR = 720, 1280, 30, 44100
TMP = os.path.join(os.path.dirname(OUT), 'gordo_tmp'); os.makedirs(TMP, exist_ok=True)
EMOJI = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'

# segmentos de voz medidos y texto (|frase| = remate que sale entero)
SEGS = {
 1: [(0.07, 1.05, 'Todos los años,'), (1.21, 3.00, 'en la cena, la misma pregunta:'),
     (3.59, 5.26, '¿qué haríais si nos toca el *Gordo?*')],
 2: [(0.09, 0.44, '*Toni,*'), (0.57, 1.20, 'un Tesla.'), (1.46, 1.88, '*Iván,*'), (2.03, 3.03, 'hacerse influencer.'),
     (3.48, 5.04, '*Mari* *Carmen,* dejar de cocinar…'), (5.34, 6.16, '|COMO SI COCINARA|')],
 3: [(0.08, 0.52, '¿Y yo?'), (1.14, 2.52, 'Yo me compro una *casita.*'), (3.02, 3.49, 'Pequeña.'),
     (4.06, 4.96, 'De una *habitación…*'), (5.55, 6.53, '|PARA QUE NO QUEPÁIS|')],
}
# piezas: (clip, ini, fin, zoom, foco_y, destello)
PIECES = [
 (1, 0.00, 3.15, 1.30, 0.56, False), (1, 3.45, 6.40, 1.55, 0.52, False),
 (2, 0.00, 1.32, 1.35, 0.55, True), (2, 1.38, 3.20, 1.50, 0.53, False), (2, 3.38, 5.22, 1.38, 0.55, False),
 (2, 5.25, 7.30, 1.75, 0.47, False),
 (3, 0.00, 2.75, 1.35, 0.55, True), (3, 2.85, 5.20, 1.50, 0.52, False), (3, 5.40, 7.90, 1.80, 0.46, False),
]
END_DUR = 1.9
STICKERS = [  # (clip, palabra, emoji)
 (1, 'Gordo', '🎟️'), (2, 'Tesla', '🚗'), (2, 'influencer', '📱'), (2, 'cocinar', '🍳'),
 (3, 'casita', '🏠'), (3, 'quepáis', '🚪'),
]

def syl(w):
    return max(1, len(re.findall(r'[aeiouáéíóúü]+', w.lower())))

piece_out = []; acc = 0.0
for p in PIECES:
    piece_out.append(acc); acc += p[2] - p[1]
MAIN_DUR = acc; TOTAL = MAIN_DUR + END_DUR

def src2out(c, t):
    for (pc, a, b, *_), o in zip(PIECES, piece_out):
        if pc == c and a - 0.05 <= t <= b + 0.05:
            return o + min(max(t, a), b) - a
    return None

WORDS = []  # (ini, fin, texto, clave, clip, remate)
for c, segs in SEGS.items():
    raw = []
    for a, b, txt in segs:
        if txt.startswith('|'):
            raw.append([a, b + 1.0, txt.strip('|'), True, True]); continue
        toks = txt.split(); ws = [syl(t) + 0.6 for t in toks]; tot = sum(ws); t = a
        for tok, wg in zip(toks, ws):
            d = (b - a) * wg / tot
            raw.append([t, t + d, tok.strip('*'), tok.startswith('*'), False]); t += d
    for i in range(len(raw) - 1):
        if not raw[i][4]:
            raw[i][1] = raw[i + 1][0] if raw[i + 1][0] - raw[i][1] < 0.35 else raw[i][1] + 0.15
    for a, b, wd, k, rem in raw:
        oa = src2out(c, a); ob = src2out(c, b)
        if oa is None: continue
        if ob is None: ob = oa + (b - a)
        WORDS.append((oa, ob, wd, k, c, rem))

def wtime(clip, word):
    for oa, ob, wd, k, c, rem in WORDS:
        if c == clip and word.lower() in wd.lower():
            return oa
    raise KeyError(word)

PUNCH = [wtime(2, 'COMO SI'), wtime(3, 'PARA QUE')]

# ---------- gráficos ----------
FB = lambda s: ImageFont.truetype(FONT, s)
WHITE, ORANGE, DARK = (255, 255, 255), (255, 170, 30), (35, 22, 10)
_c = {}

def text_img(txt, key, size=124, maxw=560):
    k = (txt, key, size)
    if k in _c: return _c[k]
    while True:
        f = FB(size); bb = f.getbbox(txt, stroke_width=9)
        if bb[2] - bb[0] <= maxw or size < 50: break
        size -= 6
    im = Image.new('RGBA', (bb[2] - bb[0] + 30, bb[3] - bb[1] + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((19 - bb[0], 21 - bb[1]), txt, font=f, fill=(0, 0, 0, 120), stroke_width=9, stroke_fill=(0, 0, 0, 120))
    d.text((15 - bb[0], 15 - bb[1]), txt, font=f, fill=ORANGE if key else WHITE, stroke_width=9, stroke_fill=DARK)
    _c[k] = im; return im

def lines_img(lines, key):
    ims = [text_img(l, key, 112) for l in lines]
    w = max(i.width for i in ims); h = sum(i.height for i in ims) - 20 * (len(ims) - 1)
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0)); y = 0
    for i in ims:
        out.alpha_composite(i, ((w - i.width) // 2, y)); y += i.height - 20
    return out

def halo(w=W, h=420):
    im = Image.new('L', (w, h), 0); ImageDraw.Draw(im).ellipse((60, 90, w - 120, h - 90), fill=135)
    im = im.filter(ImageFilter.GaussianBlur(55)); out = Image.new('RGBA', im.size, (0, 0, 0, 0)); out.putalpha(im); return out
HALO = halo(); HALO_BIG = halo(W, 640)
CAP_X, CAP_Y = 335, 870

def emoji_img(e, size=150):
    f = ImageFont.truetype(EMOJI, 109)
    im = Image.new('RGBA', (160, 160), (0, 0, 0, 0)); ImageDraw.Draw(im).text((10, 10), e, font=f, embedded_color=True)
    im = im.crop(im.getbbox()); s = size / max(im.size)
    im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    # borde blanco tipo pegatina
    a = im.getchannel('A').filter(ImageFilter.MaxFilter(13))
    st = Image.new('RGBA', (im.width + 24, im.height + 24), (0, 0, 0, 0))
    wbg = Image.new('RGBA', im.size, (255, 255, 255, 255)); wbg.putalpha(a)
    st.alpha_composite(wbg, (12, 12)); st.alpha_composite(im, (12, 12)); return st

def ease(x):
    x = min(max(x, 0), 1); return 1 - (1 - x) ** 3

def paste_c(base, im, cx, cy, scale=1.0, alpha=1.0, rot=0):
    if scale != 1.0:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    if rot: im = im.rotate(rot, resample=Image.BILINEAR, expand=True)
    if alpha < 1.0:
        a = im.getchannel('A').point(lambda v: int(v * alpha)); im = im.copy(); im.putalpha(a)
    base.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))

STK = []
for c, w, e in STICKERS:
    t0 = wtime(c, w)
    STK.append((t0, emoji_img(e)))

def draw_stickers(fr, t):
    for i, (t0, im) in enumerate(STK):
        t1 = STK[i + 1][0] if i + 1 < len(STK) else MAIN_DUR
        t1 = min(t1, t0 + 2.2)
        if t0 <= t < t1:
            k = ease((t - t0) / 0.22); bob = 6 * math.sin((t - t0) * 6)
            paste_c(fr, im, 545, 300 + bob, 0.3 + 0.7 * k + 0.15 * math.sin(min(1, (t - t0) / 0.22) * math.pi), rot=-8 + 4 * math.sin((t - t0) * 3))

def draw_caption(fr, t):
    if t < piece_out[0] + 1.25:   # gancho completo en el fotograma 0
        paste_c(fr, HALO_BIG, CAP_X, CAP_Y)
        paste_c(fr, lines_img(['¿QUÉ HARÍAS', 'SI TE TOCA', 'EL GORDO?'], False), CAP_X, CAP_Y)
        return
    for oa, ob, wd, key, c, rem in WORDS:
        if oa <= t < ob:
            if rem:
                paste_c(fr, HALO_BIG, CAP_X, CAP_Y)
                parts = wd.split(' ')
                lines = [' '.join(parts[:2]), ' '.join(parts[2:])]
                k = ease((t - oa) / 0.18)
                paste_c(fr, lines_img(lines, True), CAP_X, CAP_Y, 1.35 - 0.35 * k)
            else:
                paste_c(fr, HALO, CAP_X, CAP_Y)
                paste_c(fr, text_img(wd, key), CAP_X, CAP_Y, 1.0 + 0.18 * (1 - ease((t - oa) / 0.12)))
            return

# ---------- audio ----------
def load_wav(p):
    w = wave.open(p); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    return x.reshape(-1, w.getnchannels()).mean(axis=1)

def sfx_pop():
    t = np.arange(int(SR * 0.12)) / SR; f = 700 + 900 * t / 0.12
    return 0.5 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 30)

def sfx_boom():
    t = np.arange(int(SR * 0.6)) / SR; f = 90 * np.exp(-t * 3) + 40
    rng = np.random.default_rng(3)
    return 0.8 * (np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.15 * rng.standard_normal(len(t))) * np.exp(-t * 6)

def sfx_ding():
    t = np.arange(int(SR)) / SR
    return 0.35 * (np.sin(2 * np.pi * 1568 * t) + 0.6 * np.sin(2 * np.pi * 2349 * t)) * np.exp(-t * 4)

def sfx_whoosh():
    n = int(SR * 0.4); rng = np.random.default_rng(1); x = rng.standard_normal(n)
    y = np.convolve(x, np.ones(30) / 30, 'same'); return 0.6 * y * np.sin(np.pi * np.arange(n) / n) ** 2 / np.abs(y).max()

def build_audio(path):
    total = np.zeros(int(SR * (TOTAL + 0.5)), np.float32)
    for (c, a, b, *_), o in zip(PIECES, piece_out):
        src = os.path.join(TMP, f'g{c}.wav')
        if not os.path.exists(src):
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(CL, f'g{c}.mp4'), '-ac', '1', '-ar', str(SR), src], check=True)
        seg = load_wav(src)[int(a * SR):int(b * SR)].copy()
        act = seg[np.abs(seg) > 0.02]; rms = np.sqrt(np.mean(act ** 2)) if len(act) else 0.1
        seg *= (10 ** (-18 / 20)) / max(rms, 1e-4)
        fd = int(SR * 0.012); seg[:fd] *= np.linspace(0, 1, fd); seg[-fd:] *= np.linspace(1, 0, fd)
        i = int(o * SR); total[i:i + len(seg)] += seg
    def add(s, t, g):
        i = int(t * SR); total[i:i + len(s)] += g * s[:len(total) - i]
    for t0, _ in STK: add(sfx_pop(), t0, 0.35)
    for t0 in PUNCH: add(sfx_boom(), t0, 0.45)
    for (c, a, b, z, fy, fl), o in zip(PIECES, piece_out):
        if fl: add(sfx_whoosh(), max(0, o - 0.12), 0.2)
    add(sfx_ding(), MAIN_DUR + 0.05, 0.35)
    total = total[:int(SR * TOTAL)]; total *= (10 ** (-3 / 20)) / np.abs(total).max()
    w = wave.open(path, 'w'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((total * 32767).astype(np.int16).tobytes()); w.close()

# ---------- vídeo ----------
def clip_frames(c, start, dur):
    vf = f'fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}'
    p = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{start:.3f}', '-t', f'{dur + 0.2:.3f}', '-i', os.path.join(CL, f'g{c}.mp4'),
                        '-vf', vf, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True)
    n = len(p.stdout) // (W * H * 3)
    return [Image.frombuffer('RGB', (W, H), p.stdout[i * W * H * 3:(i + 1) * W * H * 3]) for i in range(n)]

def main():
    audio = os.path.join(TMP, 'audio.wav'); build_audio(audio)
    master = os.path.join(TMP, 'master.mp4')
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-pix_fmt', 'yuv420p', master], stdin=subprocess.PIPE)
    fi = 0; last = None
    for (c, a, b, z0, fy, flash), o in zip(PIECES, piece_out):
        dur = b - a; frames = clip_frames(c, a, dur)
        n_out = int(round((o + dur) * FPS)) - int(round(o * FPS))
        for j in range(n_out):
            t = fi / FPS; fr = frames[min(j, len(frames) - 1)]
            z = z0 + 0.06 * (j / max(1, n_out))
            for pt in PUNCH:
                if pt <= t < pt + 0.25: z += 0.12 * (1 - (t - pt) / 0.25)
            cw, ch = W / z, H / z
            x0 = (W - cw) / 2; y0 = min(max(H * fy - ch / 2, 0), H - ch)
            sh = 8 * math.sin(t * 70) if any(pt <= t < pt + 0.25 for pt in PUNCH) else 0
            img = fr.crop((int(x0 + sh), int(y0), int(x0 + sh + cw), int(y0 + ch))).resize((W, H), Image.BILINEAR).convert('RGBA')
            draw_stickers(img, t)
            if flash and j < 5:
                img.alpha_composite(Image.new('RGBA', (W, H), (255, 255, 240, int(200 * (1 - j / 5)))))
            draw_caption(img, t)
            enc.stdin.write(img.convert('RGB').tobytes()); fi += 1; last = fr
    # cierre
    bg = last.filter(ImageFilter.GaussianBlur(18)).convert('RGBA'); bg.alpha_composite(Image.new('RGBA', (W, H), (255, 214, 0, 150)))
    cov = Image.open(PORTADA).convert('RGBA'); chh = 720; cw = int(cov.width * chh / cov.height); cov = cov.resize((cw, chh), Image.LANCZOS)
    f1 = FB(64); f2 = FB(40)
    for j in range(int(round(TOTAL * FPS)) - fi):
        img = bg.copy(); s = 0.7 + 0.3 * ease(j / 8); paste_c(img, cov, 330, 460, s); d = ImageDraw.Draw(img)
        if j >= 4:
            for txt, f, col, y, sw in (('Búscalo en Amazon', f1, WHITE, 868, 7), ('Pasatiempos tóxicos · Navidad', f2, ORANGE, 962, 5)):
                bb = d.textbbox((0, 0), txt, font=f, stroke_width=sw)
                d.text((330 - (bb[2] + bb[0]) / 2, y), txt, font=f, fill=col, stroke_width=sw, stroke_fill=DARK)
        enc.stdin.write(img.convert('RGB').tobytes()); fi += 1
    enc.stdin.close(); enc.wait()
    vk = int((2.85 * 8 * 1024) / TOTAL - 96); vk = min(vk, 1100); log = os.path.join(TMP, 'pass')
    base = ['ffmpeg', '-v', 'error', '-y', '-i', master, '-i', audio, '-c:v', 'libx264', '-preset', 'slow', '-b:v', f'{vk}k',
            '-maxrate', f'{int(vk * 1.6)}k', '-bufsize', f'{vk * 3}k', '-pix_fmt', 'yuv420p', '-passlogfile', log]
    subprocess.run(base + ['-pass', '1', '-an', '-f', 'mp4', '/dev/null'], check=True)
    subprocess.run(base + ['-pass', '2', '-c:a', 'aac', '-b:a', '96k', '-af', 'loudnorm=I=-14:TP=-1.5', '-ar', '44100',
                           '-shortest', '-movflags', '+faststart', OUT], check=True)
    print('OK', OUT, f'{TOTAL:.2f}s')

if __name__ == '__main__':
    main()
