import math, subprocess, os, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
W, H, FPS = 720, 1280, 30
D = os.path.dirname(os.path.abspath(__file__)); WK = os.path.dirname(D)
ANTON = f'{WK}/Anton.ttf'; POP = f'{WK}/fonts/pop/package/files/poppins-latin-800-normal.woff'
YEL, MAG, BLK, WHT, RED = (255, 238, 0), (232, 20, 120), (17, 17, 17), (255, 255, 255), (225, 30, 35)
F = lambda p, s: ImageFont.truetype(p, s)
PUZ = Image.open(sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].endswith('.png') else f'{WK}/img/cunadoku1.png').convert('RGB')
COVER = Image.open(f'{WK}/img/portada.png').convert('RGB')
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{WK}/clips/reto_intro_30.mp4', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
CLIP = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
T_INTRO, CD, T_END = 4.0, 8, 4.0 + 8 + 1.3
def ease(x): x = max(0, min(1, x)); return 1 - (1 - x) ** 3
def tc(d, cx, y, s, f, fill, stroke=0):
    b = d.textbbox((0, 0), s, font=f, stroke_width=stroke)
    d.text((cx - (b[2] - b[0]) / 2 - b[0], y - b[1]), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=BLK)
    return y + b[3] - b[1]
def box(d, cx, y, lines, bg):
    fs = [(s, F(ANTON, sz), c) for s, sz, c in lines]
    bs = [d.textbbox((0, 0), s, font=f) for s, f, c in fs]
    tw = max(b[2] - b[0] for b in bs); th = sum(b[3] - b[1] for b in bs) + 10 * (len(bs) - 1)
    d.rounded_rectangle((cx - tw / 2 - 24, y - 16, cx + tw / 2 + 24, y + th + 18), 16, fill=bg, outline=BLK, width=4)
    yy = y
    for (s, f, c), b in zip(fs, bs):
        d.text((cx - (b[2] - b[0]) / 2 - b[0], yy - b[1]), s, font=f, fill=c); yy += b[3] - b[1] + 10
def frame(t):
    if t < T_INTRO:
        img = Image.fromarray(CLIP[min(int(t * FPS), len(CLIP) - 1)]).copy(); d = ImageDraw.Draw(img)
        box(d, 310, 150, [('RETO: ENCUENTRA', 54, WHT), ('LA MENTIRA DEL CUÑADO', 56, YEL)], BLK)
        if t > 0.4:
            box(d, 310, 990, [('«TE APUESTO A QUE', 50, WHT), ('NO LA ENCUENTRAS»', 56, YEL)], RED)
        return img
    if t < T_INTRO + CD:
        lt = t - T_INTRO
        img = Image.new('RGB', (W, H), BLK); d = ImageDraw.Draw(img)
        for yy in range(0, H, 24):
            for xx in range(0, W, 24):
                d.ellipse((xx - 2, yy - 2, xx + 2, yy + 2), fill=(45, 10, 30))
        box(d, 310, 150, [('UN NÚMERO ES FALSO', 54, WHT), ('¿LO ENCUENTRAS EN 8 SEG?', 54, YEL)], RED)
        sc = 0.9 + 0.1 * ease(lt / 0.3)
        pw = int(440 * sc); ph = int(pw * PUZ.height / PUZ.width)
        p = PUZ.resize((pw, ph), Image.LANCZOS); x, y = 310 - pw // 2, 330
        d.rectangle((x - 10, y - 10, x + pw + 10, y + ph + 10), fill=YEL); img.paste(p, (x, y))
        n = CD - int(lt); urgent = n <= 3
        r = 78 + (10 * (1 - (lt % 1) * 4) if (lt % 1) < 0.25 else 0)
        cx, cy = 310, 330 + 499 + 108
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=RED if urgent else YEL, outline=BLK, width=5)
        frac = 1 - (lt / CD)
        d.arc((cx - r - 12, cy - r - 12, cx + r + 12, cy + r + 12), -90, -90 + 360 * frac, fill=WHT, width=8)
        f = F(ANTON, 96); b = d.textbbox((0, 0), str(n), font=f)
        d.text((cx - (b[2] - b[0]) / 2 - b[0], cy - (b[3] - b[1]) / 2 - b[1]), str(n), font=f, fill=WHT if urgent else BLK)
        return img
    lt = t - T_INTRO - CD
    img = Image.new('RGB', (W, H), MAG); d = ImageDraw.Draw(img)
    cxr, cyr, R = W / 2, 560, 1600
    for i in range(18):
        a0, a1 = 2 * math.pi * i / 18, 2 * math.pi * (i + .5) / 18
        d.polygon([(cxr, cyr), (cxr + R * math.cos(a0), cyr + R * math.sin(a0)), (cxr + R * math.cos(a1), cyr + R * math.sin(a1))], fill=(200, 10, 100))
    tc(d, 310, 140, '18 CUÑADOKUS MÁS', F(ANTON, 60), YEL, 4); tc(d, 310, 215, 'EN EL LIBRO', F(ANTON, 60), WHT, 4)
    cw = int(360 * (0.94 + 0.06 * ease(lt / 0.3))); ch = int(cw * COVER.height / COVER.width)
    x, y = 310 - cw // 2, 320; d.rectangle((x + 10, y + 10, x + cw + 10, y + ch + 10), fill=BLK); img.paste(COVER.resize((cw, ch), Image.LANCZOS), (x, y))
    box(d, 310, 905, [('BÚSCALO EN AMAZON', 56, BLK)], YEL)
    tc(d, 310, 1000, 'Pasatiempos tóxicos Navidad', F(POP, 32), WHT)
    return img
if __name__ == '__main__':
    if len(sys.argv) > 2:
        for ts in sys.argv[2:]: frame(float(ts)).save(f'{D}/prev_{ts}.png')
        sys.exit()
    N = int(round(T_END * FPS))
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', f'{D}/video.mp4'], stdin=subprocess.PIPE)
    for i in range(N): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
