import pymupdf, re, unicodedata, collections, itertools
FBf='../fonts/Poppins-700.ttf'; FR='../fonts/Poppins-400.ttf'
src=pymupdf.open('pt1.pdf'); out=pymupdf.open('pt1_tmp1.pdf')
soltxt=' '.join(src[p].get_text() for p in range(79,97)).replace('\n',' ')
def norm(s): return ''.join(c for c in unicodedata.normalize('NFD',s.upper()) if unicodedata.category(c)!='Mn' or c=='̃').replace('Ñ','Ñ')
LOG=[]
for p in [8,17,23,36,42,56,63]:
    pg=src[p-1]; ws=pg.get_text('words')
    nums=[w for w in ws if w[4].isdigit() and 100<w[1]<560]
    rows={}
    for w in nums: rows.setdefault(round(w[1]),[]).append(w)
    words=[]
    for y in sorted(rows):
        r=sorted(rows[y],key=lambda w:w[0]); cur=[]
        gaps=[r[k][0]-r[k-1][0] for k in range(1,len(r))]; step=sorted(gaps)[len(gaps)//3] if gaps else 20
        for k,w in enumerate(r):
            if k and w[0]-r[k-1][0]>step*1.45: words.append(cur); cur=[]
            cur.append(w)
        words.append(cur)
    phrase=re.search(r'P\.\s*%d\s*·[^«]*«([^»]*)»'%p, soltxt).group(1)
    pw=[x for x in (re.sub('[^A-ZÑ]','',norm(x)) for x in phrase.split()) if x]; words=words[:len(pw)]
    mp={}; pos=collections.defaultdict(list)
    for a,b in zip(pw,words):
        for ch,w in zip(a,b): mp[int(w[4])]=ch; pos[int(w[4])].append(w)
    phrase_nums=[w for wd in words for w in wd]
    letters=[w for w in ws if len(w[4])==1 and w[4].isalpha() and 100<w[1]<560]
    given=set(); ref=None
    for L in letters:
        lx=(L[0]+L[2])/2
        below=[n for n in phrase_nums if abs((n[0]+n[2])/2-lx)<4 and 0<n[1]-L[1]<40]
        if below: n=min(below,key=lambda n:n[1]-L[1]); given.add(int(n[4])); ref=(L,n)
    sp=[s for b in pg.get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans'] if s['text'].strip()==ref[0][4] and abs(s['bbox'][0]-ref[0][0])<1 and abs(s['bbox'][1]-ref[0][1])<1][0]
    dy=sp['origin'][1]-ref[1][1]
    cnt=collections.Counter(int(w[4]) for w in phrase_nums)
    cand=[n for n,_ in cnt.most_common() if n not in given][:3]
    o=out[p-1]; F=pymupdf.Font(fontfile=FBf)
    for n in cand:
        for w in pos[n]:
            cx=(w[0]+w[2])/2; tw=F.text_length(mp[n],fontsize=sp['size'])
            o.insert_text((cx-tw/2,w[1]+dy),mp[n],fontsize=sp['size'],fontfile=FBf,fontname='PopB',color=(0,0,0))
    # table: labels below phrase area
    last_y=max(w[1] for w in phrase_nums)
    tlabels=[w for w in ws if w[4].isdigit() and w[1]>last_y+15]
    tletters=[w for w in ws if len(w[4])==1 and w[4].isalpha() and w[1]>last_y+15]
    tref=None
    for L in tletters:
        lab=[t for t in tlabels if t[1]<L[1] and L[1]-t[1]<30 and abs(t[0]-L[0])<25]
        if lab:
            t=min(lab,key=lambda t:(L[1]-t[1])+abs(t[0]-L[0])); tref=(L,t); break
    if tref:
        Lw,tw_=tref
        tsp=[s for b in pg.get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans'] if s['text'].strip()==Lw[4] and abs(s['bbox'][0]-Lw[0])<1 and abs(s['bbox'][1]-Lw[1])<1][0]
        dyb=tsp['origin'][1]-tw_[1]
        rowsT=collections.defaultdict(list)
        for t in tlabels: rowsT[round(t[1])].append(t)
        for n in cand:
            labn=[t for t in tlabels if t[4]==str(n)]
            for t in labn[:1]:
                row=sorted(rowsT[round(t[1])],key=lambda q:q[0]); xs_=[q[0] for q in row]
                cw=sorted(xs_[k+1]-xs_[k] for k in range(len(xs_)-1))[len(xs_)//2]
                cx=t[0]-2.2+cw/2
                w_=F.text_length(mp[n],fontsize=tsp['size'])
                o.insert_text((cx-w_/2,t[1]+dyb),mp[n],fontsize=tsp['size'],fontfile=FBf,fontname='PopB',color=(0,0,0))
    old,new=('tres','seis') if p!=56 else ('cuatro','siete')
    for r in o.search_for('regalamos'):
      cands=[x for x in o.search_for(old) if (abs(x.y0-r.y0)<2 and x.x0>r.x1-1) or (0<x.y0-r.y0<14 and x.x0<r.x0)]
      if not cands: continue
      rr=sorted(cands,key=lambda x:(x.y0,x.x0))[0]
      nxt=o.search_for(old+'.')
      punct=''
      for q in nxt:
          if abs(q.y0-rr.y0)<1 and abs(q.x0-rr.x0)<1: rr=q; punct='.'
      span=[s for b in o.get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans'] if pymupdf.Rect(s['bbox']).y0<=(rr.y0+rr.y1)/2<=s['bbox'][3] and s['bbox'][0]<=rr.x0+1<=s['bbox'][2]][0]
      o.add_redact_annot(rr,fill=False); o.apply_redactions(images=0,graphics=0)
      c=span['color']; col=((c>>16)&255)/255,((c>>8)&255)/255,(c&255)/255
      o.insert_text((rr.x0,span['origin'][1]),new+punct,fontsize=span['size'],fontfile=FBf if 'Bold' in span['font'] else FR,fontname='PopX',color=col)
    LOG.append(f"Criptograma p{p}: regaladas antes {sorted(mp[g] for g in given)}, ahora también {[mp[n] for n in cand]}")
# SUMAS
eqs={49:[("NOTA","NOTA","PISOS"),("ODIO","MIEDO","VECINA"),("RENCOR","RENCOR","QUEJAS"),("DEUDA","SUEGRA","CABREO")],
72:[("PERRO","PERRO","CABREO"),("SUEGRA","SUEGRA","TUPPER"),("CUOTA","DEUDA","TUPPER"),("RUIDO","PAGAR","GUERRA")],
95:[("PISOS","PISOS","DEUDA"),("RUIDO","RUIDO","BRONCA"),("VECINA","VECINO","TENSION"),("DEUDA","QUEJAS","JUICIO")]}
def solve(a,b,c):
    L=sorted(set(a+b+c))
    for perm in itertools.permutations(range(10),len(L)):
        m=dict(zip(L,perm))
        if 0 in (m[a[0]],m[b[0]],m[c[0]]): continue
        n=lambda w:int(''.join(str(m[ch]) for ch in w))
        if n(a)+n(b)==n(c): return m
for p,E in eqs.items():
    pg=out[p-1]
    lines=[l for b in pg.get_text('dict')['blocks'] for l in b.get('lines',[]) if any(s['text'].strip().startswith('Apunta') for s in l['spans'])]
    lines.sort(key=lambda l:l['bbox'][1])
    toks=[w for w in pg.get_text('words') if re.match(r'^[A-ZÑ]=',w[4])]
    assert len(lines)==4,(p,len(lines))
    for (a,b,c),l in zip(E,lines):
        m=solve(a,b,c); cnt=collections.Counter(a+b+c)
        pickL=[L for L,_ in cnt.most_common() if L!=c[0]][:2]
        ly=(l['bbox'][1]+l['bbox'][3])/2
        for L in pickL:
            t=[w for w in toks if w[4].startswith(L+'=') and abs((w[1]+w[3])/2-ly)<4][0]
            allsp=[s for b2 in pg.get_text('dict')['blocks'] for l2 in b2.get('lines',[]) for s in l2['spans']]
            s0=[s for s in allsp if s['bbox'][0]-1<=t[0]<=s['bbox'][2] and abs((s['bbox'][1]+s['bbox'][3])/2-(t[1]+t[3])/2)<3][0]
            ff=FBf if 'Bold' in s0['font'] else FR
            x=t[0]+pymupdf.Font(fontfile=ff).text_length(L+'=',fontsize=s0['size'])+1.5
            pg.insert_text((x,s0['origin'][1]),str(m[L]),fontsize=s0['size']*1.1,fontfile=FBf,fontname='PopB',color=(0,0,0))
        LOG.append(f"Suma p{p} {a}+{b}={c}: regaladas {dict((L,m[L]) for L in pickL)}")
out.save('pt1_tmp2.pdf'); print('\n'.join(LOG))
