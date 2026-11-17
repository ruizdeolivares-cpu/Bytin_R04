#!/usr/bin/env python3
"""Analiza las canciones de musica/: ritmo (BPM), golpes y punto de arranque con energía. Ejecutar desde editor/."""
import librosa, numpy as np, glob, json, os
res={}
for f in sorted(glob.glob('musica/*.mp3')):
    y,sr=librosa.load(f,sr=22050,mono=True)
    tempo,beats=librosa.beat.beat_track(y=y,sr=sr,units='time')
    rms=librosa.feature.rms(y=y)[0]; t=librosa.times_like(rms,sr=sr)
    # energía media en ventanas de 25 s: elegir arranque energético (no intro), alineado a beat
    best=(beats[0] if len(beats) else 0.0, 0)
    for b in beats:
        if b>len(y)/sr-30: break
        m=rms[(t>=b)&(t<b+25)].mean()
        if True:
            if m>best[1]: best=(b,m)
    first_loud=next((b for b in beats if rms[(t>=b)&(t<b+2)].mean()>0.4*rms.max()),beats[0])
    res[os.path.basename(f)]={'bpm':round(float(np.atleast_1d(tempo)[0]),1),'inicio_energia':round(float(first_loud),2),'mejor_tramo':round(float(best[0]),2),'beats':[round(float(x),3) for x in beats]}
    print(os.path.basename(f), res[os.path.basename(f)]['bpm'], res[os.path.basename(f)]['inicio_energia'], res[os.path.basename(f)]['mejor_tramo'])
json.dump(res,open('musica/beats.json','w'))
