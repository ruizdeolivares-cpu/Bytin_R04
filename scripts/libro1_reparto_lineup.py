import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy import ndimage
F='docs/libro1_reparto/'; S=sys.argv[1]
chars=[('1A_dona_remedios','REMEDIOS','1.º A · el visillo'),('1B_paco','PACO','1.º B · el taladro'),('2A_vanessa','VANESSA','2.º A · influencer'),('2B_don_anselmo','DON ANSELMO','2.º B · presidente'),('3A_marisa','MARISA','3.º A · salsa'),('3A_manolo','MANOLO','3.º A · su marido'),('3B_iker','IKER','3.º B · opositor'),('4A_charo','CHARO','4.º A · y Satanás'),('4B_misterio','4.º B','¿¿??')]
def cut(p):
    im=Image.open(F+p+'.png').convert('RGB'); a=np.asarray(im).astype(int)
    bg=np.median(np.concatenate([a[:8].reshape(-1,3),a[-8:].reshape(-1,3),a[:,:8].reshape(-1,3),a[:,-8:].reshape(-1,3)]),0)
    d=np.sqrt(((a-bg)**2).sum(2)); near=d<60
    lab,_=ndimage.label(near); edge=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
    bgm=np.isin(lab,list(edge)); fg=~bgm
    fg=ndimage.binary_opening(fg,iterations=1)
    lab2,n=ndimage.label(fg); sz=ndimage.sum(fg,lab2,range(1,n+1)); keep=np.isin(lab2,[i+1 for i,s in enumerate(sz) if s>800]); fg=keep
    al=Image.fromarray((fg*255).astype('uint8')).filter(ImageFilter.GaussianBlur(0.8))
    im=im.convert('RGBA'); im.putalpha(al); return im.crop(im.getbbox())
W,H=3600,1280; Y=(255,222,0)
c=Image.new('RGB',(W,H),Y); d=ImageDraw.Draw(c)
# halftone dots
for y in range(0,H,26):
    for x in range((y//26%2)*13,W,26): d.ellipse([x-3,y-3,x+3,y+3],fill=(250,205,0))
anton=ImageFont.truetype(S+'/fonts/fontsource-anton-5.3.0/package/files/anton-latin-400-normal.woff',150)
bal=ImageFont.truetype(S+'/fonts/fontsource-baloo-2-5.3.0/package/files/baloo-2-latin-800-normal.woff',58)
bal2=ImageFont.truetype(S+'/fonts/fontsource-baloo-2-5.3.0/package/files/baloo-2-latin-800-normal.woff',40)
def stroked(xy,t,f,fill,anchor):
    d.text(xy,t,font=f,fill=fill,anchor=anchor,stroke_width=8,stroke_fill='black')
stroked((W//2,40),'CALLE DEL RENCOR, 13',anton,(255,40,150),'mt')
stroked((W//2,215),'PASATIEMPOS TÓXICOS · LOS SOSPECHOSOS',bal,(0,200,255),'mt')
n=len(chars); M=90; slot=(W-2*M)/n; ground=H-170; th=1400
hf={'1A_dona_remedios':.70,'1B_paco':.85,'2A_vanessa':.90,'2B_don_anselmo':.80,'3A_marisa':.88,'3A_manolo':.78,'3B_iker':.90,'4A_charo':.86,'4B_misterio':.93}
ims=[]
for p,name,role in chars:
    im=cut(p); h=int(th*hf[p]); im=im.resize((int(im.width*h/im.height),h),Image.LANCZOS); ims.append(im)
gap=-20; tot=sum(m.width for m in ims)+gap*(n-1); k=min(1,(W-2*M)/tot)
ims=[m.resize((int(m.width*k),int(m.height*k)),Image.LANCZOS) for m in ims]
x=(W-(sum(m.width for m in ims)+gap*k*(n-1)))/2
for im,(p,name,role) in zip(ims,chars):
    cx=int(x+im.width/2); c.paste(im,(int(x),ground-im.height),im)
    stroked((cx,ground+12),name,bal,'white','mt'); stroked((cx,ground+80),role,bal2,(255,40,150),'mt')
    x+=im.width+gap*k
c.save(F+'reparto_libro1.png'); c.resize((1800,640),Image.LANCZOS).save(S+'/check.png')
