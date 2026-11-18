# splice.py in out "f0:f1:speed" ...  (frames a 30 fps; f1 exclusivo)
import sys,subprocess
inp,out=sys.argv[1],sys.argv[2]; segs=[s.split(':') for s in sys.argv[3:]]
fc='';cat=''
for k,(a,b,sp) in enumerate(segs):
    a,b,sp=int(a),int(b),float(sp); t0,t1=a/30,b/30; d=(t1-t0)/sp
    fc+=f"[0:v]trim=start_frame={a}:end_frame={b},setpts=(PTS-STARTPTS)/{sp}[v{k}];"
    fc+=f"[0:a]atrim={t0}:{t1},asetpts=PTS-STARTPTS"+(f",atempo={sp}" if sp!=1 else '')+f",afade=t=in:d=0.01,afade=t=out:st={max(0,d-0.015)}:d=0.015[a{k}];"
    cat+=f"[v{k}][a{k}]"
n=len(segs)
fc+=f"{cat}concat=n={n}:v=1:a=1[v][ax];[ax]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100[a]"
subprocess.run(['ffmpeg','-v','error','-y','-i',inp,'-filter_complex',fc,'-map','[v]','-map','[a]','-r','30','-c:v','libx264','-preset','veryfast','-crf','23','-maxrate','1100k','-bufsize','2200k','-c:a','aac','-b:a','128k','-movflags','+faststart',out],check=True)
