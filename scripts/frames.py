import sys
from PIL import Image, ImageFilter, ImageEnhance
S=sys.argv[1]; O='libro_navidad/v01_inicio/'
W,H=1080,1920
bg=Image.open('libro_navidad/fondo_salon.png').convert('RGB').resize((W,H),Image.LANCZOS)
bgb=ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(3))).enhance(0.85)
def frame(name,out,frac,width,xc=0.5,yoff=0):
    c=Image.open(f'{S}/v01/{name}_cut.png'); c=c.crop((0,0,c.width,int(c.height*frac)))
    s=width/c.width; c=c.resize((int(c.width*s),int(c.height*s)),Image.LANCZOS)
    if c.height>H*0.92: s2=H*0.92/c.height; c=c.resize((int(c.width*s2),int(c.height*s2)),Image.LANCZOS)
    f=bgb.copy(); f.paste(c,(int(W*xc-c.width/2),H-c.height+yoff),c); f.save(O+out)
    return f
fr=[frame('abuela_paqui','P2a_abuela.png',0.58,1150),frame('mari_carmen','P2b_P3b_suegra.png',0.55,1150),
    frame('ivan','P2c_ivan.png',0.58,1000),frame('toni','P2d_P3_toni.png',0.52,1300)]
th=[f.resize((270,480)) for f in fr]
c=Image.new('RGB',(270*4+30,480),'white'); [c.paste(t,(i*280,0)) for i,t in enumerate(th)]; c.save(S+'/v01/frames.png')
