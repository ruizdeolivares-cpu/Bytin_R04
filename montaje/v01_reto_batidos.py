#!/usr/bin/env python3
"""V01 · Reto de los batidos (p.69, problema 6). Dirigido a padres.
Uso: python3 v01_reto_batidos.py <dir_build> <pagina69.png> <salida.mp4>
"""
import sys, os, subprocess, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BUILD, P69, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIPS = os.path.join(REPO, 'kling', 'clips')
W, H, FPS = 720, 1280, 30
FONT = os.path.join(BUILD, 'fontsource-baloo-2-5.3.0/package/files/baloo-2-latin-800-normal.woff')
SFX = os.path.join(BUILD, 'uisfx-0.4.0/package/sounds')
MUSIC = os.path.join(REPO, 'musica', 'starostin-sneaky-quirky-music-635314.mp3')
MUSIC_START = 4.0
NARANJA, AMARILLO, OSCURO, BLANCO = (255, 138, 0), (255, 214, 64), (35, 30, 45), (255, 255, 255)

def font(s): return ImageFont.truetype(FONT, s)

def clip_frames(name, start, dur):
    """Devuelve lista de frames PIL 720x1280 del clip."""
    p = os.path.join(CLIPS, name)
    n = int(round(dur * FPS))
    cmd = ['ffmpeg', '-v', 'error', '-ss', str(start), '-i', p, '-t', str(dur + 0.2),
           '-vf', f'fps={FPS},scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    fr = [Image.frombuffer('RGB', (W, H), raw[i*W*H*3:(i+1)*W*H*3]) for i in range(len(raw)//(W*H*3))]
    while len(fr) < n: fr.append(fr[-1])
    return fr[:n]

def zoom(img, z, cx=0.5, cy=0.5):
    """Zoom centrado (z>=1)."""
    w, h = img.size
    nw, nh = w / z, h / z
    x0 = (w - nw) * cx; y0 = (h - nh) * cy
    return img.crop((int(x0), int(y0), int(x0 + nw), int(y0 + nh))).resize((W, H), Image.LANCZOS)

def ease_pop(t, d=0.22):
    """Escala con rebote para textos que entran (0→1)."""
    if t <= 0: return 0.0
    if t >= d: return 1.0
    x = t / d
    return 1 + 0.18 * math.sin(x * math.pi) * (1 - x) * 2 if x > 0.55 else x / 0.55 * 1.12

def text_img(lines, size, colors=None, stroke=9, maxw=560):
    """lines: lista de (texto, color). Ajusta tamaño para caber en maxw."""
    s = size
    while True:
        f = font(s)
        ws = [f.getbbox(t, stroke_width=stroke)[2] for t, _ in lines]
        if max(ws) <= maxw or s < 30: break
        s -= 2
    lh = int(s * 1.08)
    img = Image.new('RGBA', (max(ws) + 20, lh * len(lines) + 30), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for i, (t, c) in enumerate(lines):
        w = f.getbbox(t, stroke_width=stroke)[2]
        d.text(((img.width - w) // 2, 10 + i * lh), t, font=f, fill=c, stroke_width=stroke, stroke_fill=OSCURO)
    # sombra
    sh = Image.new('RGBA', img.size, (0, 0, 0, 0))
    sh.paste((0, 0, 0, 110), mask=img.split()[3])
    sh = sh.filter(ImageFilter.GaussianBlur(6))
    out = Image.new('RGBA', (img.width + 12, img.height + 12), (0, 0, 0, 0))
    out.alpha_composite(sh, (10, 10)); out.alpha_composite(img, (0, 0))
    return out

def pill(text, size, bg, fg=BLANCO):
    f = font(size)
    bb = f.getbbox(text)
    img = Image.new('RGBA', (bb[2] + 44, int(size * 1.45)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, img.width - 1, img.height - 1), radius=img.height // 2, fill=bg, outline=OSCURO, width=5)
    d.text((22, int(size * 0.12)), text, font=f, fill=fg)
    return img

def place(frame, overlay, cx, y, t, scale_fn=ease_pop):
    """Pega overlay centrado en cx (respetando x<=620) con animación pop."""
    k = scale_fn(t)
    if k <= 0: return
    ov = overlay if abs(k - 1) < 1e-3 else overlay.resize((max(1, int(overlay.width * k)), max(1, int(overlay.height * k))), Image.LANCZOS)
    x = int(cx - ov.width / 2)
    x = max(16, min(x, 620 - ov.width)) if ov.width < 604 else 16
    frame.alpha_composite(ov, (x, int(y + (overlay.height - ov.height) / 2)))

CX = 318  # centro de la zona segura horizontal (16..620)

# ---------- escenas ----------
segments = []  # (dur, render(i, n) -> RGBA frame)
sfx_events = []  # (tiempo, archivo o 'bip', volumen)

def add(dur, fn): segments.append((dur, fn))

# S1 gancho: R-04 con "?" + pregunta a los padres
f1 = clip_frames('G2c_r04_interrogacion.mp4', 0.0, 1.9)
t_pill = pill('RETO PARA PADRES', 34, NARANJA)
t1 = text_img([('¿Tu hijo sabría', BLANCO), ('resolver esto?', AMARILLO)], 84)
def s1(i, n):
    fr = zoom(f1[i], 1.0 + 0.06 * i / n).convert('RGBA'); t = i / FPS
    place(fr, t_pill, CX, 175, t)
    place(fr, t1, CX, 240, t - 0.12)
    return fr
add(1.9, s1)

# S2 Lía: cada batido cuesta 1 €
f2 = clip_frames('G2a_lia_batido.mp4', 0.3, 1.8)
t2 = text_img([('Cada batido', BLANCO), ('cuesta 1 €', AMARILLO)], 92)
def s2(i, n):
    fr = zoom(f2[i], 1.04 - 0.04 * i / n, 0.5, 0.6).convert('RGBA')
    place(fr, t2, CX, 110, i / FPS - 0.05); return fr
add(1.8, s2)

# S3 opción A
f3 = clip_frames('G3a_bityn_rasca_cabeza.mp4', 0.2, 1.9)
tA = pill('OPCIÓN A', 38, (60, 140, 255))
tA2 = text_img([('A 2 € vendes', BLANCO), ('40 batidos', AMARILLO)], 92)
def s3(i, n):
    fr = zoom(f3[i], 1.1 + 0.05 * i / n, 0.5, 0.65).convert('RGBA'); t = i / FPS
    place(fr, tA, CX, 105, t); place(fr, tA2, CX, 175, t - 0.12); return fr
add(1.9, s3)

# S4 opción B
f4 = clip_frames('G3b_bityn_idea.mp4', 0.1, 1.9)
tB = pill('OPCIÓN B', 38, (230, 60, 120))
tB2 = text_img([('A 3 € vendes', BLANCO), ('25 batidos', AMARILLO)], 92)
def s4(i, n):
    fr = zoom(f4[i], 1.0 + 0.05 * i / n, 0.5, 0.75).convert('RGBA'); t = i / FPS
    place(fr, tB, CX, 105, t); place(fr, tB2, CX, 175, t - 0.12); return fr
add(1.9, s4)

# S5 página del libro (Bityn con 6 brazos) + pregunta + cuenta atrás 3-2-1
pg = Image.open(P69).convert('RGB')
_pgw = pg.copy(); ImageDraw.Draw(_pgw).rectangle((740, 200, 1010, 585), fill=(255, 255, 255))  # quita el bocadillo
head = _pgw.crop((150, 200, 875, 800))  # ilustración de Bityn con calculadoras
bg5 = Image.new('RGB', (W, H), (255, 255, 255))
hw = 700; hh = int(head.height * hw / head.width)
q = text_img([('¿Con qué precio', BLANCO), ('GANAS MÁS?', NARANJA)], 92)
nums = [text_img([(str(k), AMARILLO)], 230, stroke=12) for k in (3, 2, 1)]
def s5(i, n):
    t = i / FPS; z = 1.0 + 0.08 * i / n
    fr = bg5.copy()
    im = head.resize((int(hw * z), int(hh * z)), Image.LANCZOS)
    fr.paste(im, ((W - im.width) // 2 - 10, 470 - (im.height - hh) // 2))
    fr = fr.convert('RGBA')
    place(fr, q, CX, 110, t)
    k = min(2, int(t // 1.0)); tt = t - k * 1.0
    place(fr, nums[k], CX, 760, tt, lambda x: ease_pop(x, 0.18))
    return fr
add(3.0, s5)

# S6 R-04 sorpresa: respuesta en comentarios
f6 = clip_frames('G3c_r04_sorpresa.mp4', 0.0, 1.9)
t6 = text_img([('Escribe A o B', BLANCO), ('en comentarios', AMARILLO)], 88)
def s6(i, n):
    fr = zoom(f6[i], 1.0 + 0.08 * i / n).convert('RGBA')
    place(fr, t6, CX, 110, i / FPS); return fr
add(1.9, s6)

# S7 el reto está en el libro (problema 6 real)
pw0 = 600; ph0 = int(pg.height * pw0 / pg.width)
pgs = pg.resize((pw0, ph0), Image.LANCZOS)
ImageDraw.Draw(pgs).rounded_rectangle((int(150*pw0/pg.width), int(1590*pw0/pg.width), int(1570*pw0/pg.width), int(1755*pw0/pg.width)), radius=10, outline=NARANJA, width=5)
t7 = text_img([('Este reto está', BLANCO), ('en el libro', AMARILLO)], 92)
t7b = pill('y muchos más', 40, NARANJA)
def s7(i, n):
    t = i / FPS
    fr = Image.new('RGB', (W, H), (255, 236, 200))
    z = 1.0 + 0.12 * i / n
    im = pgs.resize((int(pw0 * z), int(ph0 * z)), Image.LANCZOS)
    cy = int(1670 * pw0 / pg.width * z)  # mantener el problema 6 a la vista
    x = CX - im.width // 2; y = 300 - int((z - 1) * (cy - 0))
    sh = Image.new('RGBA', (im.width + 30, im.height + 30), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle((15, 15, im.width + 15, im.height + 15), fill=(0, 0, 0, 90))
    fr = fr.convert('RGBA'); fr.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)), (x - 5, y - 5)); fr.paste(im, (x, y))
    place(fr, t7, CX, 80, t); place(fr, t7b, CX, 975, t - 0.35)
    return fr
add(1.9, s7)

# S8 cierre: portada + Búscalo en Amazon (2.5 s)
cov = Image.open(os.path.join(REPO, 'libro', 'portada_frontal_720.png')).convert('RGB')
bg8 = cov.resize((W, int(cov.height * W / cov.width))).resize((W, H)).filter(ImageFilter.GaussianBlur(25))
bg8 = Image.blend(bg8, Image.new('RGB', (W, H), (20, 15, 40)), 0.35)
cw = 470; chh = int(cov.height * cw / cov.width)
covs = cov.resize((cw, chh), Image.LANCZOS)
t8 = text_img([('¡Búscalo', BLANCO), ('en Amazon!', AMARILLO)], 96)
def s8(i, n):
    t = i / FPS
    fr = bg8.copy().convert('RGBA')
    k = ease_pop(t, 0.3)
    c = covs.resize((max(1, int(cw * k)), max(1, int(chh * k)))) if k > 0 else None
    if c:
        y = 330 + (chh - c.height) // 2
        sh = Image.new('RGBA', (c.width + 30, c.height + 30), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rectangle((15, 15, c.width + 15, c.height + 15), fill=(0, 0, 0, 140))
        sh = sh.filter(ImageFilter.GaussianBlur(10))
        fr.alpha_composite(sh, (CX - c.width // 2 - 5, y - 5))
        fr.paste(c, (CX - c.width // 2, y))
    place(fr, t8, CX, 80, t - 0.15)
    return fr
add(2.5, s8)

# ---------- SFX ----------
def tstart(k): return sum(d for d, _ in segments[:k])
sfx_events += [
    (0.0, 'bip', 0.6), (0.12, f'{SFX}/arcade/notification.mp3', 0.8),
    (tstart(1), f'{SFX}/arcade/swipe.mp3', 0.7), (tstart(1) + 0.05, f'{SFX}/rubber/select.mp3', 0.8),
    (tstart(2), f'{SFX}/arcade/swipe.mp3', 0.7), (tstart(2) + 0.12, f'{SFX}/arcade/purchase.mp3', 0.8),
    (tstart(3), f'{SFX}/arcade/swipe.mp3', 0.7), (tstart(3) + 0.12, f'{SFX}/arcade/purchase.mp3', 0.8),
    (tstart(4), f'{SFX}/arcade/swipe.mp3', 0.7),
    (tstart(4) + 0.0, f'{SFX}/arcade/progress-step.mp3', 1.0), (tstart(4) + 1.0, f'{SFX}/arcade/progress-step.mp3', 1.0),
    (tstart(4) + 2.0, f'{SFX}/arcade/progress-step.mp3', 1.0),
    (tstart(5), 'bip', 0.7), (tstart(5) + 0.1, f'{SFX}/arcade/notification.mp3', 0.7),
    (tstart(6), f'{SFX}/arcade/swipe.mp3', 0.7), (tstart(6) + 0.35, f'{SFX}/rubber/select.mp3', 0.8),
    (tstart(7), f'{SFX}/arcade/swipe.mp3', 0.7), (tstart(7) + 0.2, f'{SFX}/arcade/achievement.mp3', 0.9),
]
TOTAL = sum(d for d, _ in segments)

# ---------- render vídeo ----------
tmpv = OUT + '.v.mp4'
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                        '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', tmpv], stdin=subprocess.PIPE)
for dur, fn in segments:
    n = int(round(dur * FPS))
    for i in range(n):
        enc.stdin.write(fn(i, n).convert('RGB').tobytes())
enc.stdin.close(); enc.wait()

# ---------- audio ----------
SR = 44100
def load(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).copy()
def bip():
    t = np.arange(int(SR * 0.22)) / SR
    s = np.zeros_like(t)
    for a, b, fq in ((0, 0.08, 1320), (0.11, 0.2, 1760)):
        m = (t >= a) & (t < b); s[m] = np.sin(2 * np.pi * fq * t[m]) * np.hanning(m.sum())
    return np.stack([s, s], 1).astype(np.float32) * 0.5
N = int(TOTAL * SR)
mus = load(MUSIC)[int(MUSIC_START * SR):][:N]
mus = np.pad(mus, ((0, N - len(mus)), (0, 0)))
fade = int(0.6 * SR); mus[-fade:] *= np.linspace(1, 0, fade)[:, None]
mix = mus * 0.55
for t0, p, v in sfx_events:
    s = bip() if p == 'bip' else load(p)
    a = int(t0 * SR); b = min(N, a + len(s))
    mix[a:b] += s[:b - a] * v
tmpa = OUT + '.a.wav'
import wave
pcm = (np.clip(mix, -1, 1) * 32767).astype('<i2')
with wave.open(tmpa, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmpv, '-i', tmpa,
                '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '23', '-maxrate', '1100k', '-bufsize', '2200k', '-pix_fmt', 'yuv420p',
                '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-c:a', 'aac', '-b:a', '128k', '-ar', '44100', '-movflags', '+faststart', '-shortest', OUT], check=True)
os.remove(tmpv); os.remove(tmpa)
print('OK', OUT, f'{TOTAL:.2f}s', os.path.getsize(OUT) // 1024, 'KB')
