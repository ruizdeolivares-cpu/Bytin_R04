import pymupdf, json, random, re, itertools, collections, unicodedata, sys
exec(open('../ease.py').read())
exec(open('../kakuro.py').read().replace('def solve(','def ksolve('))
exec(open('../futo.py').read().replace('def solve(','def fsolve('))
FR='../fonts/Poppins-400.ttf'; FBf='../fonts/Poppins-700.ttf'
src=pymupdf.open('pt1.pdf'); out=pymupdf.open('pt1.pdf')
CAT=json.load(open('cat.json')); sol=CAT['sol']; puz=CAT['puz']
def pick(cells,k,seed):
    rnd=random.Random(seed)
    for _ in range(3000):
        a=rnd.sample(cells,k); rows=[r for r,c in a]; cols=[c for r,c in a]
        if max(rows.count(i) for i in set(rows))<=2 and max(cols.count(i) for i in set(cols))<=2: return a
    return rnd.sample(cells,k)
# 1 SUDOKUS
target={7:38,13:37,18:36,27:35,34:35,43:35,53:34,62:34,73:33,78:33,96:33}
for p,tg in target.items():
    pg=out[p-1]; g=puz[f"{p}.0"]; xs,ys=g['xs'],g['ys']
    G=[[v if v else None for v in r] for r in g['G']]
    syms=sorted(set(v for r in G for v in r if v)); syms=syms if len(syms)==9 else [str(i) for i in range(1,10)]
    c,S=count_solutions(G,syms)
    empt=[(r,cc) for r in range(9) for cc in range(9) if G[r][cc] is None]; need=tg-(81-len(empt)); rnd=random.Random(p); add=None
    for mb in (3,2,1):
        for _ in range(3000):
            a=rnd.sample(empt,need) if need>0 else []; H=[row[:] for row in G]
            for r,cc in a: H[r][cc]=S[r][cc]
            boxes=[sum(1 for r in range(3*x,3*x+3) for cc in range(3*y,3*y+3) if H[r][cc]) for x in range(3) for y in range(3)]
            if min(boxes)>=mb and singles_solvable(H,syms): add=a; break
        if add is not None: break
    s,dy,size,col=ref_span(src[p-1],xs,ys)
    for r,cc in add: put(pg,xs[cc],xs[cc+1],ys[r],dy,S[r][cc],size)
    LOG.append(f"Sudoku p{p}: {81-len(empt)} → {81-len(empt)+len(add)} números")
# 2 KAKUROS
for p in [22,31,40,46,59,64,75,94]:
    pg=out[p-1]
    if p==94:
        T,A,Dn,V=read_kakuro(src[p-1]); R=runs(T,A,Dn)
        rs=[x['rect'] for x in src[p-1].get_drawings() if x.get('fill') is not None and 20<x['rect'].width<45 and abs(x['rect'].width-x['rect'].height)<0.6]
        s=sorted(r.width for r in rs)[len(rs)//2]; X0=min(r.x0 for r in rs); Y0=min(r.y0 for r in rs)
        xs=[X0+k*s for k in range(len(T[0])+1)]; ys=[Y0+k*s for k in range(len(T)+1)]
    else:
        g=puz[f"{p}.0"]; xs,ys=g['xs'],g['ys']; T,A,Dn,V=read_kakuro2(src[p-1],xs,ys); R=runs(T,A,Dn); s=xs[1]-xs[0]
    c,S=ksolve(T,R); W=[(i,j) for i in range(len(T)) for j in range(len(T[0])) if T[i][j]=='W']; k=round(len(W)*0.27)
    for i,j in pick(W,k,p): put(pg,xs[j],xs[j]+s,ys[i],s*0.68,str(S[(i,j)]),s*0.45)
    LOG.append(f"Kakuro p{p}: +{k} cifras de {len(W)}")
# 3 FUTOSHIKIS
for p in [24,41,54,68]:
    pg=out[p-1]; n,G,cons=read_futo(src[p-1]); c,S=fsolve(n,G,cons)
    rs=[x['rect'] for x in src[p-1].get_drawings() if x.get('fill') is None and 25<x['rect'].width<50 and abs(x['rect'].width-x['rect'].height)<0.6]
    s=rs[0].width; xs=sorted(set(round(r.x0,1) for r in rs)); ys=sorted(set(round(r.y0,1) for r in rs))
    k=4 if n==5 else 6; cells=[(i,j) for i in range(n) for j in range(n) if not G[i][j]]
    for i,j in pick(cells,k,p):
        pg.draw_rect(pymupdf.Rect(xs[j],ys[i],xs[j]+s,ys[i]+s),color=None,fill=(0.9,0.9,0.9),overlay=False)
        put(pg,xs[j],xs[j]+s,ys[i],s*0.68,str(S[i][j]),s*0.45)
    LOG.append(f"Futoshiki p{p}: +{k} números")
# 4 RASCACIELOS
sky={9:['2134','4213','1342','3421'],69:['43521','15432','52314','24153','31245']}
for p,Rr in sky.items():
    pg=out[p-1]; n=len(Rr)
    if p==9:
        rs=[x['rect'] for x in src[p-1].get_drawings() if abs(x['rect'].width-44)<0.5 and abs(x['rect'].height-44)<0.5]
        s=44.0; xs=sorted(set(round(r.x0,1) for r in rs))+[0]; ys=sorted(set(round(r.y0,1) for r in rs))+[0]
    else:
        s=40.0; xs=[123+40*k for k in range(6)]; ys=[165+40*k for k in range(6)]
    k=3 if n==4 else 5
    for i,j in pick([(i,j) for i in range(n) for j in range(n)],k,p): put(pg,xs[j],xs[j]+s,ys[i],s*0.68,Rr[i][j],s*0.45)
    LOG.append(f"Rascacielos p{p}: +{k} alturas")
# 5 NONOGRAMAS
NS=json.load(open('nono_sol.json'))
for p in [12,20,26,37,45,47,55,66,76]:
    pg=out[p-1]; g=puz[f"{p}.0"]; xs,ys=g['xs'],g['ys']; G=NS[str(p)]
    blacks=[(i,j) for i in range(len(G)) for j in range(len(G[0])) if G[i][j]==1]
    k=round(len(blacks)*(0.10 if p==12 else 0.15))
    for i,j in random.Random(p).sample(blacks,k):
        pg.draw_rect(pymupdf.Rect(xs[j]+0.6,ys[i]+0.6,xs[j+1]-0.6,ys[i+1]-0.6),color=None,fill=(0,0,0))
    LOG.append(f"Nonograma p{p}: {k} casillas pintadas de regalo")
out.save('pt1_tmp1.pdf'); print('\n'.join(LOG))
