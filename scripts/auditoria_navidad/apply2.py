import pymupdf, json, random, itertools
exec(open('../ease.py').read()); exec(open('../futo.py').read().replace('def solve(','def fsolve('))
exec(open('../calc.py').read().replace('def solve(','def csolve('))
exec(open('../kakuro.py').read().replace('def solve(','def ksolve('))
d=pymupdf.open('nav_facil_tmp1.pdf')
def lattice(pg, smin, smax, wmin=0.0, need_fill=None):
    rs=[x['rect'] for x in pg.get_drawings() if smin<x['rect'].width<smax and abs(x['rect'].width-x['rect'].height)<0.6 and (x.get('width') or 0)>=wmin and (need_fill is None or (x.get('fill') is not None)==need_fill)]
    s=sorted(r.width for r in rs)[len(rs)//2]
    xs=sorted(set(round(r.x0,1) for r in rs)); ys=sorted(set(round(r.y0,1) for r in rs))
    return xs,ys,s
def pick(n,cells,k,seed):
    rnd=random.Random(seed)
    for _ in range(2000):
        a=rnd.sample(cells,k)
        rows=[r for r,c in a]; cols=[c for r,c in a]
        if max(rows.count(i) for i in set(rows))<=2 and max(cols.count(i) for i in set(cols))<=2: return a
    return rnd.sample(cells,k)
def draw(pg,x0,y0,s,txt,size,yfrac=0.68,xoff=0):
    put(pg,x0+xoff,x0+s+xoff,y0,s*yfrac,txt,size)
# FUTOSHIKI (solve on original geometry)
for p in [20,33,49,69,88]:
    pg=d[p-1]; n,G,cons=read_futo(pg); c,S=fsolve(n,G,cons); xs,ys,s=lattice(pg,25,50,0.5,False)
    k=5 if n==5 else 7
    cells=[(i,j) for i in range(n) for j in range(n) if not G[i][j]]
    for i,j in pick(n,cells,k,p): draw(pg,xs[j],ys[i],s,str(S[i][j]),s*0.45)
    LOG.append(f"Futoshiki p{p}: +{k} números")
# CALCUDOKU
for p,ym in [(62,250),(70,0),(84,0)]:
    pg=d[p-1]; n,cages=read_calc(pg,ym); c,S=csolve(n,cages)
    xs,ys,s=lattice(pg,40,60)
    xs=xs[-n:]; ys=ys[-n:]
    k=5 if n==5 else 7
    cells=[(i,j) for i in range(n) for j in range(n)]
    for i,j in pick(n,cells,k,p): draw(pg,xs[j],ys[i],s,str(S[(i,j)]),s*0.42,0.80)
    LOG.append(f"Calcudoku p{p}: +{k} números")
# RASCACIELOS
sky={29:['12354','45132','23415','51243','34521'],52:['462315','354126','516432','241563','123654','635241'],73:['164253','241365','526431','653142','432516','315624']}
for p,Srows in sky.items():
    pg=d[p-1]; xs,ys,s=lattice(pg,35,45,0.5); n=len(Srows)
    k=5 if n==5 else 7
    cells=[(i,j) for i in range(n) for j in range(n)]
    for i,j in pick(n,cells,k,p): draw(pg,xs[j],ys[i],s,Srows[i][j],s*0.45)
    LOG.append(f"Rascacielos p{p}: +{k} alturas")
# KAKURO
for p in [18,24,37,46,55,67,77,86]:
    pg=d[p-1]; T,A,Dn,V=read_kakuro(pg); R=runs(T,A,Dn); c,S=ksolve(T,R)
    xs,ys,s=lattice(pg,20,45,0,True)
    W=[(i,j) for i in range(len(T)) for j in range(len(T[0])) if T[i][j]=='W']
    k=round(len(W)*0.27)
    for i,j in pick(len(T),W,k,p): draw(pg,xs[j],ys[i],s,str(S[(i,j)]),s*0.45)
    LOG.append(f"Kakuro p{p}: +{k} cifras")
d.save('nav_facil_tmp2.pdf'); print('\n'.join(LOG))
