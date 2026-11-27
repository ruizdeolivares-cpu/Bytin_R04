# «¿Quién ha roto la copa?» (Navidad, pág. 25; solución pág. 92: fue TONI). ~9,5 s. NO destripar en el vídeo.
import sys; sys.path.insert(0,'scripts'); from cortos_lib import *
S=sys.argv[1]; k=K(S); B=S+'/cortos/'
T1,T2=1.3,8.3; DUR=T2+1.3
mc=Image.open('libro_navidad/v01_inicio/P2b_P3b_suegra.png').convert('RGB').resize((W,H),Image.LANCZOS)
DECL=[('TONI','«Ha sido Iván o Lucía.»'),('MARI CARMEN','«Yo ni me acerqué a la vitrina.»'),('ENCARNA','«Ha sido un hombre, seguro.»'),('IVÁN','«Toni miente.»'),('LUCÍA','«No he sido yo, ni tampoco Iván.»')]
FACES={'TONI':('libro_navidad/fichas/toni.png',(330,60,690,420)),'MARI CARMEN':('libro_navidad/fichas/mari_carmen.png',(360,180,640,460)),'IVÁN':('libro_navidad/fichas/ivan.png',(350,230,650,530))}
FC={n:circle(Image.open(f).convert('RGB'),b,74) for n,(f,b) in FACES.items()}
BG=dots((40,40,48),(55,55,65)); cover=Image.open('libro_navidad/portada.png').convert('RGB'); cover=cover.resize((int(cover.width*660/cover.height),660),Image.LANCZOS); END=dots(YEL,(245,205,0))
def frame(t):
    if t<T1:
        z=1+0.07*t/T1; im=fill_crop(mc,int(W*z),int(H*z),0.3).crop((int(W*(z-1)/2),0,int(W*(z-1)/2)+W,H)); d=ImageDraw.Draw(im)
        e=ease(t/0.25); ctext(d,165,'ALGUIEN HA ROTO',k.A(70*e),WHT,6); ctext(d,248,'LA COPA BUENA',k.A(86*ease((t-0.12)/0.25)),PINK,7)
        if t>0.6: box_top(d,930,'Solo UNO miente',k.P(40*pop((t-0.6)/0.3)),BLK,YEL)
        return im
    if t<T2:
        u=t-T1; im=BG.copy(); d=ImageDraw.Draw(im)
        ctext(d,170,'¿QUIÉN FUE?',k.A(96*pop(u/0.3)),YEL,7); ctext(d,245,'Solo UNO miente… y es el culpable',k.P(27),WHT)
        for i,(n,q) in enumerate(DECL):
            a=ease((u-0.15*i)/0.25)
            if a<=0: continue
            y=300+i*138; x=40-int((1-a)*400)
            d.rounded_rectangle([x,y,x+585,y+120],radius=18,fill=WHT,outline=BLK,width=4)
            if n in FC: f,m=FC[n]; d.ellipse([x+12,y+20,x+92,y+100],fill=PINK); im.paste(f,(x+15,y+23),m); d=ImageDraw.Draw(im)
            else: d.ellipse([x+12,y+20,x+92,y+100],fill=PINK,outline=BLK,width=3); d.text((x+52,y+61),'?',font=k.A(48),fill=WHT,anchor='mm',stroke_width=3,stroke_fill=BLK)
            d.text((x+108,y+32),n,font=k.A(34),fill=PINK,anchor='lm')
            ls=wrap(d,q,k.P(27),460); 
            for j,l in enumerate(ls): d.text((x+108,y+72+j*32-(len(ls)-1)*10),l,font=k.P(27),fill=BLK,anchor='lm')
        frac=max(0,1-u/(T2-T1)); d.rounded_rectangle([60,1005,600,1031],radius=13,fill=WHT,outline=BLK,width=4)
        if frac>0: d.rounded_rectangle([64,1009,64+int(532*frac),1027],radius=9,fill=PINK)
        return im
    u=t-T2; im=END.copy(); d=ImageDraw.Draw(im); e=ease(u/0.25); cw=int(cover.width*(0.85+0.15*e)); c=cover.resize((cw,int(cover.height*cw/cover.width)))
    d.rectangle([330-cw//2-5,125,330+cw//2+4,130+c.height+4],fill=BLK); im.paste(c,(330-cw//2,130)); d=ImageDraw.Draw(im)
    ctext(d,865,'¿QUIÉN HA SIDO?',k.A(64),WHT,6); ctext(d,935,'Dímelo en comentarios',k.P(32),BLK); ctext(d,1005,'EN AMAZON',k.A(52),PINK,5)
    return im
render(frame,DUR,B+'copa_v.mp4',cover_t=0.9,cover_path='libro_navidad/V_copa_portada.jpg')
sx=Sfx(DUR); sx.boom(0); sx.pop(0.6); sx.whoosh(T1-0.15); sx.boom(T1,0.6,90)
for i in range(5): sx.pop(T1+0.15*i,0.3)
for j in range(2,7): sx.tick(T1+j,1500+j*100,0.3)
sx.whoosh(T2-0.15); sx.ding(T2); sx.save(B+'copa.wav')
mux(B+'copa_v.mp4',B+'copa.wav',DUR,'libro_navidad/V_copa.mp4')
sheet('libro_navidad/V_copa.mp4',[0.1,0.9,1.5,2.5,5,8.0,8.6,9.5],B+'hoja_copa.png'); print('ok',DUR)
