# «¿Qué cuñado eres?» (Navidad, test pág. 6 pregunta 8 «Tu frase estrella» + diagnóstico pág. 7). ~8,6 s.
import sys; sys.path.insert(0,'scripts'); from cortos_lib import *
S=sys.argv[1]; k=K(S); B=S+'/cortos/'
T1,T2,T3=1.1,4.6,7.3; DUR=T3+1.3
ab=Image.open('libro_navidad/v01_inicio/P2a_abuela.png').convert('RGB').resize((W,H),Image.LANCZOS)
OPC=[('A','«Eso te lo arreglo yo en cinco minutos.»','EL CUÑADO ENTERAO'),('B','«¿Eso te lo vas a comer?»','EL CUÑADO GORRÓN'),('C','«Bueno, yo ya me iba…»','EL CUÑADO FANTASMA')]
COL=[PINK,CYAN,PURP]
BG=dots((255,240,225),(250,222,200)); cover=Image.open('libro_navidad/portada.png').convert('RGB'); cover=cover.resize((int(cover.width*660/cover.height),660),Image.LANCZOS); END=dots(YEL,(245,205,0))
face=circle(Image.open('libro_navidad/v01_inicio/P2a_abuela.png').convert('RGB'),(220,760,600,1140),110)
def opts(im,d,u,reveal):
    for i,(L,f,dg) in enumerate(OPC):
        a=ease((u-0.35*i)/0.25)
        if a<=0: continue
        y=330+i*235; x=40+int((1-a)*500)
        d.rounded_rectangle([x,y,x+580,y+205],radius=22,fill=WHT,outline=BLK,width=5)
        d.ellipse([x+18,y+57,x+108,y+147],fill=COL[i],outline=BLK,width=4); d.text((x+63,y+102),L,font=k.A(56),fill=WHT,anchor='mm',stroke_width=3,stroke_fill=BLK)
        if reveal<=0:
            ls=wrap(d,f,k.P(33),430)
            for j,l in enumerate(ls): d.text((x+128,y+102+(j-(len(ls)-1)/2)*38),l,font=k.P(33),fill=BLK,anchor='lm')
        else:
            s=pop((reveal-0.25*i)/0.3) if reveal>0.25*i else 0
            if s: d.text((x+128,y+102),dg,font=k.A(44*s),fill=COL[i],anchor='lm')
            else:
                ls=wrap(d,f,k.P(33),430)
                for j,l in enumerate(ls): d.text((x+128,y+102+(j-(len(ls)-1)/2)*38),l,font=k.P(33),fill=BLK,anchor='lm')
def frame(t):
    if t<T1:
        z=1+0.07*t/T1; im=ab.resize((int(W*z),int(H*z)),Image.LANCZOS); x=(im.width-W)//2; im=im.crop((x,0,x+W,H)); d=ImageDraw.Draw(im)
        ctext(d,165,'¿QUÉ CUÑADO ERES?',k.A(74*ease(t/0.25)),WHT,7); ctext(d,250,'ELIGE RÁPIDO',k.A(70*ease((t-0.15)/0.25)),PINK,6)
        return im
    if t<T3:
        u=t-T1; im=BG.copy(); f,m=face; im.paste(f,(40,120),m); d=ImageDraw.Draw(im); d.ellipse([37,117,153,233],outline=BLK,width=5)
        d.text((175,160),'TU FRASE ESTRELLA:',font=k.A(56),fill=BLK,anchor='lm') if t<T2 else d.text((175,160),'TU DIAGNÓSTICO:',font=k.A(56*pop((t-T2)/0.3)),fill=PINK,anchor='lm',stroke_width=3,stroke_fill=BLK)
        d.text((175,222),'Test del libro · pág. 6',font=k.P(24),fill=(90,90,90),anchor='lm')
        opts(im,d,u,t-T2 if t>=T2 else 0)
        return im
    u=t-T3; im=END.copy(); d=ImageDraw.Draw(im); e=ease(u/0.25); cw=int(cover.width*(0.85+0.15*e)); c=cover.resize((cw,int(cover.height*cw/cover.width)))
    d.rectangle([330-cw//2-5,125,330+cw//2+4,130+c.height+4],fill=BLK); im.paste(c,(330-cw//2,130)); d=ImageDraw.Draw(im)
    ctext(d,865,'¿CUÁL TE HA SALIDO?',k.A(62),WHT,6); ctext(d,935,'Comenta tu letra',k.P(32),BLK); ctext(d,1005,'EN AMAZON',k.A(52),PINK,5)
    return im
render(frame,DUR,B+'test_v.mp4',cover_t=0.8,cover_path='libro_navidad/V_test_cunado_portada.jpg')
sx=Sfx(DUR); sx.boom(0); sx.whoosh(T1-0.15)
for i in range(3): sx.pop(T1+0.35*i)
sx.boom(T2,0.6,80)
for i in range(3): sx.ding(T2+0.25*i,0.25)
sx.whoosh(T3-0.15); sx.boom(T3,0.5,70); sx.save(B+'test.wav')
mux(B+'test_v.mp4',B+'test.wav',DUR,'libro_navidad/V_test_cunado.mp4')
sheet('libro_navidad/V_test_cunado.mp4',[0.1,0.8,1.5,2.4,4.0,5.2,6.8,8.0],B+'hoja_test.png'); print('ok',DUR)
