import numpy as np,wave,sys
D=sys.argv[1];SR=48000;N=int(10*SR);rng=np.random.default_rng(3);out=np.zeros(N);tt=np.arange(N)/SR
def band(x,lo,hi):
    X=np.fft.rfft(x);f=np.fft.rfftfreq(len(x),1/SR);m=((f>=lo)&(f<=hi)).astype(float);return np.fft.irfft(X*m,len(x))
def add(t0,s,g=1):
    i=int(t0*SR);j=min(N,i+len(s));out[i:j]+=s[:j-i]*g
def nz(d):return rng.standard_normal(int(d*SR))
def boom(d=1.0,f=48):
    t=np.arange(int(d*SR))/SR;fr=f*(1+1.5*np.exp(-t*12));return np.sin(2*np.pi*np.cumsum(fr)/SR)*np.exp(-t*3.2)
def norm(x):return x/(np.abs(x).max()+1e-9)
# логотип
add(0.0,norm(boom(1.1)),0.9);add(0.0,norm(band(nz(0.25),200,4000)*np.exp(-np.arange(int(0.25*SR))/SR*14)),0.27)
# сверчки
cr=np.zeros(N)
for k in range(int(5.4/0.5)):
    t0=1.2+k*0.5+rng.random()*0.12
    for j in range(3):
        n=int(0.035*SR);t=np.arange(n)/SR;add_=np.sin(2*np.pi*4300*t)*np.sin(np.pi*t/0.035)
        i=int((t0+j*0.06)*SR);cr[i:i+n]+=add_
cr*=((tt>1.2)&(tt<6.3))*np.where(tt<4.7,1,0.5);out+=norm(cr)*0.12
# щелчок фонарика
add(1.25,norm(band(nz(0.03),1500,9000)*np.exp(-np.arange(int(0.03*SR))/SR*200)),0.45)
# шаги по гравию (синхронно с циклом ходьбы sp=7)
for n in range(1,40):
    t0=n*np.pi/7
    if 1.25<t0<4.7:
        s=band(nz(0.12),700,5000)*np.exp(-np.arange(int(0.12*SR))/SR*35)*(1+0.5*rng.random(int(0.12*SR)));add(t0,norm(s),0.35)
# сердцебиение
for k in range(4):
    for dt,g in [(0,1),(0.18,0.7)]:
        t0=4.8+k*0.62+dt
        if t0<6.45:add(t0,norm(boom(0.18,55)),0.55*g)
# нарастание и удар
n=int(0.6*SR);t=np.arange(n)/SR;ris=band(nz(0.6),300,8000)*(t/0.6)**2+0.4*np.sin(2*np.pi*np.cumsum(200+1400*(t/0.6)**2)/SR)*(t/0.6)**2;add(5.9,norm(ris),0.35)
add(6.5,norm(boom(1.4,42)),1.0);add(6.5,norm(band(nz(0.3),100,6000)*np.exp(-np.arange(int(0.3*SR))/SR*10)),0.5)
# гул
d=2.1;t=np.arange(int(d*SR))/SR;dr=(np.sin(2*np.pi*45*t)+0.6*np.sin(2*np.pi*67.5*t+1))*np.minimum(1,t/0.3)*np.minimum(1,(d-t)/0.2);add(6.5,norm(dr),0.18)
# переход и «попы» карточек
n=int(0.35*SR);t=np.arange(n)/n;add(8.52,norm(band(nz(0.35),400,6000)*np.sin(np.pi*t)**2),0.35)
for t0 in [8.85,9.05]:
    t=np.arange(int(0.12*SR))/SR;add(t0,np.sin(2*np.pi*(700+900*np.exp(-t*30))*t)*np.exp(-t*25),0.25)
gv=np.load(D+'/gv.npy');nv=np.load(D+'/nv.npy')
vo=gv/np.abs(gv).max()*0.9+nv/np.abs(nv).max()*0.85
mix=vo+out*0.55;mix=np.tanh(mix*1.05)/np.tanh(1.05)*0.95
pcm=(np.stack([mix,mix],1)*32767).clip(-32768,32767).astype('<i2')
with wave.open(D+'/mix.wav','wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(SR);f.writeframes(pcm.tobytes())
print('ok')
