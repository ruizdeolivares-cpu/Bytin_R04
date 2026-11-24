import pymupdf
FR='../fonts/Poppins-400.ttf'
d=pymupdf.open('nav_facil_tmp2.pdf')
REPL=[(20,'Aquí no te damos ningún número: todo sale','Te damos algunos números: el resto'),(20,'de los signos.','sale de los signos.'),
(52,'Solo diez pistas: suerte.','Diez pistas y algún regalo.'),(70,'y esta vez ninguna casilla viene dada.','y te regalamos unas casillas.'),(84,'sin ninguna casilla dada.','con algunas casillas de regalo.')]
def origin_for(pg,rect):
    for b in pg.get_text('dict')['blocks']:
        for l in b.get('lines',[]):
            for s in l['spans']:
                if pymupdf.Rect(s['bbox']).intersects(rect) and abs(s['bbox'][1]-rect.y0)<2: return s['origin'][1], s['size']
for p,old,new in REPL:
    pg=d[p-1]; rs=pg.search_for(old)
    if p==20 and old.startswith('de los'): rs=[r for r in rs if r.x0<50]
    r=rs[0]; oy,sz=origin_for(pg,r)
    pg.add_redact_annot(r, fill=False)
    pg.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)
    pg.insert_text((r.x0,oy),new,fontsize=sz,fontfile=FR,fontname='PopR',color=(0,0,0))
    print(p,'ok',new)
d.save('nav_facil_tmp3.pdf')
