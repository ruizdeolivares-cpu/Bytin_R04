# Versión corta (~20 s) de «El vecino que todos tenemos», cortada del montaje largo (cierre con portada nueva).
import sys, subprocess
S=sys.argv[1]; B=S+'/vc/'
SRC='/home/user/Bytin_R04/libro_pt1/V_vecino_que_todos_tenemos.mp4'; OUT='/home/user/Bytin_R04/libro_pt1/V_vecino_20s.mp4'
# tramos (s) sobre el vídeo largo: nota, Marisa, cámaras, «¿y si el culpable… eres tú?», presidente, cierre
T=[(0,1.1333),(1.1333,3.5333),(12.3,16.4667),(19.9667,24.8667),(27.43,31.2333),(35.4333,39.2333)]
fc=''; cat=''
for i,(a,b) in enumerate(T):
    d=b-a
    fc+=f'[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}];[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={d-0.03:.3f}:d=0.03[a{i}];'
    cat+=f'[v{i}][a{i}]'
fc+=f'{cat}concat=n={len(T)}:v=1:a=1[v][a]'
for ps in (1,2):
    o=f'-map "[a]" -c:a aac -b:a 128k '+(f'-movflags +faststart {OUT}' if ps==2 else '-f mp4 /dev/null')
    subprocess.run(f'cd {B} && ffmpeg -y -i {SRC} -filter_complex "{fc}" -map "[v]" -c:v libx264 -preset slow -b:v 900k -maxrate 1300k -bufsize 2600k -pass {ps} -passlogfile {B}p20 {o}',shell=True,check=True,stderr=subprocess.DEVNULL)
print('ok')
