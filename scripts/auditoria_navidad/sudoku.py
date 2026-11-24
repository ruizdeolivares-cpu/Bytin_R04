import itertools
def blocks(n): return (3,3) if n==9 else (2,3)
def peers(n):
    br,bc=blocks(n); P={}
    for r in range(n):
        for c in range(n):
            s=set([(r,k) for k in range(n)]+[(k,c) for k in range(n)]+[(br*(r//br)+i,bc*(c//bc)+j) for i in range(br) for j in range(bc)]); s.discard((r,c)); P[(r,c)]=s
    return P
def count_solutions(G,syms,limit=2):
    n=len(G); P=peers(n); cnt=[0]; out=[None]
    def rec(G):
        if cnt[0]>=limit: return
        best=None
        for r in range(n):
            for c in range(n):
                if G[r][c] is None:
                    opts=[s for s in syms if all(G[a][b]!=s for a,b in P[(r,c)])]
                    if not opts: return
                    if best is None or len(opts)<len(best[2]): best=(r,c,opts)
        if best is None: cnt[0]+=1; out[0]=[row[:] for row in G]; return
        r,c,opts=best
        for s in opts: G[r][c]=s; rec(G); G[r][c]=None
    rec([row[:] for row in G]); return cnt[0],out[0]
def singles_solvable(G,syms):
    n=len(G); P=peers(n); G=[row[:] for row in G]; br,bc=blocks(n)
    units=[[(r,c) for c in range(n)] for r in range(n)]+[[(r,c) for r in range(n)] for c in range(n)]+[[(br*a+i,bc*b+j) for i in range(br) for j in range(bc)] for a in range(n//br) for b in range(n//bc)]
    prog=True
    while prog:
        prog=False
        cand={(r,c):[s for s in syms if all(G[a][b]!=s for a,b in P[(r,c)])] for r in range(n) for c in range(n) if G[r][c] is None}
        for k,v in cand.items():
            if len(v)==1: G[k[0]][k[1]]=v[0]; prog=True
        if prog: continue
        for u in units:
            for s in syms:
                pl=[k for k in u if k in cand and s in cand[k]]
                if len(pl)==1 and all(G[a][b]!=s for a,b in u): G[pl[0][0]][pl[0][1]]=s; prog=True
    return all(v is not None for row in G for v in row)
def valid(S):
    n=len(S); syms=set(S[0])
    if any(set(r)!=syms for r in S) or any(set(S[r][c] for r in range(n))!=syms for c in range(n)): return False
    br,bc=blocks(n)
    return all(set(S[br*a+i][bc*b+j] for i in range(br) for j in range(bc))==syms for a in range(n//br) for b in range(n//bc))
