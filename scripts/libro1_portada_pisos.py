import sys
exec(open(sys.argv[1]+'/v01/cut.py').read().split("if __name__")[0])
from PIL import Image, ImageDraw, ImageFont
S=sys.argv[1]; R='docs/libro1_reparto/'
FB=ImageFont.truetype(S+'/fonts/fontsource-baloo-2-5.3.0/package/files/baloo-2-latin-800-normal.woff',44)
W,H=1600,2400; c=Image.new('RGB',(W,H),(255,222,0)); d=ImageDraw.Draw(c)
rows=[[('4A_charo',),('4B_misterio',)],[('3A_marisa','3A_manolo'),('3B_iker',)],[('2A_vanessa',),('2B_don_anselmo',)],[('1A_dona_remedios',),('1B_paco',)]]
labels=[['4.º A · CHARO','4.º B · ¿¿??'],['3.º A · MARISA Y MANOLO','3.º B · IKER'],['2.º A · VANESSA','2.º B · DON ANSELMO'],['1.º A · DOÑA REMEDIOS','1.º B · PACO']]
cw,ch=W//2,H//4
for i,row in enumerate(rows):
    for j,cell in enumerate(row):
        x0,y0=j*cw,i*ch
        d.rectangle([x0+8,y0+8,x0+cw-8,y0+ch-8],outline='black',width=8,fill=(255,236,120))
        n=len(cell)
        for k,name in enumerate(cell):
            im=cutout(R+name+'.png',[]); im=im.crop((0,0,im.width,int(im.height*0.5)))  # busto
            tw=(cw-60)//n; th=ch-110; s=min(tw/im.width,th/im.height); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
            c.paste(im,(x0+30+k*tw+(tw-im.width)//2,y0+ch-20-im.height),im)
        d.text((x0+cw//2,y0+50),labels[i][j],font=FB,fill='black',anchor='mm')
c.save('libro_pt1/portada_referencia_pisos.png'); c.resize((400,600)).save(S+'/vv/grid_s.png')
