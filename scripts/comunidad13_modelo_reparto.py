import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy import ndimage
F='docs/comunidad13/fichas/'; S=sys.argv[1]
chars=[('1_maruja','MARUJA','La presidenta'),('2_manolo','MANOLO','El espía'),('3_rafa','RAFA','El cuñado'),('4_vane','VANE','La detective'),('5_kevin','KEVIN','El influencer'),('6_amparo','AMPARO','La suegra'),('7_sonia_v2','SONIA','La misteriosa'),('8_paco','PACO','El manitas')]
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
W,H=3200,1800; Y=(255,222,0)
c=Image.new('RGB',(W,H),Y); d=ImageDraw.Draw(c)
# halftone dots
for y in range(0,H,26):
    for x in range((y//26%2)*13,W,26): d.ellipse([x-3,y-3,x+3,y+3],fill=(250,205,0))
anton=ImageFont.truetype(S+'/fonts/fontsource-anton-5.3.0/package/files/anton-latin-400-normal.woff',150)
bal=ImageFont.truetype(S+'/fonts/fontsource-baloo-2-5.3.0/package/files/baloo-2-latin-800-normal.woff',58)
bal2=ImageFont.truetype(S+'/fonts/fontsource-baloo-2-5.3.0/package/files/baloo-2-latin-800-normal.woff',40)
def stroked(xy,t,f,fill,anchor):
    d.text(xy,t,font=f,fill=fill,anchor=anchor,stroke_width=8,stroke_fill='black')
stroked((W//2,40),'LA COMUNIDAD DEL 13',anton,(255,40,150),'mt')
stroked((W//2,215),'«AQUÍ NO SE SALVA NADIE»',bal,(0,200,255),'mt')
n=len(chars); M=90; slot=(W-2*M)/n; ground=H-170; th=1480
hf={'1_maruja':.9,'2_manolo':.84,'3_rafa':.88,'4_vane':.93,'5_kevin':.95,'6_amparo':.76,'7_sonia_v2':1.0,'8_paco':.88}
for i,(p,name,role) in enumerate(chars):
    im=cut(p); h=int(th*hf[p]); s=h/im.height; im=im.resize((int(im.width*s),h),Image.LANCZOS)
    if im.width>slot*1.35: s2=slot*1.35/im.width; im=im.resize((int(im.width*s2),int(im.height*s2)),Image.LANCZOS)
    cx=int(M+slot*i+slot/2); cx=max(cx,im.width//2+20); cx=min(cx,W-im.width//2-20); c.paste(im,(cx-im.width//2,ground-im.height),im)
    stroked((cx,ground+12),name,bal,'white','mt'); stroked((cx,ground+80),role,bal2,(255,40,150),'mt')
c.save(F+'modelo_reparto.png'); c.resize((1600,900),Image.LANCZOS).save(S+'/check.png')
