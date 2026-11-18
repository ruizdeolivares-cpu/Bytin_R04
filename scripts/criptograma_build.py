import math, subprocess, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 720, 1280, 30
D = os.path.dirname(os.path.abspath(__file__))
WK = os.path.dirname(D)
ANTON = f'{WK}/Anton.ttf'
POP = f'{WK}/fonts/pop/package/files/poppins-latin-800-normal.woff'
POP7 = f'{WK}/fonts/pop/package/files/poppins-latin-700-normal.woff'
YEL, MAG, BLK, WHT = (255, 238, 0), (232, 20, 120), (17, 17, 17), (255, 255, 255)
F = lambda p, s: ImageFont.truetype(p, s)

# ---------- datos del criptograma (pág. 16) ----------
ROWS = [  # (letra real, número)  None = espacio ; '.' = punto
    [('E',27),('L',7),None,('C',13),('U',2),('Ñ',25),('A',17),('D',10),('O',11)],
    [('N',6),('U',2),('N',6),('C',13),('A',17),None,('S',12),('E',27)],
    [('E',27),('Q',16),('U',2),('I',20),('V',15),('O',11),('C',13),('A',17),'.'],
    [('S',12),('O',11),('L',7),('O',11),None,('T',19),('I',20),('E',27),('N',6),('E',27)],
    [('D',10),('A',17),('T',19),('O',11),('S',12)],
    [('A',17),('L',7),('T',19),('E',27),('R',23),('N',6),('A',17),('T',19),('I',20),('V',15),('O',11),('S',12),'.'],
]
# revelados: (tiempo, número)
REVEAL = [(2.5,27),(3.0,11),(3.5,7),(4.5,13),(5.5,2),(6.5,25),(7.0,17),(7.5,10),(8.0,6)]
GIVEN = {27, 11}
T_HOOK, T_GRID_END, T_TONI_END, T_END = 2.0, 11.0, 13.0, 15.3

def ease(x): x = max(0, min(1, x)); return 1 - (1 - x) ** 3
def pop(t0, t, dur=0.25):
    x = (t - t0) / dur
    if x < 0: return 0
    if x >= 1: return 1
    return 1 + 0.35 * math.sin(x * math.pi) * (1 - x) + (ease(x) - 1)

def text_c(d, cx, y, s, font, fill, stroke=0, sfill=BLK):
    b = d.textbbox((0, 0), s, font=font, stroke_width=stroke)
    d.text((cx - (b[2] - b[0]) / 2 - b[0], y - b[1]), s, font=font, fill=fill, stroke_width=stroke, stroke_fill=sfill)
    return y + b[3] - b[1]

def wrap(d, s, font, maxw):
    out, cur = [], ''
    for w in s.split():
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: out.append(cur); cur = w
    out.append(cur); return out

def bubble(img, x, y, w, lines, font, tail='down'):
    d = ImageDraw.Draw(img)
    lh = font.size + 10; h = lh * len(lines) + 34
    d.rounded_rectangle((x + 6, y + 6, x + w + 6, y + h + 6), 26, fill=BLK)
    d.rounded_rectangle((x, y, x + w, y + h), 26, fill=WHT, outline=BLK, width=5)
    if tail == 'down':
        d.polygon([(x + 70, y + h - 3), (x + 120, y + h - 3), (x + 60, y + h + 46)], fill=WHT, outline=None)
        d.line([(x + 70, y + h), (x + 60, y + h + 46), (x + 120, y + h)], fill=BLK, width=5)
    for i, l in enumerate(lines):
        text_c(d, x + w / 2, y + 17 + i * lh, l, font, BLK)
    return h

# ---------- fondos ----------
def dark_bg():
    im = Image.new('RGB', (W, H), BLK); d = ImageDraw.Draw(im)
    for yy in range(0, H, 22):
        for xx in range(0, W, 22):
            o = 11 if (yy // 22) % 2 else 0
            r = 2 + 3 * (yy / H)
            d.ellipse((xx + o - r, yy - r, xx + o + r, yy + r), fill=(70, 12, 45))
    return im
BG = dark_bg()

def rays_bg(c1, c2, n=18):
    im = Image.new('RGB', (W, H), c1); d = ImageDraw.Draw(im)
    cx, cy, R = W / 2, 560, 1600
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + .5) / n
        d.polygon([(cx, cy), (cx + R * math.cos(a0), cy + R * math.sin(a0)), (cx + R * math.cos(a1), cy + R * math.sin(a1))], fill=c2)
    return im
END_BG = rays_bg((205, 10, 100), MAG)

TONI = Image.open(f'{WK}/img/inicio_cunado.png').convert('RGB')
COVER = Image.open(f'{WK}/img/portada.png').convert('RGB')

def toni_frame(z, cx, cy):
    # z: zoom sobre 1080x1920 -> 720x1280
    s = (W / TONI.width) * z
    cw, ch = W / s, H / s
    x0 = min(max(cx - cw / 2, 0), TONI.width - cw); y0 = min(max(cy - ch / 2, 0), TONI.height - ch)
    return TONI.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.LANCZOS)

# ---------- rejilla ----------
SLOT, BW, BH = 49, 45, 56
GY0, RH = 338, 100
f_let = F(ANTON, 44); f_num = F(POP7, 22)

def known_at(t):
    k = {}
    for tt, n in REVEAL:
        if t >= tt: k[n] = tt
    return k

def draw_grid(img, t, blink=False):
    d = ImageDraw.Draw(img)
    k = known_at(t)
    for r, row in enumerate(ROWS):
        n = len(row); x0 = 310 - (n * SLOT - 4) / 2; y = GY0 + r * RH
        for i, c in enumerate(row):
            x = x0 + i * SLOT
            if c is None: continue
            if c == '.':
                d.ellipse((x + 2, y + BH - 14, x + 14, y + BH - 2), fill=YEL); continue
            L, num = c
            unknown = num not in k
            fillc = WHT
            if blink and unknown and int(t * 4) % 2 == 0: fillc = (255, 200, 225)
            d.rectangle((x, y, x + BW, y + BH), fill=fillc, outline=YEL if num in GIVEN else BLK, width=3)
            text_c(d, x + BW / 2, y + BH + 6, str(num), f_num, WHT)
            if not unknown:
                sc = pop(k[num], t)
                if sc <= 0: continue
                col = BLK if num in GIVEN else MAG
                fs = max(8, int(44 * sc))
                ff = F(ANTON, fs)
                b = d.textbbox((0, 0), L, font=ff)
                d.text((x + BW / 2 - (b[2] - b[0]) / 2 - b[0], y + BH / 2 - (b[3] - b[1]) / 2 - b[1]), L, font=ff, fill=col)

f_t1 = F(ANTON, 66); f_t2 = F(POP, 30); f_pill = F(ANTON, 70); f_cap = F(POP, 36)

def grid_scene(t):
    img = BG.copy(); d = ImageDraw.Draw(img)
    text_c(d, 310, 150, 'CRIPTOGRAMA CUÑADIL', f_t1, YEL)
    text_c(d, 310, 240, 'Mismo número = misma letra', F(POP, 34), WHT)
    draw_grid(img, t, blink=t >= 9.5)
    # píldora inferior
    cur = None
    for tt, n in REVEAL:
        if t >= tt: cur = (tt, n)
    if t < 3.5:
        msg, sub = 'TE REGALAN 2 LETRAS', None
        if t >= 2.5: msg = 'E y O: GRATIS'
    elif t < 8.5:
        L = [c for row in ROWS for c in row if c and c != '.' and c[1] == cur[1]][0][0]
        msg = f'{cur[1]} = {L}'
    elif t < 9.5:
        msg = '¿YA LA VES?'
    else:
        msg = 'TE FALTAN 6 LETRAS'
    tt0 = cur[0] if (cur and 3.5 <= t < 8.5) else (8.5 if 8.5 <= t < 9.5 else (9.5 if t >= 9.5 else 2.0 if t < 2.5 else 2.5))
    sc = pop(tt0, t)
    ff = F(ANTON, max(10, int((70 if len(msg) < 10 else 56) * sc)))
    b = d.textbbox((0, 0), msg, font=ff)
    w, h = b[2] - b[0], b[3] - b[1]
    cx, cy = 310, 990
    d.rounded_rectangle((cx - w / 2 - 26, cy - h / 2 - 18, cx + w / 2 + 26, cy + h / 2 + 18), 18, fill=MAG if t < 8.5 else YEL, outline=BLK, width=4)
    d.text((cx - w / 2 - b[0], cy - h / 2 - b[1]), msg, font=ff, fill=WHT if t < 8.5 else BLK)
    return img

def hook_scene(t):
    z = 1.32 + 0.10 * (t / T_HOOK)
    img = toni_frame(z, 470, 760)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, 410), fill=BLK)
    y = text_c(d, 310, 140, 'TU CUÑADO HA ESCRITO', F(ANTON, 58), WHT)
    y = text_c(d, 310, y + 16, 'SU FRASE FAVORITA', F(ANTON, 74), YEL)
    text_c(d, 310, y + 14, 'EN CLAVE', F(ANTON, 74), MAG)
    if t >= 0.6:
        sc = max(0.05, pop(0.6, t))
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        lines = ['«Esto lo descifro yo', 'sin mirar, fíjate.»']
        bubble(lay, 40, 840, 540, lines, F(POP, 36))
        if sc < 1:
            lay = lay.resize((int(W * sc), int(H * sc)))
            tmp = Image.new('RGBA', (W, H), (0, 0, 0, 0)); tmp.paste(lay, (int(310 - 310 * sc), int(950 - 950 * sc))); lay = tmp
        img.paste(lay, (0, 0), lay)
    return img

def toni_scene(t):
    lt = t - T_GRID_END
    img = toni_frame(1.3 + 0.08 * lt / 2, 415, 700)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, 330), fill=BLK)
    y = text_c(d, 310, 145, '¿LA SACAS', F(ANTON, 76), YEL)
    text_c(d, 310, y + 14, 'ANTES QUE ÉL?', F(ANTON, 76), WHT)
    if lt >= 0.5:
        sc = max(0.05, pop(T_GRID_END + 0.5, t))
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        bubble(lay, 40, 965, 540, ['Comenta la frase', 'entera abajo'], F(POP, 38))
        if sc < 1:
            lay = lay.resize((int(W * sc), int(H * sc)))
            tmp = Image.new('RGBA', (W, H), (0, 0, 0, 0)); tmp.paste(lay, (int(310 - 310 * sc), int(950 - 950 * sc))); lay = tmp
        img.paste(lay, (0, 0), lay)
    return img

def end_scene(t):
    lt = t - T_TONI_END
    img = END_BG.copy(); d = ImageDraw.Draw(img)
    text_c(d, 310, 145, 'LA SOLUCIÓN, EN EL LIBRO', F(ANTON, 52), YEL, stroke=3)
    sc = 0.94 + 0.06 * ease(lt / 0.35)
    cw = int(400 * sc); ch = int(cw * COVER.height / COVER.width)
    cov = COVER.resize((cw, ch), Image.LANCZOS)
    x, y = int(310 - cw / 2), int(560 - ch / 2) + 10
    d.rectangle((x + 10, y + 10, x + cw + 10, y + ch + 10), fill=BLK)
    img.paste(cov, (x, y))
    by = 905
    ff = F(ANTON, 56); s = 'BÚSCALO EN AMAZON'; b = d.textbbox((0, 0), s, font=ff); w = b[2] - b[0]
    d.rounded_rectangle((310 - w / 2 - 26, by - 14, 310 + w / 2 + 26, by + (b[3] - b[1]) + 18), 16, fill=YEL, outline=BLK, width=4)
    d.text((310 - w / 2 - b[0], by - b[1]), s, font=ff, fill=BLK)
    text_c(d, 310, 1000, 'Pasatiempos tóxicos Navidad', F(POP, 34), WHT)
    return img

def frame(t):
    if t < T_HOOK: return hook_scene(t)
    if t < T_GRID_END: return grid_scene(t)
    if t < T_TONI_END: return toni_scene(t)
    return end_scene(t)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        for ts in sys.argv[1:]:
            frame(float(ts)).save(f'{D}/prev_{ts}.png')
        sys.exit()
    N = int(round(T_END * FPS))
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', f'{D}/video.mp4'], stdin=subprocess.PIPE)
    for i in range(N):
        p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
