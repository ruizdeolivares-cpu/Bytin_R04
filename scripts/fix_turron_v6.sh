IN=turron_v5.mp4; EXTRA="-loop 1 -framerate 30 -i fillA.png"; OUT=Caso_ultimo_turron_v6.mp4
# shift(N, fillrows K): top N rows = src rows 0..K scaled
FC="[0:v]split=5[a][b][c][d][e];
[a]trim=start_frame=0:end_frame=150,setpts=PTS-STARTPTS,split[a1][a2];[a2]nullsink;[1:v]trim=end_frame=150,setpts=PTS-STARTPTS,format=yuv420p[af];[a1][af]overlay=0:0[a3];[a3]null[a4];
[a4]crop=720:1280:0:0[abase];
[0:v]trim=start_frame=0:end_frame=150,setpts=PTS-STARTPTS[asrc];[abase][asrc]overlay=0:75[A];
[b]trim=start_frame=150:end_frame=438,setpts=PTS-STARTPTS,split=5[b1][b2][b3][b4][b5];
[b1]crop=720:60:0:0,scale=720:102,setsar=1[bt];
[b2]crop=720:138:0:60[bband];
[b3]crop=720:853:0:322[blow];
[b4]crop=106:56:522:198[bbadge];
[b5]crop=720:105:0:1175,scale=720:187,setsar=1[bbot];
color=c=black:s=720x1280:r=30:d=9.6[bc];
[bc][bt]overlay=0:0:shortest=1[bx1];[bx1][bband]overlay=0:102[bx2];[bx2][blow]overlay=0:240[bx3];[bx3][bbot]overlay=0:1093[bx4];[bx4][bbadge]overlay=522:246[B];
[c]trim=start_frame=438:end_frame=550,setpts=PTS-STARTPTS,split[c1][c2];[c1][c2]overlay=0:34[C];
[d]trim=start_frame=550:end_frame=594,setpts=PTS-STARTPTS,split=3[d1][d2][d3];[d2]crop=720:38:0:0,scale=720:75,setsar=1[df];[d1][df]overlay=0:0[dx];[dx][d3]overlay=0:75[D];
[e]trim=start_frame=594,setpts=PTS-STARTPTS,split=3[e1][e2][e3];[e2]crop=720:160:0:0[eh];[e3]crop=720:1110:0:170[el];[e1][el]overlay=0:210[ex];[ex][eh]overlay=0:50[E];
[A][B][C][D][E]concat=n=5:v=1:a=0,format=yuv420p[v]"
ffmpeg -v error -y -i $IN $EXTRA -filter_complex "$FC" -map "[v]" -map 0:a -c:v libx264 -preset veryfast -crf 23 -maxrate 1100k -bufsize 2200k -r 30 -c:a copy -movflags +faststart $OUT
