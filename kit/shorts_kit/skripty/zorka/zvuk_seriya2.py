import numpy as np,wave,json
WJ=json.load(open('warp.json'));SR=48000;DUR=WJ['DUR'];N=int((DUR+0.1)*SR);rng=np.random.default_rng(21);out=np.zeros(N)
OB,NB,fs=WJ['OB'],WJ['NB'],WJ['fs']
def O2N(to):
    for i in range(len(fs)):
        if to<=OB[i+1] or i==len(fs)-1:return NB[i]+(to-OB[i])*fs[i]
def band(x,lo,hi):
    X=np.fft.rfft(x);f=np.fft.rfftfreq(len(x),1/SR);return np.fft.irfft(X*((f>=lo)&(f<=hi)),len(x))
def nz(d):return rng.standard_normal(int(d*SR))
def norm(x):return x/(np.abs(x).max()+1e-9)
def addN(tn,s,g=1):
    i=int(tn*SR);j=min(N,i+len(s));out[i:j]+=s[:j-i]*g
def add(to,s,g=1):addN(O2N(to),s,g)
def env(d,k):return np.exp(-np.arange(int(d*SR))/SR*k)
def boom(d,f):
    t=np.arange(int(d*SR))/SR;fr=f*(1+1.5*np.exp(-t*12));return np.sin(2*np.pi*np.cumsum(fr)/SR)*np.exp(-t*3.2)
def whoosh(d=0.4):
    n=int(d*SR);t=np.arange(n)/n;return norm(band(nz(d),300,7000)*np.sin(np.pi*t)**2)
def click():return norm(band(nz(0.03),1500,9000)*env(0.03,200))
def beatN(t0,t1):
    k=0
    while True:
        for dt,g in [(0,1),(0.18,0.7)]:
            x=t0+k*0.62+dt
            if x>=t1:return
            addN(x,norm(boom(0.18,55)),0.45*g)
        k+=1
def droneN(t0,d,f=42,g=0.15):
    t=np.arange(int(d*SR))/SR;s=(np.sin(2*np.pi*f*t)+0.6*np.sin(2*np.pi*f*1.5*t+1))*np.minimum(1,t/0.4)*np.minimum(1,(d-t)/0.4);addN(t0,norm(s),g)
def cricketsN(t0,t1,g=0.05):
    k=t0
    while k<t1:
        for j in range(3):
            n=int(0.035*SR);t=np.arange(n)/SR;addN(k+j*0.06,np.sin(2*np.pi*4300*t)*np.sin(np.pi*t/0.035),g)
        k+=0.45+rng.random()*0.15
def ping(d=1.4):
    t=np.arange(int(d*SR))/SR;return sum(a*np.sin(2*np.pi*f*t)*np.exp(-t*k) for f,a,k in [(2350,1,3),(3920,0.6,4),(5110,0.4,6),(6830,0.25,8)])
# холодный старт
add(0.25,click(),0.5);add(0.42,norm(boom(1.2,44)),0.9);droneN(O2N(0.4),NB[1]-O2N(0.4),40,0.15)
# перемотка VHS
d=NB[2]-NB[1];t=np.arange(int(d*SR))/SR;rw=np.sin(2*np.pi*np.cumsum(900+1400*(t/d))/SR)*0.4+band(nz(d),2000,9000)*0.6;addN(NB[1],norm(rw)*np.minimum(1,t/0.1),0.22)
addN(NB[2]-0.05,click(),0.5)
# бег (реальное время)
for k in range(int((NB[3]-NB[2])/0.25)):
    addN(NB[2]+k*0.25+rng.random()*0.03,norm(band(nz(0.09),500,5000)*env(0.09,35)),0.25)
w=norm(band(nz(NB[6]-NB[2]),80,900));addN(NB[2],w,0.06)
for k in range(int((NB[4]-NB[3])/0.31)):
    addN(NB[3]+k*0.31,norm(band(nz(0.1),300,3000)*env(0.1,30)),0.25)
t=np.arange(int(0.8*SR))/SR;addN(NB[3]+1.65,np.sin(2*np.pi*2600*t)*(0.6+0.4*np.sign(np.sin(2*np.pi*28*t)))*np.minimum(1,t/0.03)*np.minimum(1,(0.8-t)/0.08),0.2)
for k in range(4):addN(NB[4]+k*0.25,norm(band(nz(0.09),500,5000)*env(0.09,35)),0.25)
addN(NB[4]+1.02,norm(boom(0.4,70)),0.6);addN(NB[4]+1.02,norm(band(nz(0.3),300,4000)*env(0.3,15)),0.3)
cricketsN(NB[5],NB[8],0.05)
for h in [0.2,0.52,0.85]:addN(NB[6]+h,norm(boom(0.3,65)),0.7);addN(NB[6]+h,norm(band(nz(0.08),200,2500)*env(0.08,40)),0.35)
n=int(0.8*SR);t=np.arange(n)/SR;cr=np.sin(2*np.pi*np.cumsum(300+200*np.sin(t*40))/SR)*(1+0.6*np.sign(np.sin(2*np.pi*35*t)))*np.minimum(1,t/0.1)*np.minimum(1,(0.8-t)/0.1);addN(NB[6]+1.25,norm(band(cr,200,4000)),0.25)
# внутри сторожки: треск печи, часы
for k in range(int((NB[9]-NB[8])/0.13)):
    if rng.random()<0.45:addN(NB[8]+k*0.13,norm(band(nz(0.02),800,6000)*env(0.02,250)),0.15)
for k in range(int((NB[9]-NB[8])/0.5)):
    tt=np.arange(int(0.05*SR))/SR;addN(NB[8]+k*0.5,np.sin(2*np.pi*(2000 if k%2 else 1600)*tt)*np.exp(-tt*80),0.1)
# фото
droneN(NB[9],NB[10]-NB[9],38,0.15);add(24.25,norm(boom(0.9,48)),0.7);add(27.75,norm(boom(1.2,44)),0.9);add(27.75,norm(band(nz(0.5),2500,9000)*env(0.5,6)),0.2);beatN(O2N(28.1),NB[10])
# стук, дверь, шаги Гены
for x in [30.25,30.45,30.65]:add(x,norm(boom(0.25,80)),0.7);add(x,norm(band(nz(0.06),200,3000)*env(0.06,45)),0.3)
add(31.0,norm(band(cr,200,4000)),0.25)
for k in range(5):add(31.2+k*0.22,norm(band(nz(0.1),200,2500)*env(0.1,28)),0.3)
droneN(NB[10],NB[13]-NB[10],40,0.1)
# капли и мокрые шаги
for k in range(10):tt=np.arange(int(0.12*SR))/SR;addN(NB[11]+k*0.3+rng.random()*0.1,np.sin(2*np.pi*(1000+rng.random()*600)*tt*(1+tt*6))*np.exp(-tt*40),0.16)
for k in range(5):addN(NB[12]+k*0.45,norm(band(nz(0.15),150,1500)*env(0.15,18)),0.14)
beatN(NB[12]+0.2,NB[13])
# раскрытие
add(43.3,norm(boom(1.3,42)),0.9);add(43.3,click(),0.4)
# монетка (локальное время сцены 45.6+)
c0=45.6
add(c0+0.45,norm(ping()),0.5)
TE,T0=4.0,0.45;K=34/(2*(TE-T0));t=np.arange(int((TE-T0)*SR))/SR;om=2*K*(TE-T0-t);fl=np.cumsum(om/np.pi)/SR;wh=np.sin(2*np.pi*2350*t)*0.5+np.sin(2*np.pi*3920*t)*0.3;am=(0.5+0.5*np.cos(2*np.pi*fl))*np.minimum(1,t/0.05)*(om/om[0])**0.6;add(c0+T0,norm(wh*am),0.16)
n=int(0.6*SR);t=np.arange(n)/SR;add(c0+3.4,norm(band(nz(0.6),400,9000)*(t/0.6)**2.5),0.3);add(c0+TE,norm(boom(1.4,44)),0.9);add(c0+TE,norm(ping(1.8)),0.25)
beatN(O2N(c0+TE+0.1),DUR-0.1)
tt=np.arange(int(0.12*SR))/SR;add(c0+4.6,np.sin(2*np.pi*(700+900*np.exp(-tt*30))*tt)*np.exp(-tt*25),0.22)
vo=np.load('nv.npy')+np.load('gv.npy')+np.load('dv.npy');vo=vo/np.abs(vo).max()*0.95
n0=min(len(vo),len(out));vo=vo[:n0];o=out[:n0]
ev=np.convolve(np.abs(vo),np.ones(int(0.06*SR))/int(0.06*SR),'same');duck=1-0.92*np.clip(ev/0.015,0,1);duck=np.convolve(duck,np.ones(int(0.18*SR))/int(0.18*SR),'same')
mix=vo+o*0.55*duck;mix=np.tanh(mix*1.05)/np.tanh(1.05)*0.95
np.save('sfx_raw.npy',o if 'o' in dir() else out[:n0]);np.save('duck.npy',duck);np.save('vo_norm.npy',vo)
pcm=(np.stack([mix,mix],1)*32767).clip(-32768,32767).astype('<i2')
with wave.open('mix.wav','wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(SR);f.writeframes(pcm.tobytes())
print('ok',n0/SR)
