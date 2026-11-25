import sys, numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
def cutout(path, extra_cols, tol=70, pocket=600):
    im=Image.open(path).convert('RGB'); a=np.asarray(im).astype(int)
    border=np.concatenate([a[:6].reshape(-1,3),a[-6:].reshape(-1,3),a[:,:6].reshape(-1,3),a[:,-6:].reshape(-1,3)])
    cols=[np.median(border,0)]+[np.array(c) for c in extra_cols]
    near=np.zeros(a.shape[:2],bool)
    for c in cols: near|=np.sqrt(((a-c)**2).sum(2))<tol
    # halftone dots inside bg are darker variants: close small holes
    near=ndimage.binary_closing(np.pad(near,6,constant_values=True),iterations=3)[6:-6,6:-6]
    lab,_=ndimage.label(near); edge=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
    bg=np.isin(lab,list(edge))
    # burst may not touch edge: also take components adjacent to bg with burst colours
    fg=~bg; fg=ndimage.binary_opening(np.pad(fg,6),iterations=2)[6:-6,6:-6]
    lab2,n=ndimage.label(fg); sz=ndimage.sum(fg,lab2,range(1,n+1)); fg=lab2==(np.argmax(sz)+1)
    fg=ndimage.binary_fill_holes(fg)
    # interior background pockets (e.g. between legs)
    labn,nn=ndimage.label(near&fg); szs=ndimage.sum(near&fg,labn,range(1,nn+1))
    fg[np.isin(labn,[i+1 for i,s in enumerate(szs) if s>pocket])]=False
    fg=ndimage.binary_opening(np.pad(fg,4),iterations=2)[4:-4,4:-4]
    lab3,n3=ndimage.label(fg); s3=ndimage.sum(fg,lab3,range(1,n3+1)); fg=lab3==(np.argmax(s3)+1)
    al=Image.fromarray((fg*255).astype('uint8')).filter(ImageFilter.GaussianBlur(1))
    im=im.convert('RGBA'); im.putalpha(al); return im.crop(im.getbbox())
if __name__=='__main__':
    D='libro_navidad/fichas/'; O=sys.argv[1]
    specs={'toni':[(240,60,140)],'mari_carmen':[(30,180,210),(20,100,140)],'abuela_paqui':[(220,30,30),(140,10,10)],'ivan':[(30,170,230),(20,90,170),(10,60,130)]}
    for n,c in specs.items():
        cutout(D+n+'.png',c,pocket=(4000 if n=='abuela_paqui' else 600)).save(O+'/'+n+'_cut.png')
    from PIL import Image
    ims=[Image.open(O+'/'+n+'_cut.png') for n in specs]
    H=500; ims=[i.resize((int(i.width*H/i.height),H)) for i in ims]
    c=Image.new('RGB',(sum(i.width for i in ims)+40,H),(40,40,40)); x=0
    for i in ims: c.paste(i,(x,0),i); x+=i.width+10
    c.save(O+'/cuts.png')
