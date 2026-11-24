import pymupdf, collections, itertools, re, math
def read_calc(pg, ymin=0):
    segs=[]
    for x in pg.get_drawings():
        w=x.get('width') or 0
        for it in x['items']:
            if it[0]=='l': segs.append((it[1],it[2],w))
            if it[0]=='re':
                r=it[1]; P=pymupdf.Point
                for a,b in [((r.x0,r.y0),(r.x1,r.y0)),((r.x1,r.y0),(r.x1,r.y1)),((r.x0,r.y1),(r.x1,r.y1)),((r.x0,r.y0),(r.x0,r.y1))]:
                    segs.append((P(*a),P(*b),w))
    thin=[s for s in segs if 0.3<s[2]<0.6 and s[0].y>ymin]
    L=collections.Counter(round(abs(s[0].x-s[1].x)+abs(s[0].y-s[1].y)) for s in thin); cs=L.most_common(1)[0][0]
    thin=[s for s in thin if abs(abs(s[0].x-s[1].x)+abs(s[0].y-s[1].y)-cs)<1]
    X0=min(min(s[0].x,s[1].x) for s in thin); Y0=min(min(s[0].y,s[1].y) for s in thin)
    X1=max(max(s[0].x,s[1].x) for s in thin); Y1=max(max(s[0].y,s[1].y) for s in thin)
    n=round((X1-X0)/cs)
    thick=[s for s in segs if s[2]>=2.0]
    def has_thick(x0,y0,x1,y1):
        for a,b,w in thick:
            ax,bx=sorted([a.x,b.x]); ay,by=sorted([a.y,b.y])
            if abs(x0-x1)<0.5 and abs(ax-x0)<1 and abs(bx-x0)<1 and ay<=min(y0,y1)+1 and by>=max(y0,y1)-1: return True
            if abs(y0-y1)<0.5 and abs(ay-y0)<1 and abs(by-y0)<1 and ax<=min(x0,x1)+1 and bx>=max(x0,x1)-1: return True
        return False
    par={(i,j):(i,j) for i in range(n) for j in range(n)}
    def f(a):
        while par[a]!=a: a=par[a]
        return a
    for i in range(n):
        for j in range(n):
            if j+1<n and not has_thick(X0+(j+1)*cs,Y0+i*cs,X0+(j+1)*cs,Y0+(i+1)*cs): par[f((i,j))]=f((i,j+1))
            if i+1<n and not has_thick(X0+j*cs,Y0+(i+1)*cs,X0+(j+1)*cs,Y0+(i+1)*cs): par[f((i,j))]=f((i+1,j))
    cages=collections.defaultdict(list)
    for c in par: cages[f(c)].append(c)
    labels={}
    for w in pg.get_text('words'):
        cx=(w[0]+w[2])/2; cy=(w[1]+w[3])/2
        if X0<cx<X1 and Y0<cy<Y1:
            labels[(int((cy-Y0)//cs),int((cx-X0)//cs))]=w[4]
    out=[]
    for k,cl in cages.items():
        lab=[labels[c] for c in cl if c in labels]
        out.append((sorted(cl),lab[0] if lab else None))
    return n,out
def cage_ok(vals,lab,complete):
    m=re.match(r'(\d+)([+×x\-−÷/]?)',lab); t=int(m.group(1)); op=m.group(2)
    if not complete:
        if op=='+' : return sum(vals)<t
        if op in '×x': return t%math.prod(vals)==0
        return True
    if op=='+': return sum(vals)==t
    if op in '×x': return math.prod(vals)==t
    if op in '-−': return len(vals)==2 and abs(vals[0]-vals[1])==t
    if op in '÷/': return len(vals)==2 and max(vals)/min(vals)==t
    return len(vals)==1 and vals[0]==t
def solve(n,cages,limit=2):
    G={}; cnt=[0]; last=[None]
    cellcage={c:(cl,lab) for cl,lab in cages for c in cl}
    order=[(i,j) for i in range(n) for j in range(n)]
    def rec(k):
        if cnt[0]>=limit: return
        if k==len(order): cnt[0]+=1; last[0]=dict(G); return
        i,j=order[k]
        for v in range(1,n+1):
            if any(G.get((i,c))==v for c in range(n)) or any(G.get((r,j))==v for r in range(n)): continue
            G[(i,j)]=v; cl,lab=cellcage[(i,j)]; vals=[G[c] for c in cl if c in G]
            if cage_ok(vals,lab,len(vals)==len(cl)): rec(k+1)
            del G[(i,j)]
    rec(0); return cnt[0],last[0]
