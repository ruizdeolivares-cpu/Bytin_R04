import pymupdf, itertools
def read_kakuro(pg):
    dr=pg.get_drawings()
    rs=[x for x in dr if x.get('fill') is not None and 15<x["rect"].width<45 and abs(x['rect'].width-x['rect'].height)<0.6]
    if not rs: return None
    s=round(sorted(x['rect'].width for x in rs)[len(rs)//2],1)
    rs=[x for x in rs if abs(x['rect'].width-s)<0.6]
    X0=min(x['rect'].x0 for x in rs); Y0=min(x['rect'].y0 for x in rs)
    n=round((max(x['rect'].x1 for x in rs)-X0)/s); m=round((max(x['rect'].y1 for x in rs)-Y0)/s)
    T=[[None]*n for _ in range(m)]
    for x in rs:
        j=round((x['rect'].x0-X0)/s); i=round((x['rect'].y0-Y0)/s)
        T[i][j]='W' if sum(x['fill'])>2.5 else 'B'
    words=pg.get_text('words'); V=[[None]*n for _ in range(m)]; A=[[None]*n for _ in range(m)]; D=[[None]*n for _ in range(m)]
    for w in words:
        if not w[4].isdigit(): continue
        cx=(w[0]+w[2])/2; cy=(w[1]+w[3])/2
        j=int((cx-X0)//s); i=int((cy-Y0)//s)
        if 0<=i<m and 0<=j<n:
            if T[i][j]=='W': V[i][j]=int(w[4])
            elif T[i][j]=='B':
                ry=(cy-Y0)-i*s; rx=(cx-X0)-j*s
                if ry<s/2 and rx>s/2: A[i][j]=int(w[4])
                else: D[i][j]=int(w[4])
    return T,A,D,V
def runs(T,A,D):
    m=len(T); n=len(T[0]); R=[]
    for i in range(m):
        for j in range(n):
            if T[i][j]=='B':
                if A[i][j]:
                    cells=[];k=j+1
                    while k<n and T[i][k]=='W': cells.append((i,k)); k+=1
                    R.append((A[i][j],cells,'H',i,j))
                if D[i][j]:
                    cells=[];k=i+1
                    while k<m and T[k][j]=='W': cells.append((k,j)); k+=1
                    R.append((D[i][j],cells,'V',i,j))
    return R
def solve(T,R,limit=2):
    W=[(i,j) for i in range(len(T)) for j in range(len(T[0])) if T[i][j]=='W']
    byc={c:[r for r in R if c in r[1]] for c in W}
    sol={}; cnt=[0]; last=[None]
    def okrun(r):
        vals=[sol[c] for c in r[1] if c in sol]
        if len(vals)!=len(set(vals)): return False
        rem=len(r[1])-len(vals); s=r[0]-sum(vals)
        if rem==0: return s==0
        avail=[d for d in range(1,10) if d not in vals]
        return sum(avail[:rem])<=s<=sum(avail[-rem:])
    order=sorted(W,key=lambda c:-len(byc[c]))
    def rec(k):
        if cnt[0]>=limit: return
        if k==len(order): cnt[0]+=1; last[0]=dict(sol); return
        c=order[k]
        for d in range(1,10):
            sol[c]=d
            if all(okrun(r) for r in byc[c]): rec(k+1)
            del sol[c]
    rec(0); return cnt[0], last[0]
