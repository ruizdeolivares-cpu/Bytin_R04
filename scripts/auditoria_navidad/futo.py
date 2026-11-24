import pymupdf, itertools
def read_futo(pg):
    rs=[x['rect'] for x in pg.get_drawings() if x.get('fill') is None and 25<x['rect'].width<50 and abs(x['rect'].width-x['rect'].height)<0.6]
    s=rs[0].width; X0=min(r.x0 for r in rs); Y0=min(r.y0 for r in rs)
    xs=sorted(set(round(r.x0,1) for r in rs)); ys=sorted(set(round(r.y0,1) for r in rs)); n=len(xs)
    def col(x): return min(range(len(xs)),key=lambda k:abs(xs[k]+s/2-x))
    def row(y): return min(range(len(ys)),key=lambda k:abs(ys[k]+s/2-y))
    G=[[None]*n for _ in range(n)]; cons=[]
    for w in pg.get_text('words'):
        cx=(w[0]+w[2])/2; cy=(w[1]+w[3])/2
        if not (xs[0]-2<cx<xs[-1]+s+2 and ys[0]-2<cy<ys[-1]+s+2): continue
        inx=[k for k in range(n) if xs[k]<=cx<=xs[k]+s]; iny=[k for k in range(n) if ys[k]<=cy<=ys[k]+s]
        t=w[4]
        if t.isdigit() and inx and iny: G[iny[0]][inx[0]]=int(t)
        elif t in '<>' and iny:
            j=max(k for k in range(n) if xs[k]+s<=cx+1); i=iny[0]
            cons.append(((i,j),(i,j+1)) if t=='>' else ((i,j+1),(i,j)))  # (bigger, smaller)
        elif t in '∧∨' and inx:
            i=max(k for k in range(n) if ys[k]+s<=cy+1); j=inx[0]
            cons.append(((i+1,j),(i,j)) if t=='∧' else ((i,j),(i+1,j)))
    return n,G,cons
def solve(n,G,cons,limit=2):
    cnt=[0]; last=[None]; G=[r[:] for r in G]
    cells=[(i,j) for i in range(n) for j in range(n)]
    def ok(i,j):
        v=G[i][j]
        if any(G[i][k]==v for k in range(n) if k!=j) or any(G[k][j]==v for k in range(n) if k!=i): return False
        for a,b in cons:
            if G[a[0]][a[1]] and G[b[0]][b[1]] and not G[a[0]][a[1]]>G[b[0]][b[1]]: return False
        return True
    def rec(k):
        if cnt[0]>=limit: return
        if k==len(cells): cnt[0]+=1; last[0]=[r[:] for r in G]; return
        i,j=cells[k]
        if G[i][j]: 
            if ok(i,j): rec(k+1)
            return
        for v in range(1,n+1):
            G[i][j]=v
            if ok(i,j): rec(k+1)
            G[i][j]=None
    rec(0); return cnt[0],last[0]
