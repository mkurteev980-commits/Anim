import numpy as np,wave
import json
WJ=json.load(open('warp.json'))
SR=48000;DUR=WJ['DUR'];N=int(DUR*SR);rng=np.random.default_rng(11);out=np.zeros(N);tt=np.arange(N)/SR
def band(x,lo,hi):
    X=np.fft.rfft(x);f=np.fft.rfftfreq(len(x),1/SR);return np.fft.irfft(X*((f>=lo)&(f<=hi)),len(x))
def nz(d):return rng.standard_normal(int(d*SR))
def norm(x):return x/(np.abs(x).max()+1e-9)
def O2N(to):
    OB,NB,fs=WJ['OB'],WJ['NB'],WJ['fs']
    for i in range(len(fs)):
        if to<=OB[i+1] or i==len(fs)-1:return NB[i]+(to-OB[i])*fs[i]
def add(t0,s,g=1):
    i=int(O2N(t0)*SR);j=min(N,i+len(s));out[i:j]+=s[:j-i]*g
def env(d,k):return np.exp(-np.arange(int(d*SR))/SR*k)
def boom(d,f):
    t=np.arange(int(d*SR))/SR;fr=f*(1+1.5*np.exp(-t*12));return np.sin(2*np.pi*np.cumsum(fr)/SR)*np.exp(-t*3.2)
def whoosh(d=0.4):
    n=int(d*SR);t=np.arange(n)/n;return norm(band(nz(d),300,7000)*np.sin(np.pi*t)**2)
def ding():
    t=np.arange(int(0.6*SR))/SR;return np.sin(2*np.pi*1320*t)*np.exp(-t*8)+0.5*np.sin(2*np.pi*1980*t)*np.exp(-t*10)
def beat(t0,t1):
    k=0
    while True:
        for dt,g in [(0,1),(0.18,0.7)]:
            x=t0+k*0.62+dt
            if x>=t1:return
            add(x,norm(boom(0.18,55)),0.45*g)
        k+=1
def drone(t0,d,f=45,g=0.15):
    t=np.arange(int(d*SR))/SR;s=(np.sin(2*np.pi*f*t)+0.6*np.sin(2*np.pi*f*1.5*t+1))*np.minimum(1,t/0.4)*np.minimum(1,(d-t)/0.4);add(t0,norm(s),g)
def crickets(t0,t1,g=0.08):
    k=t0
    while k<t1:
        for j in range(3):
            n=int(0.035*SR);t=np.arange(n)/SR;add(k+j*0.06,np.sin(2*np.pi*4300*t)*np.sin(np.pi*t/0.035),g)
        k+=0.45+rng.random()*0.15
# правила
add(0.1,norm(band(nz(0.03),1500,9000)*env(0.03,200)),0.45);drone(0,3.0,42,0.18);add(0.4,norm(band(nz(0.5),500,4000)*env(0.5,6)),0.12)
for t0 in [3.0,13.0,25.0]:add(t0-0.05,whoosh(0.35),0.35);add(t0+0.1,ding(),0.2)
# кровать
crickets(5.6,10.4,0.05);drone(5.6,4.8,40,0.12)
add(7.5,norm(boom(1.2,46)),0.9);add(7.5,norm(band(nz(0.6),2500,9000)*env(0.6,5)),0.25)
beat(7.7,10.4)
for t0 in [7.7,21.0,31.3]:add(t0,norm(boom(0.25,70)),0.7);add(t0,norm(band(nz(0.08),300,3000)*env(0.08,40)),0.35)
add(10.12,whoosh(0.3),0.25)
# линейка: горн
notes=[(392,0.25),(523,0.25),(659,0.25),(784,0.6)];x=16.0
for f,d in notes:
    t=np.arange(int(d*SR))/SR;vib=1+0.01*np.sin(2*np.pi*6*t);ph=np.cumsum(f*vib)/SR;s=sum((1/k)*np.sin(2*np.pi*k*ph) for k in range(1,7))*np.minimum(1,t/0.03)*np.minimum(1,(d-t)/0.05);add(x,norm(s),0.14);x+=d+0.03
crickets(15.9,19.6,0.06)
add(19.6,norm(boom(1.3,42)),0.9);drone(19.6,2.3,45,0.15)
# капли
for k in range(14):
    t0=21.9+k*0.22+rng.random()*0.1;t=np.arange(int(0.12*SR))/SR;f=900+rng.random()*700;add(t0,np.sin(2*np.pi*f*t*(1+t*8))*np.exp(-t*40),0.18)
# отряд оборачивается + свисток
drone(28.0,3.0,38,0.2);add(28.65,norm(band(nz(0.5),200,2000)*np.sin(np.linspace(0,np.pi,int(0.5*SR)))),0.15)
t=np.arange(int(0.8*SR))/SR;(lambda *x:None)(30.2,np.sin(2*np.pi*2600*t)*(0.6+0.4*np.sign(np.sin(2*np.pi*28*t)))*np.minimum(1,t/0.03)*np.minimum(1,(0.8-t)/0.08),0.22)
# вода
w=norm(band(nz(18),60,700));w*=0.6+0.4*np.sin(2*np.pi*0.5*np.arange(len(w))/SR);add(31.0,w*np.minimum(1,np.arange(len(w))/SR/0.5),0.12)
for k in range(10):
    t0=33.9+k*0.6+rng.random()*0.2;t=np.arange(int(0.12*SR))/SR;add(t0,np.sin(2*np.pi*(1100+rng.random()*500)*t*(1+t*6))*np.exp(-t*40),0.14)
beat(38.9,41.0)
n=int(1.05*SR);t=np.arange(n)/SR;add(44.2,norm(band(nz(1.05),300,8000)*(t/1.05)**2.5),0.35)
add(45.25,norm(boom(1.2,40)),1.0);add(45.25,norm(band(nz(0.7),200,6000)*env(0.7,6)),0.5)
add(45.7,norm(band(nz(0.5),60,500)*np.sin(np.linspace(0,np.pi,int(0.5*SR)))),0.25)
# выбор
add(46.48,norm(band(nz(0.35),1500,12000)*env(0.35,12)),0.45);add(46.75,whoosh(0.35),0.45);add(46.82,norm(boom(0.8,50)),0.6)
for k,t0 in enumerate([47.7,48.7,49.7]):
    t=np.arange(int(0.08*SR))/SR;add(t0,np.sin(2*np.pi*(1200 if k<2 else 1600)*t)*np.exp(-t*60),0.4);add(t0+0.5,np.sin(2*np.pi*800*t)*np.exp(-t*60),0.28)
t=np.arange(int(0.5*SR))/SR;add(50.7,np.sign(np.sin(2*np.pi*140*t))*np.exp(-t*5)*0.6,0.3)
t=np.arange(int(0.12*SR))/SR;add(47.4,np.sin(2*np.pi*(700+900*np.exp(-t*30))*t)*np.exp(-t*25),0.22)
nv=np.load('nv.npy');gv=np.load('gv.npy')
vo=nv+gv;vo=vo/np.abs(vo).max()*0.95
ev=np.abs(vo);k=int(0.06*SR);ev=np.convolve(ev,np.ones(k)/k,'same');ev=np.maximum.accumulate(ev[::-1])[::-1]*0+ev
duck=1-0.92*np.clip(ev/0.015,0,1)
sm=int(0.08*SR);duck=np.convolve(duck,np.ones(int(0.18*SR))/int(0.18*SR),'same')
n0=min(len(vo),len(out));vo=vo[:n0];duck=duck[:n0];mix=vo+out[:n0]*0.55*duck;mix=np.tanh(mix*1.05)/np.tanh(1.05)*0.95
np.save('sfx_raw.npy',o if 'o' in dir() else out[:n0]);np.save('duck.npy',duck);np.save('vo_norm.npy',vo)
pcm=(np.stack([mix,mix],1)*32767).clip(-32768,32767).astype('<i2')
with wave.open('mix.wav','wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(SR);f.writeframes(pcm.tobytes())
print('ok')
