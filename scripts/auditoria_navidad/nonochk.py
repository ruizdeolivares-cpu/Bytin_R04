import pymupdf, re, sys, collections
d=pymupdf.open(sys.argv[1])
def grids(pg):
    hs=collections.defaultdict(list); vs=collections.defaultdict(list)
    for x in pg.get_drawings():
        for it in x['items']:
            if it[0]=='l':
                p,q=it[1],it[2]
                if abs(p.y-q.y)<0.1 and abs(p.x-q.x)>20: hs[(round(min(p.x,q.x)),round(max(p.x,q.x)))].append(round(p.y,1))
                if abs(p.x-q.x)<0.1 and abs(p.y-q.y)>20: vs[(round(min(p.y,q.y)),round(max(p.y,q.y)))].append(round(p.x,1))
        if x.get('fill') is None and x['rect'].width>20 and x['rect'].height>20 and any(i[0]=='re' for i in x['items']):
            pass
    out=[]
    for (x0,x1),ys in hs.items():
        ys=sorted(set(ys))
        if len(ys)<4: continue
        for (y0,y1),xs in vs.items():
            xs=sorted(set(xs))
            if abs(y0-ys[0])<2 and abs(y1-ys[-1])<2 and abs(xs[0]-x0)<2 and abs(xs[-1]-x1)<2 and len(xs)>=4:
                out.append((xs,ys))
    return out
def runs(v):
    r=[];c=0
    for b in v+[0]:
        if b: c+=1
        elif c: r.append(c);c=0
    return r or [0]
def solution_grids(pn):
    pg=d[pn-1]; res=[]
    blacks=[x['rect'] for x in pg.get_drawings() if x.get('fill')==(0.0,0.0,0.0)]
    words=pg.get_text('words')
    for xs,ys in grids(pg):
        n,m=len(xs)-1,len(ys)-1; s=(xs[-1]-xs[0])/n
        G=[[0]*n for _ in range(m)]
        cnt=0
        for r in blacks:
            if abs(r.width-s)<0.5 and abs(r.height-s)<0.5:
                cx=(r.x0+r.x1)/2; cy=(r.y0+r.y1)/2
                if xs[0]<cx<xs[-1] and ys[0]<cy<ys[-1]:
                    G[int((cy-ys[0])/s)][int((cx-xs[0])/s)]=1; cnt+=1
        if cnt==0: continue
        lab=[w for w in words if w[3]<ys[0] and w[3]>ys[0]-14 and abs(w[0]-xs[0])<60]
        lab=' '.join(w[4] for w in sorted(lab,key=lambda w:w[0]))
        res.append((lab,G))
    return res
def puzzle_clues(pn):
    pg=d[pn-1]; words=pg.get_text('words'); out=[]
    for xs,ys in grids(pg):
        n,m=len(xs)-1,len(ys)-1
        if n<5: continue
        cols=[];rows=[]
        for j in range(n):
            ws=[w for w in words if w[3]<=ys[0]+1 and xs[j]<(w[0]+w[2])/2<xs[j+1] and w[1]>ys[0]-150]
            cols.append([int(w[4]) for w in sorted(ws,key=lambda w:w[1]) if w[4].isdigit()])
        for i in range(m):
            ws=[w for w in words if w[2]<=xs[0]+1 and ys[i]<(w[1]+w[3])/2<ys[i+1] and w[0]>xs[0]-120]
            rows.append([int(w[4]) for w in sorted(ws,key=lambda w:w[0]) if w[4].isdigit()])
        out.append((n,m,cols,rows))
    return out
