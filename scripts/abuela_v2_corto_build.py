import math, subprocess, os, numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 720, 1280, 30
D = os.path.dirname(os.path.abspath(__file__)); WK = os.path.dirname(D)
ANTON = f'{WK}/Anton.ttf'; POP = f'{WK}/fonts/pop/package/files/poppins-latin-800-normal.woff'
YEL, MAG, BLK, WHT, RED = (255, 238, 0), (232, 20, 120), (17, 17, 17), (255, 255, 255), (225, 30, 35)
F = lambda p, s: ImageFont.truetype(p, s)

# clip a 30 fps en memoria
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{WK}/clips/clip1.mp4', '-vf', 'fps=30,scale=720:1280',
                      '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
CLIP = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
def cf(t): return Image.fromarray(CLIP[min(int(round(t * FPS)), len(CLIP) - 1)])

# tramos: (inicio salida, fin salida, inicio clip, zoom0, zoom1, centro y del zoom)
SEG = [
    (0.0, 2.0, 1.0, 1.06, 1.12, 600),
    (2.0, 2.1, None, 0, 0, 0),
    (2.1, 4.6, 5.0, 1.00, 1.05, 640),
    (4.6, 6.4, 8.0, 1.02, 1.10, 560),
]
T_END_CLIP, T_END = 6.4, 7.6

def zoom(img, z, cy):
    if z <= 1.0: return img
    cw, ch = W / z, H / z
    y0 = min(max(cy - ch / 2, 0), H - ch); x0 = (W - cw) / 2
    return img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.LANCZOS)

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

def counter(img, t):
    # "12" que baja a "11" en el golpe
    d = ImageDraw.Draw(img)
    n = '12' if t < 2.1 else '11'
    sc = pop(0.5 if t < 2.1 else 2.1, t)
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
END_BG = rays_bg((180, 15, 25), RED)
COVER = Image.open(f'{WK}/img/portada.png').convert('RGB')

def end_scene(t):
    lt = t - T_END_CLIP
    img = END_BG.copy(); d = ImageDraw.Draw(img)
    f = F(ANTON, 54)
    for i, s in enumerate(['NAVIDAD TÓXICA', 'EN UN LIBRO']):
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
    if t < 2.0:
        label(img, [('MI ABUELA HA CONTADO', 60, WHT), ('LOS TROZOS DE TURRÓN', 60, YEL)], 920, 0.0, t)
        if t >= 0.5: counter(img, t)
    elif t < 4.6:
        label(img, [('¡FALTA UNO!', 104, WHT)], 960, 2.1, t, bg=RED, shake=6 if t < 2.8 else 0)
        counter(img, t)
    else:
        label(img, [('Y TE ESTÁ', 66, WHT), ('MIRANDO A TI', 66, YEL)], 930, 4.6, t)
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
