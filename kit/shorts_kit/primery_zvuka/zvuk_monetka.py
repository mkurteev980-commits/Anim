import numpy as np,wave
SR=48000;DUR=6.5;N=int(DUR*SR);rng=np.random.default_rng(9);out=np.zeros(N)
def band(x,lo,hi):
    X=np.fft.rfft(x);f=np.fft.rfftfreq(len(x),1/SR);return np.fft.irfft(X*((f>=lo)&(f<=hi)),len(x))
def nz(d):return rng.standard_normal(int(d*SR))
def norm(x):return x/(np.abs(x).max()+1e-9)
def add(t0,s,g=1):
    i=int(t0*SR);j=min(N,i+len(s));out[i:j]+=s[:j-i]*g
def boom(d,f):
    t=np.arange(int(d*SR))/SR;fr=f*(1+1.5*np.exp(-t*12));return np.sin(2*np.pi*np.cumsum(fr)/SR)*np.exp(-t*3.2)
def ping(d=1.4):
    t=np.arange(int(d*SR))/SR;return sum(a*np.sin(2*np.pi*f*t)*np.exp(-t*k) for f,a,k in [(2350,1,3),(3920,0.6,4),(5110,0.4,6),(6830,0.25,8)])
add(0.45,norm(ping()),0.55)
TE,T0=4.0,0.45;K=34/(2*(TE-T0))
t=np.arange(int((TE-T0)*SR))/SR;om=2*K*(TE-T0-t);flips=np.cumsum(om/np.pi)/SR
whirr=np.sin(2*np.pi*2350*t)*0.5+np.sin(2*np.pi*3920*t)*0.3
amp=(0.5+0.5*np.cos(2*np.pi*flips))*np.minimum(1,t/0.05)*(om/om[0])**0.6
add(T0,norm(whirr*amp),0.18)
n=int(0.6*SR);tt=np.arange(n)/SR;add(3.4,norm(band(nz(0.6),400,9000)*(tt/0.6)**2.5),0.3)
add(TE,norm(boom(1.4,44)),0.95);add(TE,norm(ping(1.8)),0.3)
for k in range(5):
    for dt,g in [(0,1),(0.18,0.7)]:
        t0=TE+0.1+k*0.62+dt
        if t0<DUR-0.1:add(t0,norm(boom(0.18,55)),0.45*g)
tt=np.arange(int(0.12*SR))/SR;add(4.6,np.sin(2*np.pi*(700+900*np.exp(-tt*30))*tt)*np.exp(-tt*25),0.25)
with wave.open('v.wav') as f:v=np.frombuffer(f.readframes(f.getnframes()),'<i2').astype(float)/32768
vo=np.zeros(N)
def place(a,b,at):
    seg=v[int(a*SR):int(b*SR)].copy();fd=int(0.01*SR);seg[:fd]*=np.linspace(0,1,fd);seg[-fd:]*=np.linspace(1,0,fd);i=int(at*SR);vo[i:i+len(seg)]+=seg[:N-i]
place(0,3.25,1.0);place(3.65,5.2,4.6)
mix=vo/np.abs(vo).max()*0.9+out*0.55;mix=np.tanh(mix*1.05)/np.tanh(1.05)*0.95
pcm=(np.stack([mix,mix],1)*32767).clip(-32768,32767).astype('<i2')
with wave.open('mix.wav','wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(SR);f.writeframes(pcm.tobytes())
print('ok')
