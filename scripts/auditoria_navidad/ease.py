import pymupdf, json, random, re, sys
sys.path.insert(0,'..')
exec(open('../gridread.py').read()); exec(open('../sudoku.py').read())
FONT='../fonts/Poppins-700.ttf'
FB=pymupdf.Font(fontfile=FONT)
LOG=[]
def ref_span(pg, xs, ys):
    for b in pg.get_text('dict')['blocks']:
        for l in b.get('lines',[]):
            for s in l['spans']:
                t=s['text'].strip()
                if len(t)==1 and (t.isdigit() or t.isalpha()):
                    cx=(s['bbox'][0]+s['bbox'][2])/2; cy=(s['bbox'][1]+s['bbox'][3])/2
                    if xs[0]<cx<xs[-1] and ys[0]<cy<ys[-1]:
                        j=max(k for k in range(len(xs)-1) if xs[k]<=cx); i=max(k for k in range(len(ys)-1) if ys[k]<=cy)
                        return s, s['origin'][1]-ys[i], s['size'], s['color']
def put(pg, x0, x1, y0, dy, txt, size, color=0):
    w=FB.text_length(txt,fontsize=size)
    c=((color>>16)&255)/255,((color>>8)&255)/255,(color&255)/255
    pg.insert_text(((x0+x1)/2-w/2, y0+dy), txt, fontsize=size, fontfile=FONT, fontname='PopB', color=c)
