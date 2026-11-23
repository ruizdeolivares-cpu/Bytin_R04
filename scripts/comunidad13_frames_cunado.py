import numpy as np, math
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage
F='docs/comunidad13/fichas/'; O='docs/comunidad13/piloto_cunado/'
def cut(p):
    im=Image.open(F+p+'.png').convert('RGB'); a=np.asarray(im).astype(int)
    bg=np.median(np.concatenate([a[:8].reshape(-1,3),a[-8:].reshape(-1,3),a[:,:8].reshape(-1,3),a[:,-8:].reshape(-1,3)]),0)
    near=np.sqrt(((a-bg)**2).sum(2))<60
    lab,_=ndimage.label(near); edge=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
    fg=~np.isin(lab,list(edge)); fg=ndimage.binary_opening(fg,iterations=1)
    lab2,n=ndimage.label(fg); sz=ndimage.sum(fg,lab2,range(1,n+1)); fg=np.isin(lab2,[i+1 for i,s in enumerate(sz) if s>800])
    al=Image.fromarray((fg*255).astype('uint8')).filter(ImageFilter.GaussianBlur(0.8))
    im=im.convert('RGBA'); im.putalpha(al); return im.crop(im.getbbox())
W,H=1080,1920
def bg(c1,c2,burst=False):
    c=Image.new('RGB',(W,H),c1); d=ImageDraw.Draw(c)
    if burst:
        cx,cy=W//2,H//2-150
        for k in range(24):
            a0=2*math.pi*k/24; a1=a0+math.pi/24
            d.polygon([(cx,cy),(cx+3000*math.cos(a0),cy+3000*math.sin(a0)),(cx+3000*math.cos(a1),cy+3000*math.sin(a1))],fill=c2)
    for y in range(0,H,30):
        for x in range((y//30%2)*15,W,30): d.ellipse([x-4,y-4,x+4,y+4],fill=tuple(max(0,v-25) for v in c1))
    return c
Y=(255,222,0); P=(255,45,150); C=(0,200,255)
rafa=cut('3_rafa'); vane=cut('4_vane')
def place(c,im,h,cx,top_frac=1.0,bottom=None):
    s=h/ (im.height*top_frac); im2=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
    y=(bottom if bottom is not None else H)-int(im2.height*top_frac) if top_frac<1 else (bottom or H)-im2.height
    c.paste(im2,(cx-im2.width//2,y),im2)
# F1 Rafa primer plano (cintura para arriba)
c=bg(Y,P,True); place(c,rafa,1450,W//2+40,top_frac=0.55,bottom=H); c.save(O+'F1_rafa_primer_plano.png')
# F2 plano medio de los dos
c=bg(C,C); place(c,rafa,1380,290); place(c,vane,1440,820); c.save(O+'F2_rafa_y_vane.png')
# F3 Vane primer plano a camara, Rafa detras
c=bg(P,Y,True); place(c,rafa,1250,250,top_frac=0.6,bottom=H); place(c,vane,1500,700,top_frac=0.6,bottom=H); c.save(O+'F3_vane_remate.png')
for n in ['F1_rafa_primer_plano','F2_rafa_y_vane','F3_vane_remate']:
    Image.open(O+n+'.png').resize((270,480)).save(f'{__import__("sys").argv[1]}/{n}_s.png')
