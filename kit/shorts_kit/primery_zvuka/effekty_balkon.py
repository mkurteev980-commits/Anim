import numpy as np, wave, sys
SR=48000; DUR=51.0; N=int(SR*DUR)
rng=np.random.default_rng(7)
out=np.zeros(N)
def band(x,lo,hi):
    X=np.fft.rfft(x); f=np.fft.rfftfreq(len(x),1/SR)
    m=((f>=lo)&(f<=hi)).astype(float)
    # soft edges
    m=np.convolve(m,np.hanning(41)/np.hanning(41).sum(),mode='same')
    return np.fft.irfft(X*m,len(x))
def add(t0,sig,g=1.0):
    i=int(t0*SR); j=min(N,i+len(sig)); out[i:j]+=sig[:j-i]*g
def env(n,a,d):
    t=np.arange(n)/SR; return (1-np.exp(-t/a))*np.exp(-t/d)
def norm(x): return x/ (np.abs(x).max()+1e-9)

def whoosh(d=0.42):
    n=int(d*SR); t=np.arange(n)/n
    lo=band(rng.standard_normal(n),200,900); mid=band(rng.standard_normal(n),900,3500); hi=band(rng.standard_normal(n),3500,9000)
    s=lo*np.clip(1-2*t,0,1)+mid*np.sin(np.pi*t)+hi*np.clip(2*t-1,0,1)*0.6
    e=np.sin(np.pi*np.clip(t*1.15,0,1))**2*np.exp(-2*t)
    return norm(s*e)
def click():
    n=int(0.25*SR); t=np.arange(n)/SR; s=np.zeros(n)
    for k,dt in enumerate([0.0,0.065]):
        i=int(dt*SR); m=n-i; tt=t[:m]
        hit=band(rng.standard_normal(m),2000,12000)*np.exp(-tt/0.003)
        ring=(np.sin(2*np.pi*2300*tt)+0.6*np.sin(2*np.pi*3700*tt))*np.exp(-tt/0.02)
        thunk=np.sin(2*np.pi*(170 if k else 210)*tt)*np.exp(-tt/0.035)
        s[i:]+=(hit*1.2+ring*0.35+thunk*0.9)*(1.0 if k else 0.8)
    return norm(s)
def knock():
    n=int(0.3*SR); t=np.arange(n)/SR; s=np.zeros(n)
    for dt in [0.0,0.13]:
        i=int(dt*SR); tt=t[:n-i]
        thump=np.sin(2*np.pi*160*tt)*np.exp(-tt/0.05)+0.5*np.sin(2*np.pi*410*tt)*np.exp(-tt/0.03)
        glass=0.25*np.sin(2*np.pi*1350*tt)*np.exp(-tt/0.06)
        hit=band(rng.standard_normal(n-i),300,4000)*np.exp(-tt/0.004)*0.8
        s[i:]+=thump+glass+hit
    return norm(s)
def water(d):
    n=int(d*SR); t=np.arange(n)/SR
    s=band(rng.standard_normal(n),350,2600)          # глухо, из-за двери
    s*=1+0.25*np.sin(2*np.pi*0.7*t)+0.15*rng.standard_normal(n).cumsum()/np.sqrt(n)*0
    fade=np.minimum(1,t/0.35)*np.minimum(1,(d-t)/0.08)
    return norm(s*fade)
def wind(d):
    n=int(d*SR); t=np.arange(n)/SR
    s=band(rng.standard_normal(n),60,700)
    gust=0.6+0.4*np.sin(2*np.pi*0.23*t)*np.sin(2*np.pi*0.09*t+1)
    return norm(s*gust)

# эффекты из списка
for t0 in [2.4,11.8,29.6,44.6]: add(t0-0.05,whoosh(),0.75)
for t0 in [10.35,40.1]: add(t0,click(),0.9)
for t0 in [17.95,18.55]: add(t0-0.03,knock(),0.85)
add(34.0,water(38.4-34.0),0.32)
# тихий ветер на улице (фон)
w=wind(DUR); g=np.zeros(N); tt=np.arange(N)/SR
def seg(a,b,v,fi=0.3):
    m=(tt>=a)&(tt<b); x=np.minimum(1,(tt-a)/fi)*np.minimum(1,(b-tt)/0.05); g[m]=np.maximum(g[m],v*x[m])
seg(0.5,2.4,0.16,0.8); seg(2.4,9.4,0.2,0.05); seg(11.8,21.2,0.17,0.05); seg(21.2,25.6,0.08,0.05)
out+=w*g
out=out/np.abs(out).max()*0.89
st=np.stack([out,out],1)
pcm=(st*32767).astype('<i2')
with wave.open(sys.argv[1],'wb') as f:
    f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes(pcm.tobytes())
print('ok',len(out)/SR)
