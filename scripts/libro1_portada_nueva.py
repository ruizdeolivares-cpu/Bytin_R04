import sys, numpy as np, pymupdf
from PIL import Image
S=sys.argv[1]; SRC=sys.argv[2]
TITLEFONT=sys.argv[3] if len(sys.argv)>3 else 'bangers/package/files/bangers-latin-400-normal.woff'
OUTPDF=sys.argv[4] if len(sys.argv)>4 else 'libro_pt1/Pasatiempos_toxicos_CUBIERTA_KDP_v3.pdf'
K=300/72; Y=np.array([255,242,0])
full=np.asarray(Image.open(S+'/cub300.png').convert('RGB')).astype(int)
x0=round(457.2144*K); PW=full.shape[1]-x0; PH=full.shape[0]
# art recoloured to cover yellow
art=np.asarray(Image.open('libro_pt1/portada_nueva_arte.png').convert('RGB')).astype(float)
src=np.array([253,196,5]); dist=np.sqrt(((art-src)**2).sum(2)); w=np.clip(1-dist/70,0,1)[...,None]
art=np.clip(art+w*(Y-src),0,255).astype('uint8'); art=Image.fromarray(art)
title_bottom=round(316*K)
roof=300/1728; Ha=int((PH-title_bottom)/(1-roof)); Wa=int(Ha*art.width/art.height)
art=art.resize((Wa,Ha),Image.LANCZOS)
panel=Image.new('RGB',(PW,PH),tuple(Y)); panel.paste(art,((PW-Wa)//2,PH-Ha))
# --- título nuevo, estilo pop art
from PIL import ImageDraw, ImageFont
FD=S+'/fonts/'
TF=lambda n: ImageFont.truetype(FD+TITLEFONT,n)
ANT=lambda n: ImageFont.truetype(FD+'fontsource-anton-5.3.0/package/files/anton-latin-400-normal.woff',n)
PMK=lambda n: ImageFont.truetype(FD+'pm/package/files/permanent-marker-latin-400-normal.woff',n)
BLACK=(10,10,10); PINK=(255,40,150); WHITE=(255,255,255)
def word(text,font,fill,stroke,shadow,maxw,rot,center,spacing=0):
    d0=ImageDraw.Draw(Image.new('RGB',(10,10)))
    bb=d0.textbbox((0,0),text,font=font,stroke_width=stroke)
    w=bb[2]-bb[0]; h=bb[3]-bb[1]
    L=Image.new('RGBA',(w+shadow+80,h+shadow+80),(0,0,0,0)); d=ImageDraw.Draw(L)
    o=(40-bb[0],40-bb[1])
    d.text((o[0]+shadow,o[1]+shadow),text,font=font,fill=BLACK,stroke_width=stroke,stroke_fill=BLACK)
    d.text(o,text,font=font,fill=fill,stroke_width=stroke,stroke_fill=BLACK)
    if L.width-80>maxw:
        k=maxw/(L.width-80); L=L.resize((int(L.width*k),int(L.height*k)),Image.LANCZOS)
    L=L.rotate(rot,expand=True,resample=Image.BICUBIC)
    panel.paste(L,(int(center[0]-L.width/2),int(center[1]-L.height/2)),L)
CX=(PW-37)/2  # centro del área visible (sin sangrado derecho)
dr=ImageDraw.Draw(panel)
dr.text((CX,118),'F  R  A  N  C  I  S  C  O     R  U  I  Z',font=ANT(60),fill=BLACK,anchor='mm')
word('PASATIEMPOS',TF(420),WHITE,16,22,1560,2,(CX,370))
word('TÓXICOS',ANT(560),PINK,20,28,1300,2,(CX,770))
# subtítulo sobre pegatina negra
sub='para gente con mala leche'
fs=PMK(84); bb=dr.textbbox((0,0),sub,font=fs)
tw=bb[2]-bb[0]; th=bb[3]-bb[1]
st=Image.new('RGBA',(tw+90,th+60),(0,0,0,0)); sd=ImageDraw.Draw(st)
sd.rectangle([0,0,st.width,st.height],fill=BLACK); sd.text((45-bb[0],30-bb[1]),sub,font=fs,fill=(255,242,0))
st=st.rotate(-2,expand=True,resample=Image.BICUBIC); panel.paste(st,(int(CX-st.width/2),1075-st.height//2),st)
# franja rosa original (recortada del PDF, amarillo fuera)
y1=round(262*K); y2=round(305*K)
tb=full[y1:y2, x0:]
dd=np.sqrt(((tb-Y)**2).sum(2)); alpha=np.clip((dd-25)*6,0,255).astype('uint8')
t=Image.fromarray(tb.astype('uint8')).convert('RGBA'); t.putalpha(Image.fromarray(alpha))
panel.paste(t,(0,y1+30),t)
panel.save('libro_pt1/portada_nueva_frontal.png')
# KDP cover pdf
doc=pymupdf.open(SRC); pg=doc[0]; r=pymupdf.Rect(457.2144,0,pg.rect.width,pg.rect.height)
pg.add_redact_annot(r); pg.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_REMOVE,graphics=pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_TOUCHED)
pg.insert_image(r,filename='libro_pt1/portada_nueva_frontal.png')
doc.save(OUTPDF,garbage=4,deflate=True)
print('panel',PW,PH,'art',Wa,Ha)
