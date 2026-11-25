import sys,re,wave,json,numpy as np
D=sys.argv[1];HTML=sys.argv[2];SR=48000
def rd(p):
    w=wave.open(p);return np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(float)/32768
src={k:rd(f'{D}/{k}.wav') for k in ['narr','ded','gena2','gena_old','extra','coin']}
def envl(x):
    h=int(0.02*SR);return np.array([np.sqrt(np.mean(x[i:i+h]**2)) for i in range(0,len(x)-h,h)])
E={k:envl(v) for k,v in src.items()}
def tend(k,b):
    e=E[k];i=int(b/0.02)
    while i<len(e) and 20*np.log10(e[i]+1e-9)>-45:i+=1
    return i*0.02
def tstart(k,a):
    e=E[k];i=int(a/0.02)
    while i>0 and 20*np.log10(e[i-1]+1e-9)>-45:i-=1
    return i*0.02
V=[('gena_old',0.0,1.49,0.45,0,'g',[]),
 ('narr',0.16,1.48,2.5,1,'n',[]),
 ('narr',1.74,3.15,4.3,2,'n',[('ТЫ ВЫБРАЛА СТОРОЖА.',1.74,3.15)]),
 ('narr',3.17,5.28,5.9,2,'n',[('БЕЖИШЬ ЧЕРЕЗ ЛЕС.',3.17,4.35),('В *ТАПОЧКАХ.',4.37,5.28)]),
 ('narr',5.36,6.59,8.1,3,'n',[('СЗАДИ — *СВИСТОК.',5.36,6.59)]),
 ('narr',6.61,8.37,10.1,4,'n',[('ПРЫЖОК — И ТАПОК УЛЕТЕЛ.',6.61,8.37)]),
 ('narr',8.43,9.71,12.3,5,'n',[('ВПЕРЕДИ — *СВЕТ.',8.43,9.71)]),
 ('narr',9.73,10.89,13.9,6,'n',[('ТЫ КОЛОТИШЬ В ДВЕРЬ.',9.73,10.89)]),
 ('ded',0.0,2.39,16.0,7,'d',[]),
 ('narr',10.96,12.84,19.1,8,'n',[('НА СТЕНЕ — СТАРОЕ ФОТО.',10.96,12.84)]),
 ('narr',12.88,15.87,21.3,9,'n',[('ЛАГЕРЬ «ЗОРЬКА».',12.88,13.92),('ТЫСЯЧА ДЕВЯТЬСОТ ПЯТЬДЕСЯТ ШЕСТОЙ.',13.96,15.87)]),
 ('narr',15.89,17.69,24.4,9,'n',[('А С КРАЮ — ВОЖАТЫЙ ГЕНА.',15.89,17.69)]),
 ('narr',17.76,19.24,26.3,9,'n',[('ТАКОЙ ЖЕ, КАК *СЕГОДНЯ.',17.76,19.24)]),
 ('extra',0.0,2.07,28.0,9,'n',[('А В ПЕРВОМ РЯДУ… *ТЫ.',0.0,2.07)]),
 ('narr',19.36,20.25,30.1,10,'n',[('СТУК В ДВЕРЬ.',19.36,20.25)]),
 ('gena2',0.0,2.54,31.6,10,'g',[]),
 ('ded',2.80,4.60,34.1,10,'d',[]),
 ('extra',2.63,5.08,37.1,11,'n',[('НО ВАЛЕНКИ У ДЕДА…',2.63,3.9),('ТОЖЕ *МОКРЫЕ. И В *ТИНЕ.',3.92,5.08)]),
 ('narr',20.32,22.8,40.1,12,'n',[('МОКРЫЕ СЛЕДЫ.',20.32,21.4),('ВСЁ БЛИЖЕ К *КРОВАТИ.',21.44,22.8)]),
 ('gena_old',3.74,5.75,43.3,13,'g',[]),
 ('coin',0.0,3.25,46.6,14,'n',[]),
 ('coin',3.65,5.2,50.2,14,'n',[('ИЛИ РЕШИШЬ САМ?',3.72,5.04)])]
G=[(0,2.4),(2.4,4.2),(4.2,8.0),(8.0,10.0),(10.0,12.2),(12.2,13.8),(13.8,15.8),(15.8,19.0),(19.0,21.2),(21.2,30.0),(30.0,37.0),(37.0,40.0),(40.0,43.0),(43.0,45.6),(45.6,52.1)]
PAD=0.45;GAP=0.15;VV=[]
for k,a,b,at,g,who,subs in V:
    VV.append(dict(k=k,a=max(0,tstart(k,a)-0.03),b=tend(k,b)+0.06,at=at,g=g,who=who,subs=subs))
fs=[]
for gi,(o0,o1) in enumerate(G):
    vs=[v for v in VV if v['g']==gi];f=1.0
    for i,v in enumerate(vs):
        dur=v['b']-v['a'];f=max(f,(dur+(PAD if gi<len(G)-1 else 0.3))/(o1-v['at']))
        if i+1<len(vs):f=max(f,(dur+GAP)/(vs[i+1]['at']-v['at']))
    fs.append(f)
NB=[0.0]
for gi,(o0,o1) in enumerate(G):NB.append(NB[-1]+(o1-o0)*fs[gi])
OB=[g[0] for g in G]+[G[-1][1]];DUR=round(NB[-1],2)
def O2N(to):
    for i in range(len(G)):
        if to<=G[i][1] or i==len(G)-1:return NB[i]+(to-G[i][0])*fs[i]
N=int((DUR+0.1)*SR);tr={w:np.zeros(N) for w in 'ngd'};subs=[];TARGET=10**(-19/20);place=[]
for v in VV:
    st=max(O2N(v['at']),NB[v['g']]+0.08);seg=src[v['k']][int(v['a']*SR):int(v['b']*SR)].copy()
    act=seg[np.abs(seg)>0.01];rms=np.sqrt(np.mean(act**2)) if len(act) else 1e-3;seg*=min(TARGET/rms,4.0)
    f=int(0.012*SR);seg[:f]*=np.linspace(0,1,f);seg[-f:]*=np.linspace(1,0,f);i=int(st*SR);tr[v['who']][i:i+len(seg)]+=seg[:N-i]
    for txt,ws,we in v['subs']:subs.append((round(st+max(0,ws-v['a']),2),round(st+we-v['a'],2),txt))
    place.append((v['who'],round(st,2),round(st+v['b']-v['a'],2)))
for w in 'ngd':np.save(f'{D}/{w}v.npy',tr[w])
json.dump(dict(NB=NB,OB=OB,fs=fs,DUR=DUR,place=place),open(D+'/warp.json','w'))
def lipof(x):
    hop=SR//30;F=int(DUR*30)+2;env=np.array([np.sqrt(np.mean(x[i*hop:(i+1)*hop]**2)) for i in range(F)]);ref=np.percentile(env[env>0.005],90)
    l=np.clip(env/ref,0,1);l=np.convolve(l,[0.25,0.5,0.25],'same');l[l<0.08]=0;return ','.join(f'{q:.2f}' for q in l)
s=open(HTML).read()
s=re.sub(r"let LIPG=\[[^\]]*\];","let LIPG=["+lipof(tr['g'])+"];",s)
s=re.sub(r"let LIPD=\[[^\]]*\];","let LIPD=["+lipof(tr['d'])+"];",s)
s=re.sub(r"const SUBS_RAW=\[.*?\n\];","const SUBS_RAW=[\n"+"\n".join(f" [{a},{b},'{t}']," for a,b,t in subs)+"\n];",s,flags=re.S)
s=re.sub(r"const W=1080,H=1920,DUR=[0-9.]+;",f"const W=1080,H=1920,DUR={DUR};",s)
s=re.sub(r"const WNB=\[[^\]]*\],WOB=\[[^\]]*\];","const WNB="+json.dumps([round(x,4) for x in NB])+",WOB="+json.dumps(OB)+";",s)
open(HTML,'w').write(s);print('DUR',DUR,'factors',[round(x,2) for x in fs]);print(place)
