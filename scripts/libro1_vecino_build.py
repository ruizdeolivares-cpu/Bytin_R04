# Monta «El vecino que todos tenemos» (libro 1)
import os, sys, subprocess, numpy as np, wave
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S=sys.argv[1]; C=S+'/vv/clips/'; B=S+'/vv/build/'; os.makedirs(B,exist_ok=True)
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

def note_clip(text,out,dur):
    bg=Image.open('libro_pt1/v_vecino/fondo_ascensor.png').convert('RGB')
    w,h=bg.size; crop=bg.crop((int(w*0.22),int(h*0.24),int(w*0.78),int(h*0.24)+int(w*0.56*16/9)))
    f=crop.resize((W,H),Image.LANCZOS); d=ImageDraw.Draw(f)
    fn=FA(62); lines=text.split('\n'); yy=330-(len(lines)-1)*38
    for ln in lines: d.text((361,yy),ln,font=fn,fill=(20,20,20),anchor='mm'); yy+=76
    f.save(B+out+'.png')
    run(f'ffmpeg -y -loop 1 -t {dur} -i {B}{out}.png -f lavfi -t {dur} -i anullsrc=r=48000:cl=stereo -filter_complex "[0:v]scale=1440:2560,zoompan=z=\'1.05+0.08*on/{int(dur*30)}\':x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':d={int(dur*30)}:s=720x1280:fps=30[v]" -map "[v]" -map 1:a -c:v libx264 -preset veryfast -crf 20 -c:a aac -ar 48000 -ac 2 -t {dur} {B}{out}.mp4')
    return B+out+'.mp4'
def seg(k,v,a,b,txt,keys,top=None):
    png=B+f's{k}.png'; sub_png(txt,keys,png,top=top); dur=b-a; out=B+f'p{k}.mp4'
    run(f'ffmpeg -y -ss {a} -t {dur} -i {C}{v}.mp4 -i {png} -filter_complex "[0:v]scale=720:1280,fps=30[v0];[v0][1:v]overlay=0:0[v]" -map "[v]" -map 0:a -c:v libx264 -preset veryfast -crf 20 -c:a aac -ar 48000 -ac 2 -t {dur} {out}')
    return out
parts=[]
parts.append(note_clip('ALGUIEN DE ESTA\nCOMUNIDAD ES\nUN HIJO DE…','n1',1.1))
parts.append(seg(1,'61834d2c-QrwpC',0.8,3.2,'¡¡QUE SE SEPA QUIÉN HA SIDO!!',['SEPA','SIDO']))
parts.append(seg(2,'8973db70-LuKyz',0.7,5.15,'Yo no he sido. Pero sé perfectamente quién ha sido.',['PERFECTAMENTE']))
parts.append(seg(3,'86be255a-IbcF3',2.2,3.4,'Yo no digo nada…',['NADA']))
parts.append(seg(4,'86be255a-IbcF3',5.2,8.3,'…pero ayer entró alguien a las 23:47.',['23:47']))
parts.append(seg(5,'ac6b6bc4-SllOO',1.0,5.15,'Tengo cámaras. Y tengo tiempo.',['CÁMARAS','TIEMPO']))
parts.append(seg(6,'56ace1d9-eOSBZ',2.4,4.1,'Yo ni siquiera vivo aquí.',['AQUÍ']))
parts.append(note_clip('EL CULPABLE\nESTÁ ENTRE\nLOS OCHO','n2',1.8))
parts.append(seg(7,'9921acf4-Xwbdh',1.5,3.3,'¿Y si el culpable…',['CULPABLE']))
parts.append(seg(8,'9921acf4-Xwbdh',4.6,7.7,'…eres tú?',['TÚ']))
parts.append(seg(9,'eb229668-Q4zHS',0.45,3.0,'Yo no pienso resolver nada.',['NADA']))
parts.append(seg(10,'eb229668-Q4zHS',3.0,6.8,'Que lo resuelva el presidente, que para eso cobra.',['PRESIDENTE','COBRA']))
def card(out,dur,draw):
    im=Image.new('RGB',(W,H),YEL); d=ImageDraw.Draw(im)
    for y in range(0,H,22):
        for x in range((y//22%2)*11,W,22): d.ellipse([x-3,y-3,x+3,y+3],fill=(245,205,0))
    draw(im,d); im.save(B+out+'.png')
    run(f'ffmpeg -y -loop 1 -t {dur} -i {B}{out}.png -f lavfi -t {dur} -i anullsrc=r=48000:cl=stereo -filter_complex "[0:v]scale=1440:2560,zoompan=z=\'1+0.04*on/{int(dur*30)}\':x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':d={int(dur*30)}:s=720x1280:fps=30[v]" -map "[v]" -map 1:a -c:v libx264 -preset veryfast -crf 20 -c:a aac -ar 48000 -ac 2 -t {dur} {B}{out}.mp4')
    return B+out+'.mp4'
FBs=ImageFont.truetype(S+'/fonts/fontsource-baloo-2-5.3.0/package/files/baloo-2-latin-800-normal.woff',40)
def d1(im,d):
    for i,(t,y) in enumerate([('OCHO VECINOS.',230),('OCHO SOSPECHOSOS.',330),('OCHO PISTAS.',430)]):
        d.text((330,y),t,font=FA(82),fill=PINK if i==2 else 'black',anchor='mm',stroke_width=6 if i==2 else 0,stroke_fill='black')
    R='docs/libro1_reparto/'; ims=['4A_charo','1B_paco','3A_marisa','2B_don_anselmo','1A_dona_remedios']
    x=40
    for n in ims:
        c=Image.open(R+n+'.png').convert('RGB'); w,h=c.size; c=c.crop((int(w*.15),0,int(w*.85),int(w*.7))).resize((116,116)); im.paste(c,(x,520)); d.rectangle([x,520,x+116,636],outline='black',width=4); x+=122
    for i,t in enumerate(['Sudokus, criptogramas, acertijos','y una comunidad que está','como una cabra.']):
        d.text((330,730+i*58),t,font=FBs,fill='black',anchor='mm')
parts.append(card('c1',4.2,d1))
def d2(im,d):
    p=Image.open('libro_pt1/portada.png').convert('RGB'); ph=600; p=p.resize((int(p.width*ph/p.height),ph)); im.paste(p,(330-p.width//2,150))
    d.text((330,860),'El regalo perfecto para ese',font=FBs,fill='black',anchor='mm')
    d.text((330,915),'vecino que te cae fatal.',font=FBs,fill='black',anchor='mm')
    d.text((330,990),'EN AMAZON',font=FA(54),fill=PINK,anchor='mm',stroke_width=5,stroke_fill='black')
parts.append(card('c2',3.8,d2))
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
boom(0.0)
for t in starts[1:]: whoosh(max(0,t-0.15))
hit(starts[1],0.7); hit(starts[5]+1.6,0.5); boom(starts[7],0.9,50); boom(starts[8]+0.1,0.7,55); boom(starts[11],0.8,60); boom(starts[12],0.7,90)
tr=np.clip(tr,-1,1)
with wave.open(B+'sfx.wav','w') as w_: w_.setnchannels(1); w_.setsampwidth(2); w_.setframerate(sr); w_.writeframes((tr*32767*0.5).astype(np.int16).tobytes())
OUT='libro_pt1/V_vecino_que_todos_tenemos.mp4'
run(f'ffmpeg -y -i {B}concat.mp4 -i {B}sfx.wav -filter_complex "[0:a]loudnorm=I=-14:TP=-2:LRA=11[a0];[1:a]volume=0.8[a1];[a0][a1]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89[a]" -map 0:v -map "[a]" -c:v libx264 -preset veryfast -crf 23 -maxrate 1100k -bufsize 2200k -c:a aac -b:a 128k -movflags +faststart {OUT}')
print('starts',[round(s,2) for s in starts],'dur',round(dur,2))
