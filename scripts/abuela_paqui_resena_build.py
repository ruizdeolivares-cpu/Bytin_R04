import math, subprocess, os, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
W, H, FPS = 720, 1280, 30
D = os.path.dirname(os.path.abspath(__file__)); WK = os.path.dirname(D)
ANTON = f'{WK}/Anton.ttf'; POP = f'{WK}/fonts/pop/package/files/poppins-latin-800-normal.woff'
YEL, MAG, BLK, WHT, RED = (255, 238, 0), (232, 20, 120), (17, 17, 17), (255, 255, 255), (225, 30, 35)
F = lambda p, s: ImageFont.truetype(p, s)
COVER = Image.open(f'{WK}/img/portada.png').convert('RGB')
PAGES = {'cdk': Image.open(f'{WK}/img/cdk1_grid.png').convert('RGB'),
         'cripto': Image.open(f'{WK}/img/pg_cripto.png').convert('RGB'),
         'mist': Image.open(f'{WK}/img/pg_misterio.png').convert('RGB')}
SW, SH = 448, 672
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{WK}/clips/resena2.mp4', '-vf', 'fps=30', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
CLIP = np.frombuffer(raw, np.uint8).reshape(-1, SH, SW, 3)
T_CLIP, T_END = 11.8, 13.0
SC = 720 / SW; OY = 200  # clip scaled to 720x1080 at y=200
def ease(x): x = max(0, min(1, x)); return 1 - (1 - x) ** 3
def tc(d, cx, y, s, f, fill, stroke=0):
    b = d.textbbox((0, 0), s, font=f, stroke_width=stroke)
    d.text((cx - (b[2] - b[0]) / 2 - b[0], y - b[1]), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=BLK)
    return y + b[3] - b[1]
def book_overlay(fr):
    a = fr.astype(int)
    yel = (a[:, :, 0] > 170) & (a[:, :, 1] > 150) & (a[:, :, 2] < 110) & (a[:, :, 0] - a[:, :, 2] > 100)
    ys, xs = np.where(yel[250:, :]); ys = ys + 250
    if len(xs) < 500: return Image.fromarray(fr)
    x0, x1 = np.percentile(xs, 1), np.percentile(xs, 99); y0, y1 = np.percentile(ys, 1), np.percentile(ys, 99.5)
    x0, x1, y0, y1 = int(x0), int(x1) + 1, int(y0), int(y1) + 1
    reg = a[y0:y1, x0:x1]
    dark = reg.max(2) < 90
    yl = yel[y0:y1, x0:x1]
    m = (yl | dark).astype(np.uint8) * 255
    mask = Image.fromarray(m).filter(__import__('PIL.ImageFilter', fromlist=['x']).MaxFilter(3)).filter(__import__('PIL.ImageFilter', fromlist=['x']).MinFilter(3))
    cov = COVER.resize((x1 - x0, y1 - y0), Image.LANCZOS)
    img = Image.fromarray(fr).copy(); img.paste(cov, (x0, y0), mask)
    return img
def card(img, key, t0, t):
    p = PAGES[key]; sc = 0.85 + 0.15 * ease((t - t0) / 0.25)
    pw = int((430 if key == 'cdk' else 600) * sc); ph = int(pw * p.height / p.width)
    x, y = 310 - pw // 2, 1010 - ph
    d = ImageDraw.Draw(img); d.rectangle((x - 9, y - 9, x + pw + 9, y + ph + 9), fill=YEL, outline=BLK, width=4)
    img.paste(p.resize((pw, ph), Image.LANCZOS), (x, y))
def sub(img, lines):
    d = ImageDraw.Draw(img); f = F(ANTON, 52); y = 228
    for i, l in enumerate(lines):
        y = tc(d, 310, y, l, f, YEL if i == len(lines) - 1 and len(lines) > 1 else WHT, 6) + 10
SUBS = [(0.0, 1.8, ['«ME HAN REGALADO ESTO»'], None),
        (1.9, 5.1, ['«UN CUÑADOKU: UN SUDOKU', 'CON UNA MENTIRA»'], 'cdk'),
        (5.1, 7.3, ['«CRUCIGRAMAS,', 'MENSAJES EN CLAVE...»'], 'cripto'),
        (7.3, 9.8, ['«¿QUIÉN SE COMIÓ', 'EL ÚLTIMO TURRÓN?»'], 'mist'),
        (9.8, 10.8, ['«YO YA LO SÉ...»'], None),
        (10.8, 11.8, ['«...Y NO OS LO DIGO»'], None)]
def frame(t):
    if t < T_CLIP:
        fr = CLIP[min(int(t * FPS), len(CLIP) - 1)]
        b = book_overlay(fr).resize((720, 1080), Image.LANCZOS)
        img = Image.new('RGB', (W, H), BLK); img.paste(b, (0, OY)); d = ImageDraw.Draw(img)
        d.rectangle((0, 0, W, 200), fill=BLK)
        tc(d, 310, 138, 'LA ABUELA PAQUI RESEÑA:', F(ANTON, 50), YEL)
        for a0, a1, lines, key in SUBS:
            if a0 <= t < a1:
                pass
                sub(img, lines)
        return img
    lt = t - T_CLIP
    img = Image.new('RGB', (W, H), MAG); d = ImageDraw.Draw(img)
    cx, cy, R = W / 2, 560, 1600
    for i in range(18):
        a0, a1 = 2 * math.pi * i / 18, 2 * math.pi * (i + .5) / 18
        d.polygon([(cx, cy), (cx + R * math.cos(a0), cy + R * math.sin(a0)), (cx + R * math.cos(a1), cy + R * math.sin(a1))], fill=(200, 10, 100))
    tc(d, 310, 140, '¿QUIÉN CREES QUE FUE?', F(ANTON, 56), YEL, 4)
    cw = int(360 * (0.94 + 0.06 * ease(lt / 0.3))); ch = int(cw * COVER.height / COVER.width)
    x, y = 310 - cw // 2, 260; d.rectangle((x + 10, y + 10, x + cw + 10, y + ch + 10), fill=BLK); img.paste(COVER.resize((cw, ch), Image.LANCZOS), (x, y))
    ff = F(ANTON, 56); s = 'BÚSCALO EN AMAZON'; bb = d.textbbox((0, 0), s, font=ff); w = bb[2] - bb[0]; by = 880
    d.rounded_rectangle((310 - w / 2 - 26, by - 14, 310 + w / 2 + 26, by + (bb[3] - bb[1]) + 18), 16, fill=YEL, outline=BLK, width=4)
    d.text((310 - w / 2 - bb[0], by - bb[1]), s, font=ff, fill=BLK)
    tc(d, 310, 975, 'Pasatiempos tóxicos Navidad', F(POP, 32), WHT)
    return img
if __name__ == '__main__':
    if len(sys.argv) > 1:
        for ts in sys.argv[1:]: frame(float(ts)).save(f'{D}/prev_{ts}.png')
        sys.exit()
    N = int(round(T_END * FPS))
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', f'{D}/video.mp4'], stdin=subprocess.PIPE)
    for i in range(N): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
