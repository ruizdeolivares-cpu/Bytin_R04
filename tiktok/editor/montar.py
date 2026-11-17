#!/usr/bin/env python3
"""Montador de cortos de Bityn y R-04 para TikTok.

Uso:  python3 montar.py guiones/corto-01.json
Genera un MP4 1080x1920 con textos, efectos, música opcional y cierre de la serie.
"""
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
FUENTE = '/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'
W, H, FPS = 1080, 1920, 30
COL = {'b': 'white', 'a': '#FFD43B', 'n': '#FF9A1F'}  # blanco, amarillo, naranja
FONDO = '#FCF6E6'


def sh(*a):
    subprocess.run(a, check=True)


def ruta(p):
    return p if os.path.isabs(p) else os.path.join(AQUI, p)


def capa_texto(lineas, y, out):
    """lineas: [[texto, color(b/a/n), tamaño], ...]"""
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for t, c, s in lineas:
        f = ImageFont.truetype(FUENTE, s)
        while d.textlength(t, font=f) > W - 120:  # que nunca se salga
            s -= 4
            f = ImageFont.truetype(FUENTE, s)
        x = (W - d.textlength(t, font=f)) / 2
        d.text((x, y), t, font=f, fill=COL.get(c, c), stroke_width=max(8, s // 9), stroke_fill='black')
        y += int(s * 1.18)
    im.save(out)


def fotograma_imagen(src, out, centro_y=820):
    """Ilustración horizontal o vertical sobre fondo desenfocado, a 1.15x para poder hacer zoom."""
    k = 1.15
    CW, CH = int(W * k), int(H * k)
    img = Image.open(ruta(src)).convert('RGB')
    bg = img.copy()
    r = max(CW / bg.width, CH / bg.height)
    bg = bg.resize((int(bg.width * r) + 1, int(bg.height * r) + 1)).crop((0, 0, CW, CH))
    bg = bg.filter(ImageFilter.GaussianBlur(40))
    bg = Image.blend(bg, Image.new('RGB', bg.size, FONDO), 0.35)
    r = min(CW * 0.98 / img.width, CH * 0.62 / img.height)
    fg = img.resize((int(img.width * r), int(img.height * r)), Image.LANCZOS)
    sombra = Image.new('RGBA', (fg.width + 60, fg.height + 60), (0, 0, 0, 0))
    ImageDraw.Draw(sombra).rounded_rectangle((30, 40, fg.width + 30, fg.height + 40), 30, fill=(0, 0, 0, 110))
    sombra = sombra.filter(ImageFilter.GaussianBlur(18))
    cy = int(centro_y * k)
    bg.paste(sombra, ((CW - fg.width) // 2 - 30, cy - fg.height // 2 - 30), sombra)
    bg.paste(fg, ((CW - fg.width) // 2, cy - fg.height // 2))
    bg.save(out)


def fotograma_cierre(out_bg, out_txt):
    """Cierre de la serie: portadas disponibles + títulos."""
    bg = Image.new('RGB', (W, H), FONDO)
    portadas = [p for p in ('assets/portada-mi-primer-dinero.png', 'assets/portada-mi-goloso-negocio.png')
                if os.path.exists(ruta(p))]
    alto = 820 if len(portadas) == 1 else 640
    ims = []
    for p in portadas:
        im = Image.open(ruta(p)).convert('RGB')
        ims.append(im.resize((int(im.width * alto / im.height), alto), Image.LANCZOS))
    total = sum(i.width for i in ims) + 50 * (len(ims) - 1)
    x, y = (W - total) // 2, 700
    for i in ims:
        sm = Image.new('RGBA', (i.width + 80, i.height + 80), (0, 0, 0, 0))
        ImageDraw.Draw(sm).rectangle((40, 50, i.width + 40, i.height + 50), fill=(0, 0, 0, 120))
        sm = sm.filter(ImageFilter.GaussianBlur(20))
        bg.paste(sm, (x - 40, y - 40), sm)
        bg.paste(i, (x, y))
        x += i.width + 50
    bg.save(out_bg)
    capa_texto([['La serie de libros', 'b', 66], ['BITYN Y R-04', 'a', 128],
                ['1. Mi primer dinero', 'b', 70], ['2. Mi goloso negocio', 'b', 70]], 150, out_txt)
    # Línea final bajo las portadas, por encima de la zona de botones de TikTok
    im = Image.open(out_txt)
    capa_texto([['Búscalos en Amazon', 'n', 76]], 1400 if len(portadas) == 2 else 1560, out_txt + '.2.png')
    im.alpha_composite(Image.open(out_txt + '.2.png'))
    im.save(out_txt)


def segmento(esc, tmp, i):
    out = f'{tmp}/s{i}.mp4'
    dur = esc['dur']
    txt = f'{tmp}/t{i}.png'
    if esc.get('texto'):
        capa_texto(esc['texto'], esc.get('y', 1300), txt)
    else:
        Image.new('RGBA', (W, H), (0, 0, 0, 0)).save(txt)
    n = int(dur * FPS)
    if esc['tipo'] == 'clip':
        entrada = ['-ss', str(esc.get('ss', 0)), '-t', str(dur), '-i', ruta(esc['src'])]
        base = f'[0:v]scale={W}:{H}:flags=lanczos,fps={FPS},setsar=1[v]'
    else:
        f = f'{tmp}/f{i}.png'
        if esc['tipo'] == 'cierre':
            fotograma_cierre(f, txt)
        else:
            fotograma_imagen(esc['src'], f, esc.get('centro_y', 820))
        entrada = ['-loop', '1', '-t', str(dur), '-i', f]
        z = "1.15-0.0012*on" if esc.get('mov') == 'alejar' else "1+0.0012*on"
        base = (f"[0:v]zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
                f":d={n}:s={W}x{H}:fps={FPS},setsar=1[v]")
    sh('ffmpeg', '-v', 'error', '-y', *entrada, '-loop', '1', '-t', str(dur), '-i', txt,
       '-filter_complex', f"{base};[1:v]format=rgba,fade=in:st=0.25:d=0.2:alpha=1[t];"
       f"[v][t]overlay=0:0:shortest=1,format=yuv420p",
       '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-r', str(FPS), out)
    return out


def efectos(tmp, tiempos, total):
    """whoosh en los cortes, pop en cada texto, ding opcional."""
    sh('ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i',
       'anoisesrc=d=0.35:c=pink:a=0.5,highpass=f=400,lowpass=f=4000,afade=in:d=0.15,afade=out:st=0.15:d=0.2',
       f'{tmp}/wh.wav')
    sh('ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'sine=f=600:d=0.08,afade=out:d=0.08,volume=0.5', f'{tmp}/pop.wav')
    sh('ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'sine=f=1760:d=0.6,afade=out:d=0.6,volume=0.35', f'{tmp}/ding.wav')
    ev = []
    for k, (ini, esc) in enumerate(tiempos):
        if k:
            ev.append(('wh', ini - 0.15))
        if esc.get('texto'):
            ev.append(('pop', ini + 0.25))
        if esc.get('ding'):
            ev += [('ding', ini + 0.4), ('ding', ini + 0.7)]
    args, fil, mix = [], '', ''
    for j, (s, t) in enumerate(ev):
        ms = int(max(t, 0) * 1000)
        args += ['-i', f'{tmp}/{s}.wav']
        fil += f'[{j}:a]adelay={ms}|{ms}[a{j}];'
        mix += f'[a{j}]'
    out = f'{tmp}/sfx.wav'
    sh('ffmpeg', '-v', 'error', '-y', *args, '-filter_complex',
       f'{fil}{mix}amix=inputs={len(ev)}:normalize=0,apad,atrim=0:{total},aformat=channel_layouts=stereo', out)
    return out


def duracion_clip(src):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', ruta(src)],
                       capture_output=True, text=True, check=True)
    return float(r.stdout)


def al_ritmo(spec, escenas):
    """Ajusta cada corte al golpe (beat) más cercano de la música."""
    info = json.load(open(ruta('musica/beats.json'))).get(os.path.basename(spec['musica']))
    if not info:
        return
    ini = spec.setdefault('musica_inicio', info['inicio_energia'])
    beats = [b - ini for b in info['beats'] if b >= ini - 0.01]
    t = 0.0
    for e in escenas:
        maxd = duracion_clip(e['src']) - e.get('ss', 0) - 0.05 if e['tipo'] == 'clip' else 99
        maxd = min(maxd, e.get('max', 99))
        objetivo = t + e['dur']
        cand = [b for b in beats if b - t >= 1.5 and b - t <= maxd]
        if cand:
            fin = min(cand, key=lambda b: abs(b - objetivo))
            e['dur'] = round(fin - t, 3)
        t += e['dur']


def main(spec_path):
    spec = json.load(open(spec_path))
    escenas = spec['escenas'] + ([{'tipo': 'cierre', 'dur': spec.get('dur_cierre', 4.5)}] if spec.get('cierre', True) else [])
    if spec.get('musica') and spec.get('al_ritmo', True):
        al_ritmo(spec, escenas)
    with tempfile.TemporaryDirectory() as tmp:
        segs, tiempos, t = [], [], 0.0
        for i, e in enumerate(escenas):
            segs.append(segmento(e, tmp, i))
            tiempos.append((t, e))
            t += e['dur']
        open(f'{tmp}/l.txt', 'w').write(''.join(f"file '{s}'\n" for s in segs))
        sh('ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{tmp}/l.txt', '-c', 'copy', f'{tmp}/v.mp4')
        sfx = efectos(tmp, tiempos, t)
        audio = sfx
        if spec.get('musica'):
            # música normalizada para TikTok (~-15 LUFS), fundido final, efectos por debajo
            sh('ffmpeg', '-v', 'error', '-y', '-ss', str(spec.get('musica_inicio', 0)), '-i', ruta(spec['musica']), '-i', sfx,
               '-filter_complex', f"[0:a]atrim=0:{t},asetpts=PTS-STARTPTS,loudnorm=I=-15:TP=-1.5,"
               f"afade=in:d=0.05,afade=out:st={t-1.0}:d=1.0,aformat=sample_rates=44100:channel_layouts=stereo[m];"
               f"[1:a]volume={spec.get('sfx_vol', 0.6)},aformat=sample_rates=44100:channel_layouts=stereo[s];"
               f"[m][s]amix=inputs=2:normalize=0,alimiter=limit=0.95,atrim=0:{t}",
               f'{tmp}/mix.wav')
            audio = f'{tmp}/mix.wav'
        out = ruta(spec['salida'])
        os.makedirs(os.path.dirname(out), exist_ok=True)
        sh('ffmpeg', '-v', 'error', '-y', '-i', f'{tmp}/v.mp4', '-i', audio, '-c:v', 'copy',
           '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', out)
    print(f'OK {out} ({t:.1f} s)')


if __name__ == '__main__':
    main(sys.argv[1])
