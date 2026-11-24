from functools import lru_cache
def line_options(clue,n,known):
    # returns (canBlack, canWhite) arrays via DP; known: list of -1/0/1
    clue=tuple(c for c in clue if c>0); k=len(clue)
    @lru_cache(None)
    def ok(i,j):  # can fill cells i.. with blocks j..
        if j==k: return all(known[t]!=1 for t in range(i,n))
        L=clue[j]; res=False
        for s in range(i,n-L+1):
            if any(known[t]==1 for t in range(i,s)): break
            if all(known[t]!=0 for t in range(s,s+L)) and (s+L==n or known[s+L]!=1):
                if ok(min(s+L+1,n) if s+L<n else n, j+1): return True
        return False
    if not ok(0,0): return None
    cb=[False]*n; cw=[False]*n
    @lru_cache(None)
    def mark(i,j):
        if j==k:
            if all(known[t]!=1 for t in range(i,n)):
                for t in range(i,n): cw[t]=True
                return True
            return False
        L=clue[j]; any_=False
        for s in range(i,n-L+1):
            if any(known[t]==1 for t in range(i,s)): break
            if all(known[t]!=0 for t in range(s,s+L)) and (s+L==n or known[s+L]!=1):
                nxt=s+L+1 if s+L<n else n
                if mark(nxt,j+1):
                    any_=True
                    for t in range(i,s): cw[t]=True
                    for t in range(s,s+L): cb[t]=True
                    if s+L<n: cw[s+L]=True
        return any_
    mark(0,0)
    return cb,cw
def propagate(G,rows,cols):
    m,n=len(rows),len(cols); changed=True
    while changed:
        changed=False
        for i in range(m):
            r=line_options(rows[i],n,tuple(G[i]))
            if r is None: return False
            cb,cw=r
            for j in range(n):
                if G[i][j]==-1 and cb[j]!=cw[j]: G[i][j]=1 if cb[j] else 0; changed=True
        for j in range(n):
            col=tuple(G[i][j] for i in range(m)); r=line_options(cols[j],m,col)
            if r is None: return False
            cb,cw=r
            for i in range(m):
                if G[i][j]==-1 and cb[i]!=cw[i]: G[i][j]=1 if cb[i] else 0; changed=True
    return True
def count(rows,cols,limit=2):
    m,n=len(rows),len(cols); sols=[]; lineonly=[None]
    def rec(G,depth):
        if len(sols)>=limit: return
        if not propagate(G,rows,cols): return
        if lineonly[0] is None: lineonly[0]=sum(v==-1 for r in G for v in r)
        for i in range(m):
            for j in range(n):
                if G[i][j]==-1:
                    for v in (1,0):
                        H=[r[:] for r in G]; H[i][j]=v; rec(H,depth+1)
                    return
        sols.append(G)
    rec([[-1]*n for _ in range(m)],0)
    return len(sols), lineonly[0]
