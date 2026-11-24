import pymupdf, re, itertools, collections
FBf='../fonts/Poppins-700.ttf'
out=pymupdf.open('nav_facil_tmp5.pdf')
eqs={23:[("COPAS","COPAS","POSTRE"),("TURRON","TURRON","SIESTA"),("COPAS","LICOR","SIESTA"),("TUPPER","TURRON","BRONCA")],
50:[("PAVO","VINO","PELEA"),("GAMBAS","GAMBAS","BRONCA"),("MARISCO","MARISCO","FACTURA"),("JAMON","MANDO","SIESTA")],
72:[("UVAS","GORRO","RESACA"),("SIDRA","SIDRA","GRESCA"),("REYES","REYES","BRONCA"),("ROSCON","ROSCON","DESFASE")],
90:[("GORRO","GORRO","CUESTA"),("CAVA","SUEGRA","MARCHA"),("SIDRA","SUEGRA","PESADO"),("ROSCON","SUEGRA","BRONCA")]}
def solve(a,b,c):
    L=sorted(set(a+b+c))
    for perm in itertools.permutations(range(10),len(L)):
        m=dict(zip(L,perm))
        if 0 in (m[a[0]],m[b[0]],m[c[0]]): continue
        n=lambda w:int(''.join(str(m[ch]) for ch in w))
        if n(a)+n(b)==n(c): return m
for p,E in eqs.items():
    pg=out[p-1]
    toks=[w for w in pg.get_text('words') if re.match(r'^[A-ZÑ]=',w[4]) and w[1]>90]
    rows=collections.defaultdict(list)
    for w in toks: rows[(round(w[1]/3), 0 if (p!=23 or w[0]<216) else 1)].append(w)
    keys=sorted(rows,key=lambda k:(k[0],k[1]))
    groups=[]
    for k in keys:
        g=next((g for g in groups if g['col']==k[1] and 0<k[0]*3-g['y']<16),None)
        if g: g['toks']+=rows[k]; g['y']=k[0]*3
        else: groups.append({'col':k[1],'y':k[0]*3,'toks':list(rows[k]),'y0':k[0]*3})
    groups.sort(key=lambda g:(g['y0'],g['col']))
    assert len(groups)==4, (p,len(groups))
    for (a,b,c),g in zip(E,groups):
        m=solve(a,b,c)
        cnt=collections.Counter(a+b+c)
        pickL=[L for L,_ in cnt.most_common() if L!=c[0]][:2]
        for L in pickL:
            t=[w for w in g['toks'] if w[4].startswith(L+'=')][0]
            eq_x=t[0]+pymupdf.Font(fontfile=FBf).text_length(L+'=',fontsize=(t[3]-t[1])*0.72)
            sp=[s for bl in pg.get_text('dict')['blocks'] for l in bl.get('lines',[]) for s in l['spans'] if s['text'].strip().startswith(L+'=') and abs(s['bbox'][1]-t[1])<1.5]
            s0=sp[0] if sp else None
            size=s0['size'] if s0 else 8; oy=s0['origin'][1] if s0 else t[3]-2
            x=t[0]+pymupdf.Font(fontfile=FBf if (s0 and 'Bold' in s0['font']) else '../fonts/Poppins-400.ttf').text_length(L+'=',fontsize=size)+1.5
            pg.insert_text((x,oy),str(m[L]),fontsize=size*1.1,fontfile=FBf,fontname='PopB',color=(0,0,0))
        print(p,f"{a}+{b}={c}: regaladas",{L:m[L] for L in pickL})
out.save('nav_facil_tmp6.pdf')
