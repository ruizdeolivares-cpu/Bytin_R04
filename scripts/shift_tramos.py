# usage: shift.py in out "s0:e0:N:fill" ...   fill = self | black | #rrggbb ; e=-1 => end
import sys,subprocess
inp,out=sys.argv[1],sys.argv[2]; segs=[s.split(':') for s in sys.argv[3:]]
n=len(segs); fc=f"[0:v]split={n}"+''.join(f"[i{k}]" for k in range(n))+";"
for k,(s,e,N,fill) in enumerate(segs):
    N=int(N); tr=f"trim=start_frame={s}"+(f":end_frame={e}" if e!='-1' else '')+",setpts=PTS-STARTPTS"
    if N==0: fc+=f"[i{k}]{tr}[o{k}];"; continue
    if fill=='self':
        fc+=f"[i{k}]{tr},split[a{k}][b{k}];[a{k}][b{k}]overlay=0:{N}[o{k}];"
    else:
        col='black' if fill=='black' else fill
        fc+=f"[i{k}]{tr},split[a{k}][b{k}];[a{k}][b{k}]overlay=0:{N},drawbox=x=0:y=0:w=720:h={N}:c={col}:t=fill[o{k}];"
fc+=''.join(f"[o{k}]" for k in range(n))+f"concat=n={n}:v=1:a=0,format=yuv420p[v]"
subprocess.run(['ffmpeg','-v','error','-y','-i',inp,'-filter_complex',fc,'-map','[v]','-map','0:a','-c:v','libx264','-preset','veryfast','-crf','23','-maxrate','1100k','-bufsize','2200k','-r','30','-c:a','copy','-movflags','+faststart',out],check=True)
