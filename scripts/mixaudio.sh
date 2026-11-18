# mixaudio.sh video.mp4 music.mp3 music_start dur cut0 cut1 out.mp4 "events" [nomusic]
V=$1; M=$2; MS=$3; DUR=$4; C0=$5; C1=$6; OUT=$7; EV=$8; NOM=$9
S=/home/user/Bytin_R04/work/fonts/sfx/package/sounds
ins=""; fc=""; i=2; mix=""
for e in $EV; do t=${e%%:*}; f=${e#*:}; ins="$ins -i $S/$f.mp3"; ms=$(python3 -c "print(int($t*1000))"); fc="$fc[$i:a]adelay=$ms|$ms,volume=0.9[s$i];"; mix="$mix[s$i]"; i=$((i+1)); done; n=$((i-2))
MV=0.55; [ "$NOM" = "nomusic" ] && MV=0
FO=$(python3 -c "print($DUR-0.35)")
ffmpeg -v error -y -i $V -ss $MS -t $DUR -i $M $ins -filter_complex "[1:a]volume='if(between(t,$C0,$C1),0,1)':eval=frame,afade=t=out:st=$FO:d=0.35,volume=$MV[m];$fc[m]${mix}amix=inputs=$((n+1)):normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100[a]" -map 0:v -map "[a]" -c:v libx264 -preset veryfast -crf 23 -maxrate 1100k -bufsize 2200k -c:a aac -b:a 128k -t $DUR -movflags +faststart $OUT
