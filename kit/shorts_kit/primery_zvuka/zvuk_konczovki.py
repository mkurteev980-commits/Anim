import numpy as np,wave
SR=48000;N=int(15*SR);rng=np.random.default_rng(5);out=np.zeros(N)
def band(x,lo,hi):
    X=np.fft.rfft(x);f=np.fft.rfftfreq(len(x),1/SR);return np.fft.irfft(X*((f>=lo)&(f<=hi)),len(x))
def nz(d):return rng.standard_normal(int(d*SR))
def norm(x):return x/(np.abs(x).max()+1e-9)
def add(t0,s,g=1):
    i=int(t0*SR);j=min(N,i+len(s));out[i:j]+=s[:j-i]*g
def env(d,k):return np.exp(-np.arange(int(d*SR))/SR*k)
def boom(d,f):
    t=np.arange(int(d*SR))/SR;fr=f*(1+1.5*np.exp(-t*12));return np.sin(2*np.pi*np.cumsum(fr)/SR)*np.exp(-t*3.5)
def whoosh(d=0.4):
    n=int(d*SR);t=np.arange(n)/n;return norm(band(nz(d),300,7000)*np.sin(np.pi*t)**2)
# A
add(0.28,norm(band(nz(0.35),1500,12000)*env(0.35,12)),0.5)
add(0.55,whoosh(0.35),0.5);add(0.62,norm(boom(0.8,50)),0.6)
for k,t0 in enumerate([1.5,2.5,3.5]):
    t=np.arange(int(0.08*SR))/SR;add(t0,np.sin(2*np.pi*(1200 if k<2 else 1600)*t)*np.exp(-t*60),0.45)
    add(t0+0.5,np.sin(2*np.pi*800*t)*np.exp(-t*60),0.3)
t=np.arange(int(0.5*SR))/SR;add(4.5,np.sign(np.sin(2*np.pi*140*t))*np.exp(-t*5)*0.6,0.35)
# B
w=norm(band(nz(5),80,900));w*=0.6+0.4*np.sin(2*np.pi*0.4*np.arange(len(w))/SR);add(5,w,0.12)
for t0 in np.arange(5.3,10,0.7):
    t=np.arange(int(0.09*SR))/SR;add(t0,np.sin(2*np.pi*(1800-1200*t/0.09)*t)*np.exp(-t*40),0.2)
for t0 in [5.4,7.9]:
    add(t0,norm(band(nz(0.25),200,2000)*env(0.25,18)),0.25)
n=int(0.8*SR);t=np.arange(n)/SR;cr=np.sin(2*np.pi*np.cumsum(300+200*np.sin(t*40))/SR)*(1+0.6*np.sign(np.sin(2*np.pi*35*t)))*np.minimum(1,t/0.1)*np.minimum(1,(0.8-t)/0.1);add(9.05,norm(band(cr,200,4000)),0.3)
add(4.95,whoosh(0.35),0.4)
# C
add(9.95,whoosh(0.35),0.4)
for k in range(6):
    for dt,g in [(0,1),(0.18,0.7)]:
        t0=10+k*0.62+dt
        if t0<13.6:add(t0,norm(boom(0.18,55)),0.5*g)
n=int(0.6*SR);t=np.arange(n)/SR;add(13.0,norm(band(nz(0.6),300,8000)*(t/0.6)**2),0.35)
add(13.6,norm(boom(1.2,42)),0.9)
for t0 in [13.95,14.05,14.12,14.2,14.3,14.37,14.45,14.55]:
    add(t0,norm(band(nz(0.03),1500,8000)*env(0.03,150)),0.25)
mix=np.tanh(out*1.1)/np.tanh(1.1)*0.9
pcm=(np.stack([mix,mix],1)*32767).clip(-32768,32767).astype('<i2')
with wave.open('sfx.wav','wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(SR);f.writeframes(pcm.tobytes())
print('ok')
