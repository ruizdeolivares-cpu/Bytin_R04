"""Funciones comunes de montaje (canal Bityn y R-04). Ver PROMPT_MAESTRO.md.
BUILD = carpeta con fuentes y SFX descargados con:
  npm pack @fontsource/baloo-2 uisfx  (y descomprimir cada .tgz en una carpeta con su nombre)
"""
import os, subprocess, math, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIPS = os.path.join(REPO, 'kling', 'clips')
PERS = os.path.join(REPO, 'kling', 'personajes')
W, H, FPS = 720, 1280, 30
CX = 318  # centro de la zona segura (x 16..620)
NARANJA, AMARILLO, OSCURO, BLANCO = (255, 138, 0), (255, 214, 64), (35, 30, 45), (255, 255, 255)
AZUL, ROSA, VERDE = (60, 140, 255), (230, 60, 120), (40, 180, 90)

class Kit:
    def __init__(self, build):
        self.font_path = os.path.join(build, 'fontsource-baloo-2-5.3.0/package/files/baloo-2-latin-800-normal.woff')
        self.sfx = os.path.join(build, 'uisfx-0.4.0/package/sounds')
        self.segments, self.events = [], []
    def font(self, s): return ImageFont.truetype(self.font_path, s)
    def s(self, name): return os.path.join(self.sfx, name)

    def text(self, lines, size, stroke=9, maxw=560):
        s = size
        while True:
            f = self.font(s); ws = [f.getbbox(t, stroke_width=stroke)[2] for t, _ in lines]
            if max(ws) <= maxw or s < 30: break
            s -= 2
        lh = int(s * 1.08)
        img = Image.new('RGBA', (max(ws) + 20, lh * len(lines) + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
        for i, (t, c) in enumerate(lines):
            w = f.getbbox(t, stroke_width=stroke)[2]
            d.text(((img.width - w) // 2, 10 + i * lh), t, font=f, fill=c, stroke_width=stroke, stroke_fill=OSCURO)
        sh = Image.new('RGBA', img.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 110), mask=img.split()[3])
        sh = sh.filter(ImageFilter.GaussianBlur(6))
        out = Image.new('RGBA', (img.width + 12, img.height + 12), (0, 0, 0, 0))
        out.alpha_composite(sh, (10, 10)); out.alpha_composite(img, (0, 0)); return out

    def pill(self, text, size, bg, fg=BLANCO):
        f = self.font(size); bb = f.getbbox(text)
        img = Image.new('RGBA', (bb[2] + 44, int(size * 1.45)), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
        d.rounded_rectangle((0, 0, img.width - 1, img.height - 1), radius=img.height // 2, fill=bg, outline=OSCURO, width=5)
        d.text((22, int(size * 0.12)), text, font=f, fill=fg); return img

    def add(self, dur, fn): self.segments.append((dur, fn))
    def t0(self, k): return sum(d for d, _ in self.segments[:k])
    def sfx_at(self, t, name, vol=0.8): self.events.append((t, name, vol))

    def render(self, out):
        total = sum(d for d, _ in self.segments); tmpv, tmpa = out + '.v.mp4', out + '.a.wav'
        enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                                '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', tmpv], stdin=subprocess.PIPE)
        for dur, fn in self.segments:
            n = int(round(dur * FPS))
            for i in range(n): enc.stdin.write(fn(i, n).convert('RGB').tobytes())
        enc.stdin.close(); enc.wait()
        SR = 44100; N = int(total * SR); mix = np.zeros((N, 2), np.float32)
        for t, p, v in self.events:
            s = bip(SR) if p == 'bip' else load_audio(self.s(p) if not os.path.isabs(p) else p, SR)
            a = int(t * SR); b = min(N, a + len(s)); mix[a:b] += s[:b - a] * v
        mix *= 0.7 / max(1e-6, np.abs(mix).max())  # sin música; pico a -3 dB
        with wave.open(tmpa, 'wb') as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(mix, -1, 1) * 32767).astype('<i2').tobytes())
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmpv, '-i', tmpa, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '23',
                        '-maxrate', '1100k', '-bufsize', '2200k', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', '-ar', '44100',
                        '-movflags', '+faststart', '-shortest', out], check=True)
        os.remove(tmpv); os.remove(tmpa)
        print('OK', out, f'{total:.2f}s', os.path.getsize(out) // 1024, 'KB')

def load_audio(p, SR=44100):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).copy()

def bip(SR=44100):
    t = np.arange(int(SR * 0.22)) / SR; s = np.zeros_like(t)
    for a, b, fq in ((0, 0.08, 1320), (0.11, 0.2, 1760)):
        m = (t >= a) & (t < b); s[m] = np.sin(2 * np.pi * fq * t[m]) * np.hanning(m.sum())
    return np.stack([s, s], 1).astype(np.float32) * 0.5

def clip_frames(name, start, dur):
    p = os.path.join(CLIPS, name); n = int(round(dur * FPS))
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(start), '-i', p, '-t', str(dur + 0.2), '-vf', f'fps={FPS},scale={W}:{H}',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    fr = [Image.frombuffer('RGB', (W, H), raw[i*W*H*3:(i+1)*W*H*3]) for i in range(len(raw)//(W*H*3))]
    while len(fr) < n: fr.append(fr[-1])
    return fr[:n]

def zoom(img, z, cx=0.5, cy=0.5):
    w, h = img.size; nw, nh = w / z, h / z; x0 = (w - nw) * cx; y0 = (h - nh) * cy
    return img.crop((int(x0), int(y0), int(x0 + nw), int(y0 + nh))).resize((W, H), Image.LANCZOS)

def ease_pop(t, d=0.22):
    if t <= 0: return 0.0
    if t >= d: return 1.0
    x = t / d
    return 1 + 0.18 * math.sin(x * math.pi) * (1 - x) * 2 if x > 0.55 else x / 0.55 * 1.12

def place(frame, ov, cx, y, t, d=0.22):
    k = ease_pop(t, d)
    if k <= 0: return
    o = ov if abs(k - 1) < 1e-3 else ov.resize((max(1, int(ov.width * k)), max(1, int(ov.height * k))), Image.LANCZOS)
    x = int(cx - o.width / 2); x = max(16, min(x, 620 - o.width)) if o.width < 604 else 16
    frame.alpha_composite(o, (x, int(y + (ov.height - o.height) / 2)))

def fill_bg(img, blur=30, dark=0.25):
    """Fondo 720x1280 a partir de una imagen (recorte + desenfoque)."""
    r = max(W / img.width, H / img.height)
    b = img.resize((int(img.width * r) + 1, int(img.height * r) + 1)).crop((0, 0, W, H)).filter(ImageFilter.GaussianBlur(blur))
    return Image.blend(b.convert('RGB'), Image.new('RGB', (W, H), (20, 15, 40)), dark)

def shadowed(fr, im, x, y, alpha=120):
    sh = Image.new('RGBA', (im.width + 30, im.height + 30), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((15, 15, im.width + 15, im.height + 15), radius=18, fill=(0, 0, 0, alpha))
    fr.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)), (x - 5, y + 4)); fr.paste(im, (x, y))

def cierre(kit, dur=2.5, variante=0, color=(255, 214, 64), portada=None):
    """Cierre con portada + ¡Búscalo en Amazon! + edad. 3 variantes: NO repetir la misma en días seguidos.
    0 = fondo portada desenfocada · 1 = fondo de color liso con rayos y portada inclinada · 2 = degradado con portada pequeña + «enlace en el perfil»."""
    cov = Image.open(portada or os.path.join(REPO, 'libro', 'portada_frontal_720.png')).convert('RGB')  # libro 1: libro1/paginas/pag_001.jpg
    t1 = kit.text([('¡Búscalo', BLANCO), ('en Amazon!', AMARILLO)], 96); t2 = kit.pill('Para niños de 8 a 12 años', 36, NARANJA)
    if variante == 0:
        bg = fill_bg(cov, 25, 0.35); cw = 470
    elif variante == 1:
        bg = Image.new('RGB', (W, H), color); d = ImageDraw.Draw(bg); cx, cy = CX, 640
        for a in range(0, 360, 15):
            r = math.radians(a); r2 = math.radians(a + 7)
            d.polygon([(cx, cy), (cx + 1500 * math.cos(r), cy + 1500 * math.sin(r)), (cx + 1500 * math.cos(r2), cy + 1500 * math.sin(r2))], fill=tuple(min(255, c + 25) for c in color))
        cw = 440
    else:
        bg = Image.new('RGB', (W, H)); top, bot = (40, 30, 110), (255, 120, 60)
        for y in range(H):
            k = y / H; ImageDraw.Draw(bg).line((0, y, W, y), fill=tuple(int(top[j] * (1 - k) + bot[j] * k) for j in range(3)))
        cw = 400; t3 = kit.pill('👉 Enlace en el perfil'.replace('👉 ', ''), 34, ROSA)
    chh = int(cov.height * cw / cov.width); covs = cov.resize((cw, chh), Image.LANCZOS)
    if variante == 1: covs = covs.convert('RGBA').rotate(-4, expand=True, resample=Image.BICUBIC)
    y0 = 330
    def fn(i, n):
        t = i / FPS; fr = bg.copy().convert('RGBA'); k = ease_pop(t, 0.3)
        if k > 0:
            c = covs.resize((max(1, int(covs.width * k)), max(1, int(covs.height * k))))
            x, y = CX - c.width // 2, y0 + (covs.height - c.height) // 2
            if c.mode == 'RGBA': fr.alpha_composite(c, (x, y))
            else: shadowed(fr, c, x, y)
        place(fr, t1, CX, 80, t - 0.15); place(fr, t2, CX, y0 + covs.height + 14, t - 0.35)
        if variante == 2: place(fr, t3, CX, y0 + covs.height + 80, t - 0.5)
        return fr
    t = kit.t0(len(kit.segments)); kit.add(dur, fn)
    kit.sfx_at(t, 'arcade/swipe.mp3', 0.7); kit.sfx_at(t + 0.2, ['arcade/achievement.mp3', 'arcade/reward.mp3', 'arcade/level-up.mp3'][variante], 0.9)

def hoja(video, out, ts):
    """Hoja de revisión con líneas de zona segura (y=1047, x=620) y recorte 3:4."""
    ims = []
    for t in ts:
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', video, '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True).stdout
        import io; im = Image.open(io.BytesIO(raw)).convert('RGB'); d = ImageDraw.Draw(im)
        d.line((620, 0, 620, H), fill='red', width=3); d.line((0, 1047, W, 1047), fill='red', width=3); d.rectangle((0, 160, W - 1, 1120), outline='lime', width=3)
        ims.append(im.resize((240, 427)))
    cols = 5; s = Image.new('RGB', (cols * 250, ((len(ims) + cols - 1) // cols) * 437), 'black')
    for i, im in enumerate(ims): s.paste(im, ((i % cols) * 250, (i // cols) * 437))
    s.save(out)
