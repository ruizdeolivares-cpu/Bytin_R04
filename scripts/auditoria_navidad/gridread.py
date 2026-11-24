import pymupdf, re, collections
def grids(pg, minn=3):
    hs=collections.defaultdict(set); vs=collections.defaultdict(set)
    for x in pg.get_drawings():
        for it in x['items']:
            if it[0]=='l':
                p,q=it[1],it[2]
                if abs(p.y-q.y)<0.2 and abs(p.x-q.x)>15: hs[(round(min(p.x,q.x)),round(max(p.x,q.x)))].add(round(p.y,1))
                if abs(p.x-q.x)<0.2 and abs(p.y-q.y)>15: vs[(round(min(p.y,q.y)),round(max(p.y,q.y)))].add(round(p.x,1))
            if it[0]=='re':
                r=it[1]
                if r.width>15 and r.height>15:
                    hs[(round(r.x0),round(r.x1))].update([round(r.y0,1),round(r.y1,1)])
                    vs[(round(r.y0),round(r.y1))].update([round(r.x0,1),round(r.x1,1)])
    out=[]
    for (x0,x1),ys in hs.items():
        ys=sorted(ys)
        for (y0,y1),xs0 in vs.items():
            xs=sorted(v for v in xs0 if x0-2<=v<=x1+2)
            ysf=[v for v in ys if y0-2<=v<=y1+2]
            if not xs or len(ysf)<2: continue
            ys_=ysf
            if abs(y0-ys_[0])<2 and abs(y1-ys_[-1])<2 and abs(xs[0]-x0)<2 and abs(xs[-1]-x1)<2 and len(xs)>minn and len(ys_)>minn:
                out.append((xs,ys_)); continue
            if False and abs(y0-ys[0])<2 and abs(y1-ys[-1])<2 and abs(xs[0]-x0)<2 and abs(xs[-1]-x1)<2 and len(xs)>minn and len(ys)>minn:
                out.append((xs,ys))
    # dedupe
    # rect lattices (kakuro etc.)
    rects=collections.defaultdict(list)
    for x in pg.get_drawings():
        r=x['rect']
        if 12<r.width<40 and abs(r.width-r.height)<0.5 and any(i[0]=='re' for i in x['items']) and x.get('width'):
            rects[round(r.width)].append(r)
    for s_,rs in rects.items():
        used=set()
        for i,r in enumerate(rs):
            if i in used: continue
            comp=[i]; stack=[i]; used.add(i)
            while stack:
                a=rs[stack.pop()]
                for j,b in enumerate(rs):
                    if j not in used and abs(a.x0-b.x0)<=s_+1 and abs(a.y0-b.y0)<=s_+1:
                        used.add(j); comp.append(j); stack.append(j)
            if len(comp)>=9:
                X0=min(rs[k].x0 for k in comp); Y0=min(rs[k].y0 for k in comp)
                X1=max(rs[k].x1 for k in comp); Y1=max(rs[k].y1 for k in comp)
                n=round((X1-X0)/s_); m=round((Y1-Y0)/s_)
                out.append(([X0+k*(X1-X0)/n for k in range(n+1)],[Y0+k*(Y1-Y0)/m for k in range(m+1)]))
    res=[]
    for g in out:
        if not any(abs(g[0][0]-h[0][0])<1 and abs(g[1][0]-h[1][0])<1 for h in res): res.append(g)
    return res
def cells(pg, g):
    xs,ys=g; words=pg.get_text('words'); n=len(xs)-1; m=len(ys)-1
    G=[['' for _ in range(n)] for _ in range(m)]
    for w in words:
        cx=(w[0]+w[2])/2; cy=(w[1]+w[3])/2
        if xs[0]<cx<xs[-1] and ys[0]<cy<ys[-1]:
            j=max(k for k in range(n) if xs[k]<=cx); i=max(k for k in range(m) if ys[k]<=cy)
            G[i][j]=(G[i][j]+' '+w[4]).strip()
    return G
def label_above(pg,g,dy=16):
    xs,ys=g; ws=[w for w in pg.get_text('words') if ys[0]-dy<w[3]<=ys[0]+1 and xs[0]-5<w[0]<xs[-1]]
    return ' '.join(w[4] for w in sorted(ws,key=lambda w:w[0]))
