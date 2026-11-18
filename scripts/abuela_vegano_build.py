import math, subprocess, os, numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 720, 1280, 30
D = os.path.dirname(os.path.abspath(__file__)); WK = os.path.dirname(D)
ANTON = f'{WK}/Anton.ttf'; POP = f'{WK}/fonts/pop/package/files/poppins-latin-800-normal.woff'
YEL, MAG, BLK, WHT, RED = (255, 238, 0), (232, 20, 120), (17, 17, 17), (255, 255, 255), (225, 30, 35)
F = lambda p, s: ImageFont.truetype(p, s)

# clip a 30 fps en memoria
CW, CH = 720, 810
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{WK}/clips/grok5_cut.mp4', '-vf', 'fps=30,scale=720:810',
                      '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
CLIP = np.frombuffer(raw, np.uint8).reshape(-1, CH, CW, 3)
def cf(t): return Image.fromarray(CLIP[min(int(round(t * FPS)), len(CLIP) - 1)])

# tramos: (inicio salida, fin salida, inicio clip, zoom0, zoom1, centro y del zoom)
SEG = [
    (0.0, 3.35, 0.0, 1.00, 1.04, 405),
    (3.35, 6.55, 3.35, 1.04, 1.08, 405),
    (6.55, 8.3, 6.55, 1.10, 1.20, 360),
]
T_END_CLIP, T_END = 8.3, 9.5

def zoom(img, z, cy):
    w, h = img.size
    if z > 1.0:
        cw, ch = w / z, h / z
        y0 = min(max(cy - ch / 2, 0), h - ch); x0 = (w - cw) / 2
        img = img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((w, h), Image.LANCZOS)
    can = Image.new('RGB', (W, H), BLK); can.paste(img, (0, 300))
    return can

def ease(x): x = max(0, min(1, x)); return 1 - (1 - x) ** 3
def pop(t0, t, dur=0.22):
    x = (t - t0) / dur
    if x <= 0: return 0.05
    if x >= 1: return 1
    return ease(x) + 0.3 * math.sin(x * math.pi) * (1 - x)

def label(img, lines, cy, t0, t, bg=BLK, shake=0):
    """lines: [(texto, tamaño, color)] dentro de una caja centrada en x=310"""
    sc = pop(t0, t)
    d0 = ImageDraw.Draw(img)
    fs = [(s, F(ANTON, max(8, int(sz * sc))), c) for s, sz, c in lines]
    boxes = [d0.textbbox((0, 0), s, font=f) for s, f, c in fs]
    gap = int(10 * sc)
    th = sum(b[3] - b[1] for b in boxes) + gap * (len(fs) - 1)
    tw = max(b[2] - b[0] for b in boxes)
    dx = int(shake * math.sin(t * 60)) if shake else 0
    x0, y0 = 310 - tw / 2 - 24 + dx, cy - th / 2 - 18
    d0.rounded_rectangle((x0 + 7, y0 + 7, x0 + tw + 48 + 7, y0 + th + 36 + 7), 18, fill=BLK)
    d0.rounded_rectangle((x0, y0, x0 + tw + 48, y0 + th + 36), 18, fill=bg, outline=BLK, width=4)
    y = y0 + 18
    for (s, f, c), b in zip(fs, boxes):
        d0.text((310 - (b[2] - b[0]) / 2 - b[0] + dx, y - b[1]), s, font=f, fill=c)
        y += b[3] - b[1] + gap

def say(img, lines, cy, t0, t):
    sc = pop(t0, t)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    f = F(POP, 50); lh = 64
    w = max(d.textlength(l, font=f) for l in lines) + 70; h = lh * len(lines) + 40
    x, y = 310 - w / 2, cy - h / 2
    d.rounded_rectangle((x + 7, y + 7, x + w + 7, y + h + 7), 30, fill=BLK)
    d.rounded_rectangle((x, y, x + w, y + h), 30, fill=WHT, outline=BLK, width=5)
    d.polygon([(x + 90, y + 4), (x + 150, y + 4), (x + 110, y - 50)], fill=WHT)
    d.line([(x + 90, y), (x + 110, y - 50), (x + 150, y)], fill=BLK, width=5)
    for i, l in enumerate(lines):
        b = d.textbbox((0, 0), l, font=f)
        d.text((310 - (b[2] - b[0]) / 2 - b[0], y + 20 + i * lh - b[1] + 6), l, font=f, fill=BLK)
    if sc < 1:
        s = lay.resize((int(W * sc), int(H * sc)))
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); lay.paste(s, (int(310 - 310 * sc), int(cy - cy * sc)))
    img.paste(lay, (0, 0), lay)

def counter(img, t):
    # "12" que baja a "11" en el golpe
    d = ImageDraw.Draw(img)
    n = '12' if t < 2.1 else '11'
    sc = pop(-1 if t < 2.1 else 2.1, t)
    f = F(ANTON, max(8, int(120 * sc)))
    cx, cy = 505, 250
    r = 95 * sc
    d.ellipse((cx - r + 6, cy - r + 6, cx + r + 6, cy + r + 6), fill=BLK)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=YEL if t < 2.1 else RED, outline=BLK, width=5)
    b = d.textbbox((0, 0), n, font=f)
    d.text((cx - (b[2] - b[0]) / 2 - b[0], cy - (b[3] - b[1]) / 2 - b[1] - 8), n, font=f, fill=BLK if t < 2.1 else WHT)
    fs = F(POP, max(8, int(26 * sc))); s = 'trozos'
    b = d.textbbox((0, 0), s, font=fs)
    d.text((cx - (b[2] - b[0]) / 2 - b[0], cy + 48 * sc), s, font=fs, fill=BLK if t < 2.1 else WHT)

def rays_bg(c1, c2, n=18):
    im = Image.new('RGB', (W, H), c1); d = ImageDraw.Draw(im)
    cx, cy, R = W / 2, 560, 1600
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + .5) / n
        d.polygon([(cx, cy), (cx + R * math.cos(a0), cy + R * math.sin(a0)), (cx + R * math.cos(a1), cy + R * math.sin(a1))], fill=c2)
    return im
END_BG = rays_bg((110, 20, 20), (160, 35, 35))
COVER = Image.open(f'{WK}/img/portada.png').convert('RGB')

def end_scene(t):
    lt = t - T_END_CLIP
    img = END_BG.copy(); d = ImageDraw.Draw(img)
    f = F(ANTON, 54)
    for i, s in enumerate(['100 % VEGANO:', 'ESTE LIBRO']):
        b = d.textbbox((0, 0), s, font=f, stroke_width=4)
        d.text((310 - (b[2] - b[0]) / 2 - b[0], 140 + i * 70 - b[1]), s, font=f, fill=YEL if i == 0 else WHT, stroke_width=4, stroke_fill=BLK)
    sc = 0.94 + 0.06 * ease(lt / 0.35)
    cw = int(380 * sc); ch = int(cw * COVER.height / COVER.width)
    cov = COVER.resize((cw, ch), Image.LANCZOS)
    x, y = int(310 - cw / 2), 300
    d.rectangle((x + 10, y + 10, x + cw + 10, y + ch + 10), fill=BLK); img.paste(cov, (x, y))
    ff = F(ANTON, 56); s = 'BÚSCALO EN AMAZON'; b = d.textbbox((0, 0), s, font=ff); w = b[2] - b[0]; by = 925
    d.rounded_rectangle((310 - w / 2 - 26, by - 14, 310 + w / 2 + 26, by + (b[3] - b[1]) + 18), 16, fill=YEL, outline=BLK, width=4)
    d.text((310 - w / 2 - b[0], by - b[1]), s, font=ff, fill=BLK)
    fp = F(POP, 32); s = 'Pasatiempos tóxicos Navidad'; b = d.textbbox((0, 0), s, font=fp)
    d.text((310 - (b[2] - b[0]) / 2 - b[0], 1012 - b[1]), s, font=fp, fill=WHT)
    return img

def frame(t):
    if t >= T_END_CLIP: return end_scene(t)
    for s0, s1, c0, z0, z1, cy in SEG:
        if s0 <= t < s1: break
    if c0 is None: return Image.new('RGB', (W, H), BLK)
    x = (t - s0) / (s1 - s0)
    img = zoom(cf(c0 + (t - s0)), z0 + (z1 - z0) * x, cy)
    d = ImageDraw.Draw(img)
    f1 = F(ANTON, 52); f2 = F(ANTON, 56)
    for txt, f, y, c in [('POV: DICES EN NOCHEBUENA', f1, 140, WHT), ('QUE TE HAS HECHO VEGANO', f2, 210, YEL)]:
        b = d.textbbox((0, 0), txt, font=f); d.text((310 - (b[2] - b[0]) / 2 - b[0], y - b[1]), txt, font=f, fill=c)
    if 0.7 <= t < 1.7:
        say(img, ['«¿Vegano?»'], 930, 0.7, t)
    elif 1.7 <= t < 3.35:
        say(img, ['«¿Eso qué es,', 'una enfermedad?»'], 930, 1.7, t)
    elif 3.35 <= t < 4.4:
        say(img, ['«Toma»'], 930, 3.5, t)
    elif 4.4 <= t < 6.55:
        say(img, ['«Esto es verdura, que', 'es de cerdo de bellota»'], 930, 4.4, t)
    elif t >= 6.55:
        label(img, [('Y NADIE', 62, WHT), ('LE LLEVÓ LA CONTRARIA', 46, YEL)], 945, 6.55, t)
    return img

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        for ts in sys.argv[1:]: frame(float(ts)).save(f'{D}/prev_{ts}.png')
        sys.exit()
    N = int(round(T_END * FPS))
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', f'{D}/video.mp4'], stdin=subprocess.PIPE)
    for i in range(N): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
