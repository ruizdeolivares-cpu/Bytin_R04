# Monta «El asesinato del último turrón» (Navidad V01)
import os, sys, subprocess, numpy as np, wave
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S=sys.argv[1]; C=S+'/v01/clips/'; B=S+'/v01/build/'; os.makedirs(B,exist_ok=True)
FB=ImageFont.truetype(S+'/fonts/fontsource-baloo-2-5.3.0/package/files/baloo-2-latin-800-normal.woff',58)
FA=lambda n: ImageFont.truetype(S+'/fonts/fontsource-anton-5.3.0/package/files/anton-latin-400-normal.woff',n)
W,H=720,1280; YEL=(255,226,0); PINK=(255,45,150)
def run(c): subprocess.run(c,shell=True,check=True,stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
def sub_png(text,keys,path,y=900,top=None):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    if top:
        d.text((330,150),top,font=FA(64),fill=YEL,anchor='mm',stroke_width=6,stroke_fill='black')
    if text:
        words=text.split(); lines=[]; cur=''
        for w in words:
            t=(cur+' '+w).strip()
            if d.textlength(t,font=FB)>540 and cur: lines.append(cur); cur=w
            else: cur=t
        lines.append(cur)
        yy=y-len(lines)*66//2
        for ln in lines:
            # draw word by word to colour keywords
            x=330-d.textlength(ln,font=FB)/2
            for w in ln.split(' '):
                col=YEL if any(k in w.upper() for k in keys) else 'white'
                d.text((x,yy),w,font=FB,fill=col,stroke_width=5,stroke_fill='black'); x+=d.textlength(w+' ',font=FB)
            yy+=66
    im.save(path)
# segments: (video_src, vstart, vend, audio_src, astart, text, keys, top, zoom)
SEG=[('bf4f5ec4-Q8MDc',0.0,2.35,'f6768ec8-UwZiS',0.0,'¡¡HAN MATADO AL TURRÓN!!',['TURRÓN','MATADO'],'NOCHEBUENA · 23:30',False),
('f6768ec8-UwZiS',2.95,4.85,None,None,'¡Aquí hay un ladrón!',['LADRÓN'],None,False),
('f1dc42b0-tjKp3',0.72,4.12,None,None,'Yo ya dije que no lo escondieras en la despensa.',['DESPENSA'],None,False),
('6f2fceba-O41Tv',0.72,3.18,None,None,'¿Qué turrón? Yo estaba con el móvil.',['MÓVIL','TURRÓN'],None,False),
('20146bec-bsRdy',0.45,4.1,None,None,'Tampoco vamos a montar un juicio por un trozo de almendra.',['JUICIO','ALMENDRA'],None,False),
('452bff6a-IWGDR',0.72,3.72,None,None,'Tranquilos. Soy experto en investigación criminal.',['INVESTIGACIÓN','CRIMINAL'],None,False),
('7394ef14-gqFTY',0.80,3.38,None,None,'Tú no has encontrado ni trabajo.',['TRABAJO'],None,False),
('2e1eb934-hirVV',0.85,2.15,None,None,'¡PROTESTO!',['PROTESTO'],None,False),
('2e1eb934-hirVV',4.0,4.9,'SILENT',None,'',[],None,False)]
parts=[]
for k,(v,a,b,asrc,ast,txt,keys,top,z) in enumerate(SEG):
    png=B+f's{k}.png'; sub_png(txt,keys,png,top=top)
    dur=b-a; out=B+f'p{k}.mp4'
    if asrc=='SILENT':
        aud=f'-f lavfi -t {dur} -i anullsrc=r=48000:cl=stereo'; amap='-map 2:a'
    elif asrc:
        aud=f'-ss {ast} -t {dur} -i {C}{asrc}.mp4'; amap='-map 2:a'
    else:
        aud=''; amap='-map 0:a'
    run(f'ffmpeg -y -ss {a} -t {dur} -i {C}{v}.mp4 -i {png} {aud} -filter_complex "[0:v]scale=720:1280,fps=30[v0];[v0][1:v]overlay=0:0[v]" -map "[v]" {amap} -c:v libx264 -preset veryfast -crf 20 -c:a aac -ar 48000 -ac 2 -t {dur} {out}')
    parts.append(out)
# BOARD
board=Image.new('RGB',(W,H),YEL); d=ImageDraw.Draw(board)
for y in range(0,H,22):
    for x in range((y//22%2)*11,W,22): d.ellipse([x-3,y-3,x+3,y+3],fill=(245,205,0))
F='libro_navidad/fichas/'
cards=[('abuela_paqui','ABUELA PAQUI'),('mari_carmen','MARI CARMEN'),('toni','TONI'),('ivan','IVÁN'),(None,'TÍA ENCARNA'),(None,'CHISPAS')]
pos=[(80,250),(360,250),(80,510),(360,510),(80,770),(360,770)]
cent=[]
for (n,lab),(x,y) in zip(cards,pos):
    card=Image.new('RGB',(220,240),'white'); cd=ImageDraw.Draw(card)
    if n:
        im=Image.open(F+n+'.png').convert('RGB'); w,h=im.size; face=im.crop((int(w*0.18),int(h*0.04),int(w*0.82),int(h*0.04)+int(w*0.64)))
        card.paste(face.resize((200,175)),(10,10))
    else:
        cd.rectangle([10,10,210,185],fill=(40,40,40)); cd.text((110,98),'?',font=FA(130),fill=YEL,anchor='mm')
    cd.text((110,212),lab,font=ImageFont.truetype(S+'/fonts/fontsource-baloo-2-5.3.0/package/files/baloo-2-latin-800-normal.woff',30),fill='black',anchor='mm')
    card=card.rotate((-4,3,-2,4,3,-3)[len(cent)],expand=True,fillcolor=YEL)
    board.paste(card,(x,y)); cent.append((x+110,y+18))
for i in range(len(cent)-1):
    d.line([cent[i],cent[i+1]],fill=(200,0,0),width=4)
for c_ in cent: d.ellipse([c_[0]-9,c_[1]-9,c_[0]+9,c_[1]+9],fill=(220,0,0),outline='black',width=2)
d.text((330,120),'6 SOSPECHOSOS',font=FA(76),fill=PINK,anchor='mm',stroke_width=6,stroke_fill='black')
d.text((330,195),'4 PISTAS · 1 FAMILIA ENCERRADA',font=FA(40),fill='white',anchor='mm',stroke_width=5,stroke_fill='black')
board.save(B+'board.png')
run(f'ffmpeg -y -loop 1 -t 4.2 -i {B}board.png -f lavfi -t 4.2 -i anullsrc=r=48000:cl=stereo -filter_complex "[0:v]scale=1440:2560,zoompan=z=\'1+0.06*on/126\':x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':d=126:s=720x1280:fps=30[v]" -map "[v]" -map 1:a -c:v libx264 -preset veryfast -crf 20 -c:a aac -ar 48000 -ac 2 -t 4.2 {B}board.mp4')
parts.append(B+'board.mp4')
# COVER
cov=Image.new('RGB',(W,H),YEL); d=ImageDraw.Draw(cov)
for y in range(0,H,22):
    for x in range((y//22%2)*11,W,22): d.ellipse([x-3,y-3,x+3,y+3],fill=(245,205,0))
p=Image.open('libro_navidad/portada.png').convert('RGB'); ph=600; p=p.resize((int(p.width*ph/p.height),ph))
cov.paste(p,(330-p.width//2,290))
d.text((330,170),'¿QUIÉN HA SIDO?',font=FA(84),fill=PINK,anchor='mm',stroke_width=7,stroke_fill='black')
d.text((330,245),'LO RESUELVES TÚ',font=FA(46),fill='white',anchor='mm',stroke_width=5,stroke_fill='black')
d.text((330,935),'PASATIEMPOS TÓXICOS',font=FA(52),fill='black',anchor='mm')
d.text((330,985),'EDICIÓN NAVIDAD · EN AMAZON',font=FA(34),fill=PINK,anchor='mm',stroke_width=3,stroke_fill='black')
cov.save(B+'cover.png')
run(f'ffmpeg -y -loop 1 -t 3.8 -i {B}cover.png -f lavfi -t 3.8 -i anullsrc=r=48000:cl=stereo -filter_complex "[0:v]scale=1440:2560,zoompan=z=\'1+0.04*on/114\':x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':d=114:s=720x1280:fps=30[v]" -map "[v]" -map 1:a -c:v libx264 -preset veryfast -crf 20 -c:a aac -ar 48000 -ac 2 -t 3.8 {B}cover.mp4')
parts.append(B+'cover.mp4')
open(B+'list.txt','w').write(''.join(f"file '{x}'\n" for x in parts))
run(f'ffmpeg -y -f concat -safe 0 -i {B}list.txt -c:v libx264 -preset veryfast -crf 20 -c:a aac -ar 48000 -ac 2 {B}concat.mp4')
# SFX track
sr=48000; dur=float(subprocess.check_output(f'ffprobe -v error -show_entries format=duration -of csv=p=0 {B}concat.mp4',shell=True))
tr=np.zeros(int(sr*(dur+1)))
def boom(t,amp=0.9,f0=70):
    n=int(sr*0.6); x=np.arange(n)/sr; s=amp*np.sin(2*np.pi*f0*x*(1-0.4*x))*np.exp(-x*6); i=int(t*sr); tr[i:i+n]+=s[:len(tr)-i]
def hit(t,amp=0.6):
    n=int(sr*0.25); x=np.arange(n)/sr; s=amp*np.random.RandomState(1).randn(n)*np.exp(-x*25); i=int(t*sr); tr[i:i+n]+=s[:len(tr)-i]
def whoosh(t,amp=0.25,l=0.4):
    n=int(sr*l); x=np.linspace(0,1,n); s=amp*np.random.RandomState(2).randn(n)*np.sin(np.pi*x)**2; s=np.convolve(s,np.ones(30)/30,'same'); i=int(t*sr); tr[i:i+n]+=s[:len(tr)-i]
starts=[0]; 
for x in parts[:-1]: starts.append(starts[-1]+float(subprocess.check_output(f'ffprobe -v error -show_entries format=duration -of csv=p=0 {x}',shell=True)))
boom(0.0); 
for t in starts[1:]: whoosh(max(0,t-0.15))
hit(starts[7]+0.05,0.7); boom(starts[8]+0.02,0.8,55); boom(starts[9],0.9,60); boom(starts[10],0.7,90)
tr=np.clip(tr,-1,1)
with wave.open(B+'sfx.wav','w') as w_: w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(sr); w_.writeframes((tr*32767*0.5).astype(np.int16).tobytes())
OUT='libro_navidad/V01_ultimo_turron.mp4'
run(f'ffmpeg -y -i {B}concat.mp4 -i {B}sfx.wav -filter_complex "[0:a]loudnorm=I=-14:TP=-2:LRA=11[a0];[1:a]volume=0.8[a1];[a0][a1]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89[a]" -map 0:v -map "[a]" -c:v libx264 -preset veryfast -crf 23 -maxrate 1100k -bufsize 2200k -c:a aac -b:a 128k -movflags +faststart {OUT}')
print('starts',[round(s,2) for s in starts],'dur',round(dur,2))
