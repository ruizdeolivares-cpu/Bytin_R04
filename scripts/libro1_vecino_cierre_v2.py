# Cambia el cierre de «El vecino que todos tenemos» por la portada nueva (v3). Audio intacto.
import sys, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S=sys.argv[1]; B=S+'/vc/'; W,H=720,1280; YEL=(255,226,0); PINK=(255,45,150)
SRC='libro_pt1/V_vecino_que_todos_tenemos.mp4'; OUT=B+'V_vecino_v2.mp4'
FA=lambda n: ImageFont.truetype(S+'/fonts/fontsource-anton-5.3.0/package/files/anton-latin-400-normal.woff',n)
FBs=ImageFont.truetype(S+'/fonts/fontsource-baloo-2-5.3.0/package/files/baloo-2-latin-800-normal.woff',40)
def run(c): subprocess.run(c,shell=True,check=True,stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
im=Image.new('RGB',(W,H),YEL); d=ImageDraw.Draw(im)
for y in range(0,H,22):
    for x in range((y//22%2)*11,W,22): d.ellipse([x-3,y-3,x+3,y+3],fill=(245,205,0))
p=Image.open('libro_pt1/portada_nueva_frontal.png').convert('RGB'); ph=640; p=p.resize((int(p.width*ph/p.height),ph),Image.LANCZOS)
x0,y0=330-p.width//2,120
sh=Image.new('L',(W,H),0); ImageDraw.Draw(sh).rectangle([x0+14,y0+14,x0+p.width+14,y0+ph+14],fill=150); sh=sh.filter(ImageFilter.GaussianBlur(10))
im.paste((40,30,0),(0,0),sh); im.paste(p,(x0,y0)); d.rectangle([x0-5,y0-5,x0+p.width+4,y0+ph+4],outline='black',width=6)
d.text((330,840),'El regalo perfecto para ese',font=FBs,fill='black',anchor='mm')
d.text((330,895),'vecino que te cae fatal.',font=FBs,fill='black',anchor='mm')
d.text((330,975),'EN AMAZON',font=FA(58),fill=PINK,anchor='mm',stroke_width=5,stroke_fill='black')
im.save(B+'cierre_v2.png')
dur=3.8; n=int(dur*30); cut=1177-n  # el cierre antiguo son los últimos 114 fotogramas
run(f'ffmpeg -y -loop 1 -t {dur} -i {B}cierre_v2.png -vf "scale=1440:2560,zoompan=z=\'1+0.04*on/{n}\':x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':d={n}:s=720x1280:fps=30" -frames:v {n} -c:v libx264 -preset veryfast -crf 18 {B}cierre_v2.mp4')
fc=f'[0:v]trim=end_frame={cut},setpts=PTS-STARTPTS[a];[1:v]setpts=PTS-STARTPTS,setsar=1[b];[a][b]concat=n=2:v=1:a=0[v]'
for ps in (1,2):
    o=f'-c:a aac -b:a 128k -movflags +faststart {OUT}' if ps==2 else '-an -f mp4 /dev/null'
    run(f'cd {B} && ffmpeg -y -i /home/user/Bytin_R04/{SRC} -i {B}cierre_v2.mp4 -filter_complex "{fc}" -map "[v]" -map 0:a? -c:v libx264 -preset slow -b:v 430k -pass {ps} -passlogfile {B}p2 {o}')
print('ok')
