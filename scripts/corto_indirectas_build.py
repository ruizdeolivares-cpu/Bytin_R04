# «Traductor de indirectas» (libro 1, pág. 10 «Traduce la indirecta»; soluciones pág. Archivo: 2-H, 3-C, 6-D). ~8 s.
import sys; sys.path.insert(0,'scripts'); from cortos_lib import *
S=sys.argv[1]; k=K(S); B=S+'/cortos/'
R='docs/libro1_reparto/'
PAIRS=[('1A_dona_remedios','«No pasa nada.»','Ha pasado de todo. Y me lo apunto.',(255,45,150),(225,25,125)),
       ('2A_vanessa','«Qué valiente, ponerte eso.»','Te queda fatal.',(0,180,225),(0,155,200)),
       ('4A_charo','«Me alegro muchísimo por ti.»','Me muero de envidia.',(130,70,210),(110,55,185))]
SEG=2.35; T_END=SEG*3; DUR=T_END+1.3
BGS=[dots(c,dc) for _,_,_,c,dc in PAIRS]
IMG={}
for n,_,_,_,_ in PAIRS:
    im=Image.open(R+n+'.png').convert('RGB'); im=im.crop((0,0,im.width,min(im.height,int(im.width*1.2)))) # parte de arriba (cara y cuerpo)
    IMG[n]=im.resize((540,int(540*im.height/im.width)),Image.LANCZOS)
cover=Image.open('libro_pt1/portada_nueva_frontal.png').convert('RGB'); cover=cover.resize((int(cover.width*660/cover.height),660),Image.LANCZOS)
END_BG=dots(YEL,(245,205,0))
def frame(t):
    if t<T_END:
        i=int(t//SEG); u=t-i*SEG; n,dice,quiere,_,_=PAIRS[i]
        im=BGS[i].copy(); d=ImageDraw.Draw(im)
        ctext(d,150,'TRADUCTOR DE INDIRECTAS',k.A(54),YEL,6)
        p=IMG[n]; e=ease(u/0.25); y=640+int((1-e)*300)
        d.rectangle([330-p.width//2-6,y-6,330+p.width//2+5,H],fill=BLK); im.paste(p,(330-p.width//2,y)); d=ImageDraw.Draw(im)
        s=pop(u/0.3); ctext(d,222,'LO QUE DICE:',k.P(26),WHT,3)
        yb=box_top(d,245,dice,k.P(42*s),BLK,WHT,maxw=540)
        if u>0.85:
            s2=pop((u-0.85)/0.3); ctext(d,yb+38,'LO QUE QUIERE DECIR:',k.P(26),YEL,3)
            box_top(d,yb+62,quiere.upper(),k.A(56*s2),BLK,YEL,maxw=560)
        return im
    u=t-T_END; im=END_BG.copy(); d=ImageDraw.Draw(im); e=ease(u/0.25); cw=int(cover.width*(0.85+0.15*e)); c=cover.resize((cw,int(cover.height*cw/cover.width)))
    d.rectangle([330-cw//2-5,125,330+cw//2+4,130+c.height+4],fill=BLK); im.paste(c,(330-cw//2,130)); d=ImageDraw.Draw(im)
    ctext(d,860,'¿CUÁL TE HAN DICHO A TI?',k.A(52),WHT,6); ctext(d,930,'Pasatiempos tóxicos · en Amazon',k.P(30),BLK)
    return im
render(frame,DUR,B+'ind_v.mp4',cover_t=1.6,cover_path='libro_pt1/V_indirectas_portada.jpg')
sx=Sfx(DUR); sx.boom(0)
for i in range(3):
    t=i*SEG
    if i: sx.whoosh(t-0.15)
    sx.pop(t+0.05); sx.buzz(t+0.85,0.25)
sx.whoosh(T_END-0.15); sx.ding(T_END); sx.save(B+'ind.wav')
mux(B+'ind_v.mp4',B+'ind.wav',DUR,'libro_pt1/V_indirectas.mp4')
sheet('libro_pt1/V_indirectas.mp4',[0.1,0.5,1.5,2.9,4.0,5.4,6.6,7.6],B+'hoja_ind.png'); print('ok',DUR)
