import numpy as np,sys,json
D=sys.argv[1];SR=48000
vo=np.load(D+'/vo_norm.npy');sfx=np.load(D+'/sfx_raw.npy');duck=np.load(D+'/duck.npy')
n=min(len(vo),len(sfx),len(duck));vo,sfx,duck=vo[:n],sfx[:n]*0.55*duck[:n],duck[:n]
def bp(x):
    X=np.fft.rfft(x);f=np.fft.rfftfreq(len(x),1/SR);return np.fft.irfft(X*((f>=300)&(f<=4000)),len(x))
vo,sfx=bp(vo),bp(sfx)
h=int(0.05*SR);rms=lambda x:np.sqrt(np.mean(x**2))+1e-9
bad=[]
for i in range(0,n-h,h):
    v=rms(vo[i:i+h]);s=rms(sfx[i:i+h])
    if 20*np.log10(v)>-38 and 20*np.log10(s)>20*np.log10(v)-6:bad.append((i/SR,round(20*np.log10(s)-20*np.log10(v),1)))
grp=[]
for t,d in bad:
    if grp and t-grp[-1][1]<0.3:grp[-1]=[grp[-1][0],t,max(grp[-1][2],d)]
    else:grp.append([t,t,d])
W=json.load(open(D+'/warp.json'))
for a,b,d in grp:print(f"{a:6.2f}-{b+0.05:6.2f}с  эффект громче голоса/вровень (+{d} дБ)")
print('ИТОГО мест, где эффект глушит голос:',len(grp))
