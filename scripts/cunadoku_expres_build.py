# «Cuñadoku exprés» (~7 s): Toni + Cuñadoku n.º 1 (pág. 9, libro Navidad). Mentira real: fila 4, col 4 (el 6; de verdad es un 3). NO destripar en el vídeo.
import sys, subprocess, numpy as np, wave, math
from PIL import Image, ImageDraw, ImageFont
S=sys.argv[1]; B=S+'/cd/'; W,H,FPS=720,1280,30
ANT=S+'/fonts/fontsource-anton-5.3.0/package/files/anton-latin-400-normal.woff'
POP=S+'/fonts/pop/package/files/poppins-latin-800-normal.woff'
F=lambda p,s: ImageFont.truetype(p,s)
YEL,PINK,BLK,WHT,GRY=(255,226,0),(255,45,150),(17,17,17),(255,255,255),(226,226,226)
G=["060451","540032","450210","100645","614000","000104"]
T1,T2,T3=1.1,6.1,7.3
def ease(x): x=max(0,min(1,x)); return 1-(1-x)**3
toni=Image.open('libro_navidad/v01_inicio/P2d_P3_toni.png').convert('RGB').resize((W,H),Image.LANCZOS)
cover=Image.open('libro_navidad/portada.png').convert('RGB'); ch=660; cover=cover.resize((int(cover.width*ch/cover.height),ch),Image.LANCZOS)
def bg():
    im=Image.new('RGB',(W,H),YEL); d=ImageDraw.Draw(im)
    for y in range(0,H,22):
        for x in range((y//22%2)*11,W,22): d.ellipse([x-3,y-3,x+3,y+3],fill=(245,205,0))
    return im
BG=bg()
def ctext(d,y,s,f,fill,sw=0,sf=BLK,cx=330): d.text((cx,y),s,font=f,fill=fill,anchor='mm',stroke_width=sw,stroke_fill=sf)
def grid_img():
    c=95; g=Image.new('RGB',(c*6+8,c*6+8),WHT); d=ImageDraw.Draw(g); o=4
    for r in range(6):
        for k in range(6):
            v=G[r][k]; x,y=o+k*c,o+r*c
            d.rectangle([x,y,x+c,y+c],fill=GRY if v!='0' else WHT,outline=(120,120,120),width=2)
            if v!='0': d.text((x+c/2,y+c/2+3),v,font=F(POP,54),fill=BLK,anchor='mm')
    for i in range(7):
        w=8 if i in (0,6,3) else 2
        if i in (0,3,6): d.line([o+i*c,0,o+i*c,c*6+8],fill=BLK,width=w)
        if i in (0,2,4,6): d.line([0,o+i*c,c*6+8,o+i*c],fill=BLK,width=8)
    return g
GRID=grid_img()
_f=Image.open('libro_navidad/v01_inicio/P2d_P3_toni.png').convert('RGB').crop((380,520,820,960)).resize((130,130),Image.LANCZOS)
_m=Image.new('L',(130,130),0); ImageDraw.Draw(_m).ellipse([0,0,129,129],fill=255)
def badge(im,x,y,s):
    f=_f.resize((s,s),Image.LANCZOS); m=_m.resize((s,s)); d=ImageDraw.Draw(im)
    d.ellipse([x-6,y-6,x+s+5,y+s+5],fill=PINK,outline=BLK,width=4); im.paste(f,(x,y),m)
def frame(t):
    if t<T1:  # Toni + gancho
        z=1+0.08*t/T1; im=toni.resize((int(W*z),int(H*z)),Image.LANCZOS); x=(im.width-W)//2; im=im.crop((x,int((im.height-H)*0.3),x+W,int((im.height-H)*0.3)+H))
        d=ImageDraw.Draw(im); e=ease(t/0.25)
        ctext(d,175,'MI CUÑADO HA METIDO',F(ANT,int(60*e)+1),WHT,6)
        e2=ease((t-0.15)/0.25)
        ctext(d,270,'1 NÚMERO FALSO',F(ANT,int(92*e2)+1),PINK,7)
        return im
    if t<T2:  # el Cuñadoku
        im=BG.copy(); d=ImageDraw.Draw(im); u=t-T1
        e=ease(u/0.3); ctext(d,175,'¿CUÁL ES?',F(ANT,int(104*e)+1),PINK,7,cx=385)
        bs=int(118*(ease((u-0.1)/0.3)*(1+0.12*math.sin(max(0,u-2.5)*18)*math.exp(-max(0,u-2.5)*5)*(u>2.5)))) or 1
        badge(im,98-bs//2,175-bs//2,bs)
        ctext(d,262,'CUÑADOKU · NIVEL FÁCIL · 1 MENTIRA',F(POP,25),BLK)
        z=0.92+0.08*ease(u/0.35)+0.03*u/5; gw=int(GRID.width*z); g=GRID.resize((gw,gw),Image.LANCZOS)
        im.paste(g,(330-gw//2,600-gw//2)); d=ImageDraw.Draw(im)
        # barra de cuenta atrás
        frac=max(0,1-u/5.0); d.rounded_rectangle([60,918,600,944],radius=13,fill=(255,255,255),outline=BLK,width=4)
        if frac>0: d.rounded_rectangle([64,922,64+int(532*frac),940],radius=9,fill=PINK)
        ctext(d,995,'«Este vino es de 40 euros, que lo sepáis»',F(POP,27),BLK)
        return im
    im=BG.copy(); d=ImageDraw.Draw(im); u=t-T2   # cierre
    e=ease(u/0.25); cw=int(cover.width*(0.85+0.15*e)); c2=cover.resize((cw,int(cover.height*cw/cover.width)))
    d.rectangle([330-cw//2-5,130-5,330+cw//2+4,130+c2.height+4],fill=BLK); im.paste(c2,(330-cw//2,130))
    ctext(d,860,'¿LO HAS PILLADO?',F(ANT,64),WHT,6); ctext(d,935,'DÍMELO EN COMENTARIOS',F(POP,32),BLK)
    ctext(d,1005,'EN AMAZON',F(ANT,52),PINK,5)
    return im
N=int(T3*FPS)
p=subprocess.Popen(f'ffmpeg -v error -y -f rawvideo -pix_fmt rgb24 -s {W}x{H} -r {FPS} -i - -c:v libx264 -preset veryfast -crf 16 -pix_fmt yuv420p {B}v.mp4',shell=True,stdin=subprocess.PIPE)
for i in range(N):
    f=frame(i/FPS); p.stdin.write(f.tobytes())
    if i==int(0.6*FPS): f.save(B+'portada.png')
p.stdin.close(); p.wait()
# SFX
sr=48000; tr=np.zeros(int(sr*T3)+sr)
def add(t,s): i=int(t*sr); tr[i:i+len(s)]+=s[:len(tr)-i]
def boom(t,a=0.9,f0=65): x=np.arange(int(sr*.6))/sr; add(t,a*np.sin(2*np.pi*f0*x*(1-0.4*x))*np.exp(-x*6))
def whoosh(t,a=0.3,l=0.35): n=int(sr*l); x=np.linspace(0,1,n); s=a*np.random.RandomState(2).randn(n)*np.sin(np.pi*x)**2; add(t,np.convolve(s,np.ones(30)/30,'same'))
def tick(t,f=1800,a=0.35): x=np.arange(int(sr*.06))/sr; add(t,a*np.sin(2*np.pi*f*x)*np.exp(-x*70))
def ding(t,a=0.4): x=np.arange(int(sr*.8))/sr; add(t,a*(np.sin(2*np.pi*1320*x)+0.5*np.sin(2*np.pi*1980*x))*np.exp(-x*5))
boom(0.0); whoosh(T1-0.15); boom(T1,0.6,90)
for k in range(5): tick(T1+0.4+k, 1500+k*150, 0.3+k*0.04)
whoosh(T2-0.15); ding(T2)
tr=tr/np.abs(tr).max()*10**(-3/20)
with wave.open(B+'sfx.wav','w') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((tr*32767).astype(np.int16).tobytes())
OUT='libro_navidad/V_cunadoku_expres.mp4'
subprocess.run(f'ffmpeg -v error -y -i {B}v.mp4 -i {B}sfx.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 21 -maxrate 1500k -bufsize 3000k -c:a aac -b:a 128k -ac 2 -t {T3} -movflags +faststart {OUT}',shell=True,check=True)
Image.open(B+'portada.png').convert('RGB').save('libro_navidad/V_cunadoku_expres_portada.jpg',quality=92)
print('ok')
