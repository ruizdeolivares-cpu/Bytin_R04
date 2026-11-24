import pymupdf, json
exec(open('../ease.py').read())
d=pymupdf.open('nav.pdf')
C=json.load(open('cat.json')); sol=C['sol']; puz=C['puz']
GRAY=(0.9,0.9,0.9)
def add_given(pg, xs, ys, i, j, txt, size, dy, shade=True):
    r=pymupdf.Rect(xs[j],ys[i],xs[j+1],ys[i+1])
    if shade: pg.draw_rect(r, color=None, fill=GRAY, overlay=False)
    put(pg, r.x0, r.x1, r.y0, dy, txt, size)
# sudokus
ps=json.load(open('plan_sudoku.json'))
for p,add in ps.items():
    p=int(p); pg=d[p-1]; xs,ys=puz[f"{p}.0"]['xs'],puz[f"{p}.0"]['ys']
    s,dy,size,col=ref_span(pg,xs,ys)
    S=[sol[k]['G'] for k in sol if k.split()[0]==str(p)][0]
    for r,c in add: add_given(pg,xs,ys,r,c,S[r][c],size,dy)
    LOG.append(f"Sudoku p{p}: +{len(add)} números")
pc=json.load(open('plan_cunadoku.json'))
for key,add in pc.items():
    p=int(key.split('.')[0]); pg=d[p-1]; xs,ys=puz[key]['xs'],puz[key]['ys']
    s,dy,size,col=ref_span(pg,xs,ys)
    for r,c,v in add: add_given(pg,xs,ys,r,c,str(v),size,dy)
    LOG.append(f"Cuñadoku p{p}.{key[-1]}: +{len(add)} números verdaderos")
d.save('nav_facil_tmp1.pdf'); print('\n'.join(LOG))
