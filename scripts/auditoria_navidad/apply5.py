import pymupdf, re, unicodedata, collections
FBf='../fonts/Poppins-700.ttf'; FR='../fonts/Poppins-400.ttf'
src=pymupdf.open('nav.pdf'); out=pymupdf.open('nav_facil_tmp4.pdf')
soltxt=' '.join(src[p].get_text() for p in range(90,102)).replace('\n',' ')
def norm(s): return ''.join(c for c in unicodedata.normalize('NFD',s.upper()) if unicodedata.category(c)!='Mn' or c=='̃').replace('Ñ','Ñ')
for p in [16,34,53,74,89]:
    pg=src[p-1]; ws=pg.get_text('words'); tabla=[w for w in ws if w[4]=='TABLA'][0][1]
    nums=[w for w in ws if w[4].isdigit() and 100<w[1]<tabla-5]
    rows={}
    for w in nums: rows.setdefault(round(w[1]),[]).append(w)
    seq=[]
    for y in sorted(rows):
        r=sorted(rows[y],key=lambda w:w[0])
        for k,w in enumerate(r):
            if k and w[0]-r[k-1][0]>27: seq.append('|')
            seq.append(w)
        seq.append('|')
    words=[];cur=[]
    for t in seq:
        if t=='|':
            if cur: words.append(cur); cur=[]
        else: cur.append(t)
    phrase=re.search(r'P\. ?%d · [^«]*«([^»]*)»'%p, soltxt).group(1)
    pw=[x for x in (re.sub('[^A-ZÑ]','',norm(x)) for x in phrase.split()) if x]
    mp={}; pos=collections.defaultdict(list)
    for a,b in zip(pw,words):
        for ch,w in zip(a,b): mp[int(w[4])]=ch; pos[int(w[4])].append(w)
    # existing given letters: letter words above numbers
    letters=[w for w in ws if len(w[4])==1 and w[4].isalpha() and 100<w[1]<tabla-5]
    given=set()
    ref=None
    for L in letters:
        lx=(L[0]+L[2])/2
        below=[n for n in nums if abs((n[0]+n[2])/2-lx)<4 and 0<n[1]-L[1]<40]
        if below:
            n=min(below,key=lambda n:n[1]-L[1]); given.add(int(n[4])); ref=(L,n)
    # reference style from span
    sp=None
    for b in pg.get_text('dict')['blocks']:
        for l in b.get('lines',[]):
            for s in l['spans']:
                if s['text'].strip()==ref[0][4] and abs(s['bbox'][0]-ref[0][0])<1 and abs(s['bbox'][1]-ref[0][1])<1: sp=s
    dy=sp['origin'][1]-ref[1][1]  # baseline relative to number top
    cnt=collections.Counter(int(w[4]) for wd in words for w in wd)
    cand=[n for n,_ in cnt.most_common() if n not in given][:3]
    o=out[p-1]
    for n in cand:
        ch=mp[n]
        for w in pos[n]:
            cx=(w[0]+w[2])/2; tw=pymupdf.Font(fontfile=FBf).text_length(ch,fontsize=sp['size'])
            o.insert_text((cx-tw/2, w[1]+dy), ch, fontsize=sp['size'], fontfile=FBf, fontname='PopB', color=(0,0,0))
    # text fix
    r=o.search_for('regalamos')[0]
    cands=[x for x in o.search_for('dos') if (abs(x.y0-r.y0)<2 and x.x0>r.x1-1) or (0<x.y0-r.y0<16 and x.x0<r.x0)]
    rr=sorted(cands,key=lambda x:(x.y0,x.x0))[0]
    oy=None
    for b in o.get_text('dict')['blocks']:
        for l in b.get('lines',[]):
            for s in l['spans']:
                sb=pymupdf.Rect(s['bbox'])
                if sb.y0<=(rr.y0+rr.y1)/2<=sb.y1 and sb.x0<=rr.x0+1<=sb.x1: oy=s['origin'][1]; sz=s['size']
    line=None
    for b in o.get_text('dict')['blocks']:
        for l in b.get('lines',[]):
            lb=pymupdf.Rect(l['bbox']); cy=(rr.y0+rr.y1)/2
            if lb.y0<=cy<=lb.y1 and lb.x0<=rr.x0<=lb.x1: line=l
    # rebuild spans after 'dos' keeping each span's font and colour
    segs=[]; started=False
    for sp_ in line['spans']:
        t=sp_['text']
        if not started:
            k=t.find('dos', t.find('regalamos')+1 if 'regalamos' in t else 0)
            if k>=0 and pymupdf.Rect(sp_['bbox']).x0-1<=rr.x0<=sp_['bbox'][2]:
                started=True; segs.append(('cinco',sp_)); segs.append((t[k+3:],sp_))
            continue
        segs.append((t,sp_))
    red=pymupdf.Rect(rr.x0,rr.y0,line['bbox'][2]+1,rr.y1)
    o.add_redact_annot(red,fill=False); o.apply_redactions(images=0,graphics=0)
    x=rr.x0
    for t,sp_ in segs:
        if not t: continue
        ff=FBf if 'Bold' in sp_['font'] else FR; fn='PopB' if 'Bold' in sp_['font'] else 'PopR'
        c=sp_['color']; col=((c>>16)&255)/255,((c>>8)&255)/255,(c&255)/255
        o.insert_text((x,sp_['origin'][1]),t,fontsize=sp_['size'],fontfile=ff,fontname=fn,color=col)
        x+=pymupdf.Font(fontfile=ff).text_length(t,fontsize=sp_['size'])
    print('   termina en',round(x),'antes',round(line['bbox'][2]), 'colores',set(hex(sp_['color']) for _,sp_ in segs))
    print(p,'dadas antes',sorted(mp[g] for g in given),'añadidas',[mp[n] for n in cand])
out.save('nav_facil_tmp5.pdf')
