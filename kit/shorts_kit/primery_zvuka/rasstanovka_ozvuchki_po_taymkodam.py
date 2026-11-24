import numpy as np, wave
SR=48000; N=int(51.0*SR)
def rd(p):
    with wave.open(p) as f: a=np.frombuffer(f.readframes(f.getnframes()),'<i2').astype(float)/32768; 
    return a.reshape(-1,f.getnchannels()).mean(1) if f.getnchannels()>1 else a
narr=rd('narr.wav'); gr=rd('granny.wav')
# (источник, начало, конец, куда ставим)
N_LINES=[(0.08,1.44,0.2),(1.68,2.76,2.8),(2.96,4.28,4.0),(4.48,6.44,6.1),(6.64,8.04,8.1),(8.24,9.76,9.5),
 (9.92,10.68,12.1),(10.8,12.32,13.7),(12.48,13.84,16.1),(14.0,15.12,17.8),(15.28,16.16,19.7),(16.4,17.6,21.3),
 (17.76,19.12,25.7),(19.28,20.76,27.5),(20.88,22.56,30.0),(22.72,24.48,32.0),(24.64,26.32,33.9),(26.36,27.56,35.6),
 (27.84,29.32,38.5),(29.6,30.12,40.1),(30.32,31.68,40.7),(31.92,32.88,45.0),(33.04,34.72,46.4),(34.88,36.0,48.9)]
G_LINES=[(0.0,2.71,22.8),(3.20,5.56,42.6)]
vo=np.zeros(N)
def place(src,a,b,at,nxt):
    a=max(0,a-0.06); b=min(b+0.15,nxt-0.02,len(src)/SR)
    seg=src[int(a*SR):int(b*SR)].copy(); n=len(seg); f=int(0.012*SR)
    seg[:f]*=np.linspace(0,1,f); seg[-f:]*=np.linspace(1,0,f)
    i=int(at*SR); vo[i:i+n]+=seg[:N-i]
for k,(a,b,at) in enumerate(N_LINES):
    nxt=N_LINES[k+1][0] if k+1<len(N_LINES) else 99
    place(narr,a,b,at,nxt)
for k,(a,b,at) in enumerate(G_LINES):
    nxt=G_LINES[k+1][0] if k+1<len(G_LINES) else 99
    place(gr,a,b,at,nxt)
vo=vo/np.abs(vo).max()*0.89
with wave.open('/home/user/Anim/part2/sfx_tmp.wav') if False else wave.open('/home/user/Anim/part2/balkon_part2_sfx.wav') as f:
    sfx=np.frombuffer(f.readframes(f.getnframes()),'<i2').astype(float).reshape(-1,2).mean(1)/32768
sfx=np.pad(sfx,(0,max(0,N-len(sfx))))[:N]
mix=vo+sfx*0.5
mix=np.tanh(mix*1.1)/np.tanh(1.1)*0.95  # мягкий лимитер
def wr(p,x):
    pcm=(np.stack([x,x],1)*32767).clip(-32768,32767).astype('<i2')
    with wave.open(p,'wb') as f: f.setnchannels(2);f.setsampwidth(2);f.setframerate(SR);f.writeframes(pcm.tobytes())
wr('/home/user/Anim/part2/balkon_part2_voice.wav',vo); wr('mix.wav',mix); print('ok')
