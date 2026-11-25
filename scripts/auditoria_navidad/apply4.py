import pymupdf, json, random, re, sys
sys.argv=['x','nav.pdf']; exec(open('../nonochk.py').read())
orig=d
C=json.load(open('cat.json'))['puz']
sols={}
for pn in [91,94,98,101,102]:
    for lab,G in solution_grids(pn): sols[int(re.search(r'P\. (\d+)',lab).group(1))]=G
out=pymupdf.open('nav_facil_tmp3.pdf')
FR='../fonts/Poppins-400.ttf'; FBf='../fonts/Poppins-700.ttf'
for p in [11,28,38,45,56,66,78,87]:
    pg=out[p-1]; xs=C[f"{p}.0"]['xs']; ys=C[f"{p}.0"]['ys']; G=sols[p]
    blacks=[(i,j) for i in range(len(G)) for j in range(len(G[0])) if G[i][j]]
    k=round(len(blacks)*(0.18 if p==11 else 0.14))
    for i,j in random.Random(p).sample(blacks,k):
        r=pymupdf.Rect(xs[j]+0.6,ys[i]+0.6,xs[j+1]-0.6,ys[i+1]-0.6)
        pg.draw_rect(r,color=None,fill=(0,0,0))
    y=ys[-1]+16; t2='las casillas ya pintadas son correctas.'
    w1=pymupdf.Font(fontfile=FBf).text_length('REGALO: ',fontsize=7.6); w2=pymupdf.Font(fontfile=FR).text_length(t2,fontsize=7.6)
    x0=(pg.rect.width-(w1+w2))/2
    pg.insert_text((x0,y),'REGALO:',fontsize=7.6,fontfile=FBf,fontname='PopB',color=(0,0,0))
    pg.insert_text((x0+w1,y),t2,fontsize=7.6,fontfile=FR,fontname='PopR',color=(0,0,0))
    print(p,'pintadas',k,'de',len(blacks))
out.save('nav_facil_tmp4.pdf')
