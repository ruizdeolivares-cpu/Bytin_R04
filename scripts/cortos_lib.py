# Base común para vídeos cortos de Pasatiempos tóxicos (720×1280, 30 fps, sin música, SFX sintetizados).
import subprocess, numpy as np, wave, math
from PIL import Image, ImageDraw, ImageFont
W,H,FPS=720,1280,30
YEL,PINK,BLK,WHT,GRY,CYAN,PURP=(255,226,0),(255,45,150),(17,17,17),(255,255,255),(226,226,226),(0,190,235),(120,60,200)
class K:
    def __init__(s,S):
        s.ANT=S+'/fonts/fontsource-anton-5.3.0/package/files/anton-latin-400-normal.woff'
        s.POP=S+'/fonts/pop/package/files/poppins-latin-800-normal.woff'
    def A(s,n): return ImageFont.truetype(s.ANT,max(1,int(n)))
    def P(s,n): return ImageFont.truetype(s.POP,max(1,int(n)))
def ease(x): x=max(0,min(1,x)); return 1-(1-x)**3
def pop(x): x=max(0,min(1,x)); return 1+0.18*math.sin(x*math.pi)*(1-x) if x<1 else 1
def dots(col,dot):
    im=Image.new('RGB',(W,H),col); d=ImageDraw.Draw(im)
    for y in range(0,H,22):
        for x in range((y//22%2)*11,W,22): d.ellipse([x-3,y-3,x+3,y+3],fill=dot)
    return im
def ctext(d,y,s,f,fill,sw=0,sf=BLK,cx=330): d.text((cx,y),s,font=f,fill=fill,anchor='mm',stroke_width=sw,stroke_fill=sf)
def wrap(d,s,f,maxw):
    out=[];cur=''
    for w in s.split():
        t=(cur+' '+w).strip()
        if d.textlength(t,font=f)>maxw and cur: out.append(cur);cur=w
        else: cur=t
    out.append(cur); return out
def box_text(d,cy,s,f,fill,bg,maxw=520,lh=None,pad=18,outline=BLK):
    ls=wrap(d,s,f,maxw); lh=lh or int(f.size*1.18); h=len(ls)*lh
    w=max(d.textlength(l,font=f) for l in ls)
    d.rounded_rectangle([330-w/2-pad,cy-h/2-pad*0.7,330+w/2+pad,cy+h/2+pad*0.7],radius=16,fill=bg,outline=outline,width=5)
    for i,l in enumerate(ls): d.text((330,cy-h/2+lh*i+lh/2),l,font=f,fill=fill,anchor='mm')
def fill_crop(im,w,h,yc=0.5):
    r=max(w/im.width,h/im.height); im=im.resize((int(im.width*r)+1,int(im.height*r)+1),Image.LANCZOS)
    x=(im.width-w)//2; y=int((im.height-h)*yc); return im.crop((x,y,x+w,y+h))
def circle(img,box,s):
    f=img.crop(box).resize((s,s),Image.LANCZOS); m=Image.new('L',(s,s),0); ImageDraw.Draw(m).ellipse([0,0,s-1,s-1],fill=255); return f,m
def render(frame_fn,dur,out_v,cover_t=None,cover_path=None):
    p=subprocess.Popen(f'ffmpeg -v error -y -f rawvideo -pix_fmt rgb24 -s {W}x{H} -r {FPS} -i - -c:v libx264 -preset veryfast -crf 16 -pix_fmt yuv420p {out_v}',shell=True,stdin=subprocess.PIPE)
    for i in range(int(round(dur*FPS))):
        f=frame_fn(i/FPS); p.stdin.write(f.tobytes())
        if cover_t is not None and i==int(cover_t*FPS): f.convert('RGB').save(cover_path,quality=92)
    p.stdin.close(); p.wait()
class Sfx:
    def __init__(s,dur,sr=48000): s.sr=sr; s.tr=np.zeros(int(sr*(dur+1)))
    def add(s,t,x): i=int(t*s.sr); s.tr[i:i+len(x)]+=x[:len(s.tr)-i]
    def boom(s,t,a=0.9,f0=65): x=np.arange(int(s.sr*.6))/s.sr; s.add(t,a*np.sin(2*np.pi*f0*x*(1-0.4*x))*np.exp(-x*6))
    def whoosh(s,t,a=0.3,l=0.35,seed=2): n=int(s.sr*l); x=np.linspace(0,1,n); y=a*np.random.RandomState(seed).randn(n)*np.sin(np.pi*x)**2; s.add(t,np.convolve(y,np.ones(30)/30,'same'))
    def tick(s,t,f=1800,a=0.35): x=np.arange(int(s.sr*.06))/s.sr; s.add(t,a*np.sin(2*np.pi*f*x)*np.exp(-x*70))
    def ding(s,t,a=0.4): x=np.arange(int(s.sr*.8))/s.sr; s.add(t,a*(np.sin(2*np.pi*1320*x)+0.5*np.sin(2*np.pi*1980*x))*np.exp(-x*5))
    def pop(s,t,a=0.5): x=np.arange(int(s.sr*.09))/s.sr; s.add(t,a*np.sin(2*np.pi*(500+3000*x)*x)*np.exp(-x*40))
    def buzz(s,t,a=0.3,l=0.35): x=np.arange(int(s.sr*l))/s.sr; s.add(t,a*np.sign(np.sin(2*np.pi*110*x))*np.exp(-x*4))
    def save(s,path):
        tr=s.tr/np.abs(s.tr).max()*10**(-3/20)
        with wave.open(path,'w') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(s.sr); w.writeframes((tr*32767).astype(np.int16).tobytes())
def mux(v,a,dur,out):
    subprocess.run(f'ffmpeg -v error -y -i {v} -i {a} -map 0:v -map 1:a -c:v libx264 -preset slow -crf 21 -maxrate 1500k -bufsize 3000k -c:a aac -b:a 128k -ac 2 -t {dur} -movflags +faststart {out}',shell=True,check=True)
def sheet(video,times,out):
    fr=[]
    for t in times:
        r=subprocess.run(f'ffmpeg -v error -ss {t} -i {video} -frames:v 1 -f rawvideo -pix_fmt rgb24 -',shell=True,capture_output=True).stdout
        im=Image.frombytes('RGB',(W,H),r); d=ImageDraw.Draw(im); d.line([0,1047,W,1047],fill='red',width=4); d.line([620,0,620,H],fill='red',width=4); fr.append(im.resize((240,427)))
    o=Image.new('RGB',(240*len(fr),427)); [o.paste(f,(i*240,0)) for i,f in enumerate(fr)]; o.save(out)
def box_top(d,top,s,f,fill,bg,maxw=520,pad=16,outline=BLK,cx=330):
    """Caja con texto anclada por arriba. Devuelve la y de abajo."""
    ls=wrap(d,s,f,maxw); lh=int(f.size*1.2); h=len(ls)*lh; w=max(d.textlength(l,font=f) for l in ls)
    d.rounded_rectangle([cx-w/2-pad,top,cx+w/2+pad,top+h+pad*1.4],radius=16,fill=bg,outline=outline,width=5)
    for i,l in enumerate(ls): d.text((cx,top+pad*0.7+lh*i+lh/2),l,font=f,fill=fill,anchor='mm')
    return top+h+pad*1.4
