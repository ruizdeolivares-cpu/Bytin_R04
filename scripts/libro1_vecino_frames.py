import sys
sys.argv=[sys.argv[0],sys.argv[1]]
exec(open(sys.argv[1]+'/v01/cut.py').read().split("if __name__")[0])
from PIL import Image, ImageFilter, ImageEnhance
S=sys.argv[1]; R='docs/libro1_reparto/'; O='libro_pt1/v_vecino/'
W,H=1080,1920
def bg(n,blur=2): 
    b=Image.open(O+f'fondo_{n}.png').convert('RGB').resize((W,H),Image.LANCZOS)
    return ImageEnhance.Brightness(b.filter(ImageFilter.GaussianBlur(blur))).enhance(0.9)
def frame(char,fondo,out,frac,width,xc=0.5):
    c=cutout(R+char+'.png',[]); c=c.crop((0,0,c.width,int(c.height*frac)))
    s=width/c.width; c=c.resize((int(c.width*s),int(c.height*s)),Image.LANCZOS)
    if c.height>H*0.92: s2=H*0.92/c.height; c=c.resize((int(c.width*s2),int(c.height*s2)),Image.LANCZOS)
    f=bg(fondo); f.paste(c,(int(W*xc-c.width/2),H-c.height),c); f.save(O+out); return f
fr=[frame('3A_marisa','ascensor','P1_marisa.png',0.62,1050),
frame('3A_manolo','portal','P2_manolo.png',0.50,1350),
frame('1A_dona_remedios','portal','P3_remedios.png',0.62,1050),
frame('2B_don_anselmo','portal','P4_anselmo.png',0.50,1350),
frame('4B_misterio','ascensor','P5_4B.png',0.55,1000),
frame('4A_charo','ascensor','P6_charo.png',0.55,1100)]
th=[f.resize((216,384)) for f in fr]
c=Image.new('RGB',(216*6+50,384),'white'); [c.paste(t,(i*226,0)) for i,t in enumerate(th)]; c.save(S+'/vv/frames.png')
