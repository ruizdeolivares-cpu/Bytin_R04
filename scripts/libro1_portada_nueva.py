import sys, numpy as np, pymupdf
from PIL import Image
S=sys.argv[1]; SRC=sys.argv[2]
K=300/72; Y=np.array([255,242,0])
full=np.asarray(Image.open(S+'/cub300.png').convert('RGB')).astype(int)
x0=round(457.2144*K); PW=full.shape[1]-x0; PH=full.shape[0]
# art recoloured to cover yellow
art=np.asarray(Image.open('libro_pt1/portada_nueva_arte.png').convert('RGB')).astype(float)
src=np.array([253,196,5]); dist=np.sqrt(((art-src)**2).sum(2)); w=np.clip(1-dist/70,0,1)[...,None]
art=np.clip(art+w*(Y-src),0,255).astype('uint8'); art=Image.fromarray(art)
title_bottom=round(305*K)
roof=300/1728; Ha=int((PH-title_bottom)/(1-roof)); Wa=int(Ha*art.width/art.height)
art=art.resize((Wa,Ha),Image.LANCZOS)
panel=Image.new('RGB',(PW,PH),tuple(Y)); panel.paste(art,((PW-Wa)//2,PH-Ha))
# title block from original, yellow keyed out
tb=full[:title_bottom+10, x0:]
d=np.sqrt(((tb-Y)**2).sum(2)); alpha=np.clip((d-25)*6,0,255).astype('uint8')
t=Image.fromarray(tb.astype('uint8')).convert('RGBA'); t.putalpha(Image.fromarray(alpha))
panel.paste(t,(0,0),t)
panel.save('libro_pt1/portada_nueva_frontal.png')
# KDP cover pdf
doc=pymupdf.open(SRC); pg=doc[0]; r=pymupdf.Rect(457.2144,0,pg.rect.width,pg.rect.height)
pg.add_redact_annot(r); pg.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_REMOVE,graphics=pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_TOUCHED)
pg.insert_image(r,filename='libro_pt1/portada_nueva_frontal.png')
doc.save('libro_pt1/Pasatiempos_toxicos_CUBIERTA_KDP_v3.pdf',garbage=4,deflate=True)
print('panel',PW,PH,'art',Wa,Ha)
